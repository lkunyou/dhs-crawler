package com.thaiautoparts.service.impl;

import com.thaiautoparts.service.CustomerSearchService;
import com.thaiautoparts.service.SystemConfigService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

@Slf4j
@Service
public class CustomerSearchServiceImpl implements CustomerSearchService {

    private final SystemConfigService systemConfigService;

    public CustomerSearchServiceImpl(SystemConfigService systemConfigService) {
        this.systemConfigService = systemConfigService;
    }

    @Value("${app.search.serpapi-key:}")
    private String serpApiKeyYml;

    @Value("${app.search.brave-api-key:}")
    private String braveApiKeyYml;

    @Value("${app.search.bing-api-key:}")
    private String bingApiKeyYml;

    private String getSearchConfig(String key, String defaultValue) {
        return systemConfigService.getValue(key, defaultValue);
    }

    private final RestTemplate restTemplate = new RestTemplate();

    @Override
    public List<Map<String, Object>> searchCompanies(String keyword, String source, String country) {
        if (country == null || country.isEmpty()) {
            country = "TH";
        }

        switch (source.toLowerCase()) {
            case "serpapi":
                return searchWithSerpApi(keyword, country);
            case "brave":
                return searchWithBrave(keyword, country);
            case "bing":
                return searchWithBing(keyword, country);
            case "linkedin":
                return searchWithLinkedIn(keyword, country);
            case "yellowpages":
                return searchYellowPages(keyword, country);
            default:
                return searchWithBrave(keyword, country);
        }
    }

    @Override
    public List<Map<String, Object>> batchSearchCompanies(List<String> keywords, String source, String country) {
        List<Map<String, Object>> allResults = new ArrayList<>();
        for (String keyword : keywords) {
            try {
                List<Map<String, Object>> results = searchCompanies(keyword, source, country);
                allResults.addAll(results);
            } catch (Exception e) {
                log.error("搜索失败: {}", keyword, e);
            }
        }
        return allResults;
    }

    private List<Map<String, Object>> searchWithSerpApi(String keyword, String country) {
        List<Map<String, Object>> results = new ArrayList<>();
        try {
            String query = URLEncoder.encode(keyword + " auto parts Thailand", StandardCharsets.UTF_8);
            String url = String.format(
                "https://serpapi.com/search.json?q=%s&gl=%s&hl=en&api_key=%s",
                query, country.toLowerCase(), getSearchConfig("search.serpapi-key", serpApiKeyYml)
            );

            ResponseEntity<Map> response = restTemplate.getForEntity(url, Map.class);
            Map<String, Object> body = response.getBody();

            if (body != null && body.containsKey("organic_results")) {
                List<Map<String, Object>> organicResults = (List<Map<String, Object>>) body.get("organic_results");
                for (Map<String, Object> item : organicResults) {
                    Map<String, Object> company = new HashMap<>();
                    company.put("companyName", item.get("title"));
                    company.put("website", item.get("link"));
                    company.put("description", item.get("snippet"));
                    company.put("source", "SerpAPI");
                    company.put("country", country);
                    company.put("searchKeyword", keyword);

                    // 尝试从描述中提取邮箱和电话
                    extractContactInfo(company, (String) item.get("snippet"));

                    results.add(company);
                }
            }
        } catch (Exception e) {
            log.error("SerpAPI搜索失败", e);
        }
        return results;
    }

    private List<Map<String, Object>> searchWithBrave(String keyword, String country) {
        List<Map<String, Object>> results = new ArrayList<>();
        try {
            String query = URLEncoder.encode(keyword + " auto parts Thailand", StandardCharsets.UTF_8);
            String url = String.format(
                "https://api.search.brave.com/res/v1/web/search?q=%s&country=%s&count=20",
                query, country
            );

            HttpHeaders headers = new HttpHeaders();
            headers.set("X-Subscription-Token", getSearchConfig("search.brave-api-key", braveApiKeyYml));
            headers.set("Accept", "application/json");

            HttpEntity<String> entity = new HttpEntity<>(headers);
            ResponseEntity<Map> response = restTemplate.exchange(url, HttpMethod.GET, entity, Map.class);
            Map<String, Object> body = response.getBody();

            if (body != null && body.containsKey("web")) {
                Map<String, Object> web = (Map<String, Object>) body.get("web");
                if (web.containsKey("results")) {
                    List<Map<String, Object>> webResults = (List<Map<String, Object>>) web.get("results");
                    for (Map<String, Object> item : webResults) {
                        Map<String, Object> company = new HashMap<>();
                        company.put("companyName", item.get("title"));
                        company.put("website", item.get("url"));
                        company.put("description", item.get("description"));
                        company.put("source", "Brave Search");
                        company.put("country", country);
                        company.put("searchKeyword", keyword);

                        extractContactInfo(company, (String) item.get("description"));

                        results.add(company);
                    }
                }
            }
        } catch (Exception e) {
            log.error("Brave搜索失败", e);
        }
        return results;
    }

