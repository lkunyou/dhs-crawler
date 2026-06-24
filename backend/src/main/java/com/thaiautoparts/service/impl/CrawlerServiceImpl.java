package com.thaiautoparts.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.thaiautoparts.entity.Company;
import com.thaiautoparts.entity.CrawlerTask;
import com.thaiautoparts.repository.CompanyMapper;
import com.thaiautoparts.repository.CrawlerTaskMapper;
import com.thaiautoparts.service.CrawlerService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ClassPathResource;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Slf4j
@Service
@RequiredArgsConstructor
public class CrawlerServiceImpl implements CrawlerService {

    private final CrawlerTaskMapper crawlerTaskMapper;
    private final CompanyMapper companyMapper;
    private final ObjectMapper objectMapper;

    @Value("${crawler.python.path:python}")
    private String pythonPath;

    @Value("${crawler.script.output-dir:/tmp}")
    private String outputDir;

    @Override
    @Transactional
    public CrawlerTask createCrawlerTask(CrawlerTask task) {
        if (task.getStatus() == null) {
            task.setStatus("Pending");
        }
        if (task.getProgress() == null) {
            task.setProgress(0);
        }
        if (task.getTargetCountry() == null) {
            task.setTargetCountry("Thailand");
        }
        crawlerTaskMapper.insert(task);
        return task;
    }

    @Override
    @Transactional
    public CrawlerTask startCrawlerTask(Long taskId) {
        CrawlerTask task = crawlerTaskMapper.selectById(taskId);
        if (task == null) {
            throw new RuntimeException("Task not found: " + taskId);
        }
        
        task.setStatus("Running");
        task.setStartedAt(LocalDateTime.now());
        task.setProgress(0);
        crawlerTaskMapper.updateById(task);
        
        executeCrawlerScript(task);
        
        return task;
    }

    @Override
    @Transactional
    public CrawlerTask stopCrawlerTask(Long taskId) {
        CrawlerTask task = crawlerTaskMapper.selectById(taskId);
        if (task == null) {
            throw new RuntimeException("Task not found: " + taskId);
        }
        
        task.setStatus("Paused");
        crawlerTaskMapper.updateById(task);
        return task;
    }

    @Override
    public List<CrawlerTask> getTaskHistory() {
        LambdaQueryWrapper<CrawlerTask> wrapper = new LambdaQueryWrapper<>();
        wrapper.orderByDesc(CrawlerTask::getCreatedAt);
        wrapper.last("LIMIT 100");
        return crawlerTaskMapper.selectList(wrapper);
    }

    @Override
    public List<CrawlerTask> getRunningTasks() {
        LambdaQueryWrapper<CrawlerTask> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(CrawlerTask::getStatus, "Running");
        return crawlerTaskMapper.selectList(wrapper);
    }

    @Override
    public Map<String, Object> getTaskStats() {
        Map<String, Object> stats = new HashMap<>();
        
        LambdaQueryWrapper<CrawlerTask> wrapper = new LambdaQueryWrapper<>();
        long total = crawlerTaskMapper.selectCount(wrapper);
        
        wrapper.eq(CrawlerTask::getStatus, "Running");
        long running = crawlerTaskMapper.selectCount(wrapper);
        
        wrapper.eq(CrawlerTask::getStatus, "Completed");
        long completed = crawlerTaskMapper.selectCount(wrapper);
        
        stats.put("total", total);
        stats.put("running", running);
        stats.put("completed", completed);
        
        return stats;
    }

    @Override
    public void scheduleCrawlerTask(CrawlerTask task) {
        createCrawlerTask(task);
        log.info("Crawler task scheduled: {}", task.getTaskName());
    }

