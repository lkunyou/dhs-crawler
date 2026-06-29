package com.thaiautoparts.service.impl;

import com.thaiautoparts.dto.RagDocument;
import com.thaiautoparts.dto.RagSearchResult;
import com.thaiautoparts.entity.Company;
import com.thaiautoparts.entity.Product;
import com.thaiautoparts.repository.CompanyMapper;
import com.thaiautoparts.repository.ProductMapper;
import com.thaiautoparts.service.AiRagService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import jakarta.annotation.PostConstruct;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

/**
 * RAG 服务实现
 * 简单的内存向量存储和检索（基于词频相似度）
 * 可扩展为使用专业向量数据库（Milvus、Pinecone、pgvector等）
 */
@Slf4j
@Service
public class AiRagServiceImpl implements AiRagService {

    private final CompanyMapper companyMapper;
    private final ProductMapper productMapper;

    private final Map<String, RagDocument> documentMap = new ConcurrentHashMap<>();
    private final Map<String, Map<String, Integer>> wordIndex = new ConcurrentHashMap<>();

    public AiRagServiceImpl(CompanyMapper companyMapper, ProductMapper productMapper) {
        this.companyMapper = companyMapper;
        this.productMapper = productMapper;
    }

    @PostConstruct
    public void init() {
        log.info("RAG service initialized with in-memory storage");
    }

    @Override
    public void addDocument(String content, String source, String sourceId) {
        String id = UUID.randomUUID().toString();
        RagDocument doc = new RagDocument();
        doc.setId(id);
        doc.setContent(content);
        doc.setSource(source);
        doc.setSourceId(sourceId);

        // 构建词索引
        Map<String, Integer> words = tokenizeAndCount(content.toLowerCase());
        wordIndex.put(id, words);
        documentMap.put(id, doc);

        log.info("Document added to RAG: id={}, source={}, contentLength={}", id, source, content.length());
    }

    @Override
    public void indexCompany(Long companyId) {
        Company company = companyMapper.selectById(companyId);
        if (company == null) {
            log.warn("Company not found for indexing: {}", companyId);
            return;
        }

        StringBuilder content = new StringBuilder();
        content.append("公司信息：");
        if (company.getCompanyName() != null) content.append("名称：").append(company.getCompanyName()).append("；");
        if (company.getCompanyNameTh() != null) content.append("泰文名：").append(company.getCompanyNameTh()).append("；");
        if (company.getCompanyNameEn() != null) content.append("英文名：").append(company.getCompanyNameEn()).append("；");
        if (company.getCountry() != null) content.append("国家：").append(company.getCountry()).append("；");
        if (company.getAddress() != null) content.append("地址：").append(company.getAddress()).append("；");
        if (company.getPhone() != null) content.append("电话：").append(company.getPhone()).append("；");
        if (company.getEmail() != null) content.append("邮箱：").append(company.getEmail()).append("；");
        if (company.getWebsite() != null) content.append("网站：").append(company.getWebsite()).append("；");
        if (company.getWhatsapp() != null) content.append("WhatsApp：").append(company.getWhatsapp()).append("；");
        if (company.getLeadGrade() != null) content.append("等级：").append(company.getLeadGrade()).append("；");
        if (company.getCompanyType() != null) content.append("类型：").append(company.getCompanyType()).append("；");
        if (company.getDescription() != null) content.append("描述：").append(company.getDescription()).append("；");

        addDocument(content.toString(), "company", String.valueOf(company.getId()));
    }

    @Override
    public void indexProduct(Long productId) {
        Product product = productMapper.selectById(productId);
        if (product == null) {
            log.warn("Product not found for indexing: {}", productId);
            return;
        }

        StringBuilder content = new StringBuilder();
        content.append("产品信息：");
        if (product.getProductName() != null) content.append("名称：").append(product.getProductName()).append("；");
        if (product.getProductCode() != null) content.append("编码：").append(product.getProductCode()).append("；");
        if (product.getCategory() != null) content.append("类别：").append(product.getCategory()).append("；");
        if (product.getBrand() != null) content.append("品牌：").append(product.getBrand()).append("；");
        if (product.getSpecification() != null) content.append("规格：").append(product.getSpecification()).append("；");
        if (product.getUnitPrice() != null) content.append("单价：").append(product.getUnitPrice()).append("；");
        if (product.getDescription() != null) content.append("描述：").append(product.getDescription()).append("；");

        addDocument(content.toString(), "product", String.valueOf(product.getId()));
    }