    private List<Map<String, Object>> searchWithBing(String keyword, String country) {
        List<Map<String, Object>> results = new ArrayList<>();
        try {
            String query = URLEncoder.encode(keyword + " auto parts Thailand", StandardCharsets.UTF_8);
            String bingUrlTemplate = getSearchConfig("search.bing-url", "https://api.bing.microsoft.com/v7.0/search?q=%s&market=%s-TH&count=20");
            String url = String.format(bingUrlTemplate, query, country);

            HttpHeaders headers = new HttpHeaders();
            headers.set("Ocp-Apim-Subscription-Key", getSearchConfig("search.bing-api-key", bingApiKeyYml));
            headers.set("Accept", "application/json");

            HttpEntity<String> entity = new HttpEntity<>(headers);
            ResponseEntity<Map> response = restTemplate.exchange(url, HttpMethod.GET, entity, Map.class);
            Map<String, Object> body = response.getBody();

            if (body != null && body.containsKey("webPages")) {
                Map<String, Object> webPages = (Map<String, Object>) body.get("webPages");
                if (webPages.containsKey("value")) {
                    List<Map<String, Object>> webResults = (List<Map<String, Object>>) webPages.get("value");
                    for (Map<String, Object> item : webResults) {
                        Map<String, Object> company = new HashMap<>();
                        company.put("companyName", item.get("name"));
                        company.put("website", item.get("url"));
                        company.put("description", item.get("snippet"));
                        company.put("source", "Bing");
                        company.put("country", country);
                        company.put("searchKeyword", keyword);

                        extractContactInfo(company, (String) item.get("snippet"));

                        results.add(company);
                    }
                }
            }
        } catch (Exception e) {
            log.error("Bing搜索失败", e);
        }
        return results;
    }

    private List<Map<String, Object>> searchWithLinkedIn(String keyword, String country) {
        List<Map<String, Object>> results = new ArrayList<>();
        try {
            String query = URLEncoder.encode(keyword + " auto parts Thailand", StandardCharsets.UTF_8);
            String url = String.format(
                "https://www.linkedin.com/search/results/companies/?keywords=%s&geoUrn=%%5B%%22103323778%%22%%5D",
                query
            );

            HttpHeaders headers = new HttpHeaders();
            headers.set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36");

            HttpEntity<String> entity = new HttpEntity<>(headers);
            ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.GET, entity, String.class);

            // 解析LinkedIn搜索结果（简化版本）
            Pattern pattern = Pattern.compile("company-name[^>]*>([^<]+)");
            Matcher matcher = pattern.matcher(response.getBody());

            while (matcher.find()) {
                Map<String, Object> company = new HashMap<>();
                company.put("companyName", matcher.group(1).trim());
                company.put("source", "LinkedIn");
                company.put("country", country);
                company.put("searchKeyword", keyword);
                results.add(company);
            }
        } catch (Exception e) {
            log.error("LinkedIn搜索失败", e);
        }
        return results;
    }

    private List<Map<String, Object>> searchYellowPages(String keyword, String country) {
        List<Map<String, Object>> results = new ArrayList<>();
        try {
            String query = URLEncoder.encode(keyword + " auto parts", StandardCharsets.UTF_8);
            String url = String.format(
                "https://www.yellowpages.co.th/search?search_terms=%s&geo_location_terms=Thailand",
                query
            );

            HttpHeaders headers = new HttpHeaders();
            headers.set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36");

            HttpEntity<String> entity = new HttpEntity<>(headers);
            ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.GET, entity, String.class);

            // 解析Yellow Pages结果（简化版本）
            Pattern pattern = Pattern.compile("business-name[^>]*>([^<]+)");
            Matcher matcher = pattern.matcher(response.getBody());

            while (matcher.find()) {
                Map<String, Object> company = new HashMap<>();
                company.put("companyName", matcher.group(1).trim());
                company.put("source", "Yellow Pages");
                company.put("country", country);
                company.put("searchKeyword", keyword);
                results.add(company);
            }
        } catch (Exception e) {
            log.error("Yellow Pages搜索失败", e);
        }
        return results;
    }

    private void extractContactInfo(Map<String, Object> company, String text) {
        if (text == null) return;

        // 提取邮箱
        Pattern emailPattern = Pattern.compile("[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}");
        Matcher emailMatcher = emailPattern.matcher(text);
        if (emailMatcher.find()) {
            company.put("email", emailMatcher.group());
        }

        // 提取电话（泰国格式）
        Pattern phonePattern = Pattern.compile("(\\+66|66|0)[\\s-]?[2-9][\\d]{2}[\\s-]?[\\d]{3}[\\s-]?[\\d]{4}");
        Matcher phoneMatcher = phonePattern.matcher(text);
        if (phoneMatcher.find()) {
            company.put("phone", phoneMatcher.group().replaceAll("[\\s-]", ""));
        }
    }
}