    @Async
    protected void executeCrawlerScript(CrawlerTask task) {
        try {
            String crawlerScript = switch (task.getSourceType()) {
                case "Google_Search" -> "google_crawler.py";
                case "Google_Maps" -> "google_maps_crawler.py";
                case "LinkedIn" -> "linkedin_crawler.py";
                case "B2B_Platform" -> "b2b_crawler.py";
                default -> null;
            };

            if (crawlerScript == null) {
                completeTask(task.getId(), "Failed", "Unsupported source type");
                return;
            }

            Path configFile = writeTaskConfig(task);
            String scriptPath = extractScript(crawlerScript);

            ProcessBuilder pb = new ProcessBuilder(pythonPath, scriptPath, task.getId().toString());
            pb.redirectErrorStream(true);
            Process process = pb.start();

            try (BufferedReader reader = new BufferedReader(
                    new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8))) {
                
                String line;
                int totalFound = 0;
                int newCompanies = 0;
                
                while ((line = reader.readLine()) != null) {
                    log.debug("Crawler output: {}", line);
                    
                    if (line.startsWith("PROGRESS:")) {
                        int progress = Integer.parseInt(line.substring(9));
                        updateProgress(task.getId(), progress);
                    } else if (line.startsWith("FOUND:")) {
                        int found = Integer.parseInt(line.substring(6));
                        totalFound += found;
                        newCompanies += found;
                        updateProgress(task.getId(), totalFound);
                    } else if (line.startsWith("FINISHED:")) {
                        String resultJson = line.substring(9);
                        processCrawlerResult(task.getId(), resultJson);
                    }
                }
                
                int exitCode = process.waitFor();
                if (exitCode != 0 && !task.getStatus().equals("Completed")) {
                    completeTask(task.getId(), "Failed", "Python script exited with code: " + exitCode);
                }
            }

            Files.deleteIfExists(configFile);
            
        } catch (Exception e) {
            log.error("Failed to execute crawler task {}: {}", task.getId(), e.getMessage(), e);
            completeTask(task.getId(), "Failed", e.getMessage());
        }
    }

    private Path writeTaskConfig(CrawlerTask task) throws IOException {
        Map<String, Object> config = new HashMap<>();
        config.put("taskId", task.getId());
        config.put("taskName", task.getTaskName());
        config.put("sourceType", task.getSourceType());
        config.put("targetCountry", task.getTargetCountry());
        config.put("targetCity", task.getTargetCity());
        
        if (task.getKeywords() != null) {
            try {
                List<String> keywords = objectMapper.readValue(task.getKeywords(), 
                        new TypeReference<List<String>>() {});
                config.put("keywords", keywords);
            } catch (Exception e) {
                config.put("keywords", task.getKeywords());
            }
        }
        
        if (task.getFilters() != null) {
            try {
                Map<String, Object> filters = objectMapper.readValue(task.getFilters(),
                        new TypeReference<Map<String, Object>>() {});
                config.put("filters", filters);
            } catch (Exception e) {
                config.put("filters", task.getFilters());
            }
        }

        Path outputPath = Paths.get(outputDir);
        if (!Files.exists(outputPath)) {
            Files.createDirectories(outputPath);
        }

        Path configFile = outputPath.resolve("crawler_task_" + task.getId() + ".json");
        Files.writeString(configFile, objectMapper.writeValueAsString(config), StandardCharsets.UTF_8);
        
        return configFile;
    }

    private String extractScript(String scriptName) throws IOException {
        Path tempDir = Paths.get(outputDir, "scripts");
        if (!Files.exists(tempDir)) {
            Files.createDirectories(tempDir);
        }

        Path scriptPath = tempDir.resolve(scriptName);
        
        if (!Files.exists(scriptPath)) {
            ClassPathResource resource = new ClassPathResource("crawler/" + scriptName);
            try (InputStream is = resource.getInputStream()) {
                Files.copy(is, scriptPath);
            }
        }

        return scriptPath.toString();
    }

    private void processCrawlerResult(Long taskId, String resultJson) {
        try {
            JsonNode root = objectMapper.readTree(resultJson);
            
            int totalFound = root.has("totalFound") ? root.get("totalFound").asInt() : 0;
            int newCompanies = root.has("newCompanies") ? root.get("newCompanies").asInt() : 0;
            int duplicates = root.has("duplicates") ? root.get("duplicates").asInt() : 0;
            
            CrawlerTask task = crawlerTaskMapper.selectById(taskId);
            if (task != null) {
                task.setTotalFound(totalFound);
                task.setNewCompanies(newCompanies);
                task.setDuplicates(duplicates);
                crawlerTaskMapper.updateById(task);
            }

            if (root.has("companies")) {
                JsonNode companiesNode = root.get("companies");
                if (companiesNode.isArray()) {
                    for (JsonNode companyNode : companiesNode) {
                        saveCompany(taskId, companyNode);
                    }
                }
            }

            completeTask(taskId, "Completed", null);
            
        } catch (Exception e) {
            log.error("Failed to process crawler result: {}", e.getMessage(), e);
            completeTask(taskId, "Completed", "Result processing error: " + e.getMessage());
        }
    }

    @Transactional
    protected void saveCompany(Long taskId, JsonNode companyNode) {
        try {
            String companyName = companyNode.has("companyName") ? companyNode.get("companyName").asText() : "";
            
            if (companyName.isEmpty()) {
                return;
            }

            LambdaQueryWrapper<Company> wrapper = new LambdaQueryWrapper<>();
            wrapper.eq(Company::getCompanyName, companyName);
            Company existing = companyMapper.selectOne(wrapper);
            
            if (existing != null) {
                existing.setIsDuplicate(true);
                companyMapper.updateById(existing);
                return;
            }

            Company company = new Company();
            company.setCompanyName(companyName);
            
            if (companyNode.has("website")) {
                company.setWebsite(companyNode.get("website").asText());
            }
            if (companyNode.has("city")) {
                company.setCity(companyNode.get("city").asText());
            }
            if (companyNode.has("country")) {
                company.setAddress(companyNode.get("country").asText());
            }
            if (companyNode.has("description")) {
                company.setDescription(companyNode.get("description").asText());
            }
            if (companyNode.has("source")) {
                company.setSource(companyNode.get("source").asText());
            }
            
            company.setSourceType("Crawler");
            company.setLeadGrade("C");
            company.setLeadScore(0);
            company.setStatus("New");
            company.setIsDuplicate(false);
            
            companyMapper.insert(company);
            
        } catch (Exception e) {
            log.warn("Failed to save company: {}", e.getMessage());
        }
    }

    @Transactional
    protected void updateProgress(Long taskId, int progress) {
        CrawlerTask task = crawlerTaskMapper.selectById(taskId);
        if (task != null && "Running".equals(task.getStatus())) {
            task.setProgress(Math.min(progress, 99));
            crawlerTaskMapper.updateById(task);
        }
    }

    @Transactional
    protected void completeTask(Long taskId, String status, String errorMessage) {
        CrawlerTask task = crawlerTaskMapper.selectById(taskId);
        if (task != null) {
            task.setStatus(status);
            task.setProgress(status.equals("Completed") ? 100 : task.getProgress());
            task.setCompletedAt(LocalDateTime.now());
            if (errorMessage != null) {
                task.setErrorMessage(errorMessage);
            }
            crawlerTaskMapper.updateById(task);
            log.info("Crawler task {} completed with status: {}", taskId, status);
        }
    }
}