    @Override
    public List<RagSearchResult> search(String query, int topK) {
        if (query == null || query.trim().isEmpty()) {
            return Collections.emptyList();
        }

        try {
            // 对查询进行分词和词频统计
            Map<String, Integer> queryWords = tokenizeAndCount(query.toLowerCase());

            // 计算与每个文档的相似度
            List<ScoredDocument> scored = new ArrayList<>();
            for (Map.Entry<String, RagDocument> entry : documentMap.entrySet()) {
                String docId = entry.getKey();
                RagDocument doc = entry.getValue();
                Map<String, Integer> docWords = wordIndex.get(docId);

                if (docWords == null) continue;

                double score = cosineSimilarity(queryWords, docWords);
                scored.add(new ScoredDocument(doc, score));
            }

            // 按相似度排序
            scored.sort((a, b) -> Double.compare(b.score, a.score));

            // 返回 topK 结果
            return scored.stream()
                    .limit(topK)
                    .map(sd -> {
                        RagSearchResult result = new RagSearchResult();
                        result.setContent(sd.doc.getContent());
                        result.setSource(sd.doc.getSource());
                        result.setSourceId(sd.doc.getSourceId());
                        result.setScore(sd.score);
                        return result;
                    })
                    .collect(Collectors.toList());
        } catch (Exception e) {
            log.error("RAG search failed: {}", e.getMessage(), e);
            return Collections.emptyList();
        }
    }

    @Override
    public void clear() {
        wordIndex.clear();
        documentMap.clear();
        log.info("RAG knowledge base cleared");
    }

    @Override
    public int getDocumentCount() {
        return documentMap.size();
    }

    /**
     * 简单的中文分词（基于字符 n-gram 和空格）
     */
    private Map<String, Integer> tokenizeAndCount(String text) {
        Map<String, Integer> wordCount = new HashMap<>();

        // 简单的中文字符分词（2-gram）
        for (int i = 0; i < text.length() - 1; i++) {
            String word = text.substring(i, i + 2);
            wordCount.merge(word, 1, Integer::sum);
        }

        // 英文单词分词
        String[] englishWords = text.split("[\\u4e00-\\u9fa5\\s，。、；：！？\"\"''（）《》【】『』「」,.;:!?'\"()\\[\\]{}]+");
        for (String word : englishWords) {
            if (!word.isEmpty()) {
                wordCount.merge(word.toLowerCase(), 1, Integer::sum);
            }
        }

        return wordCount;
    }

    /**
     * 计算余弦相似度
     */
    private double cosineSimilarity(Map<String, Integer> vec1, Map<String, Integer> vec2) {
        // 计算交集词的词频
        Set<String> commonWords = new HashSet<>(vec1.keySet());
        commonWords.retainAll(vec2.keySet());

        if (commonWords.isEmpty()) {
            return 0.0;
        }

        // 计算点积
        double dotProduct = 0.0;
        for (String word : commonWords) {
            dotProduct += vec1.get(word) * vec2.get(word);
        }

        // 计算模长
        double norm1 = Math.sqrt(vec1.values().stream().mapToInt(v -> v * v).sum());
        double norm2 = Math.sqrt(vec2.values().stream().mapToInt(v -> v * v).sum());

        if (norm1 == 0 || norm2 == 0) {
            return 0.0;
        }

        return dotProduct / (norm1 * norm2);
    }

    private static class ScoredDocument {
        RagDocument doc;
        double score;

        ScoredDocument(RagDocument doc, double score) {
            this.doc = doc;
            this.score = score;
        }
    }
}
