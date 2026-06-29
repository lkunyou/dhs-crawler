package com.thaiautoparts.service;

import com.thaiautoparts.dto.RagDocument;
import com.thaiautoparts.dto.RagSearchResult;

import java.util.List;

/**
 * RAG（检索增强生成）服务接口
 */
public interface AiRagService {

    /**
     * 将文本内容添加到知识库
     */
    void addDocument(String content, String source, String sourceId);

    /**
     * 将公司数据添加到知识库
     */
    void indexCompany(Long companyId);

    /**
     * 将产品数据添加到知识库
     */
    void indexProduct(Long productId);

    /**
     * 搜索知识库
     * @param query 查询文本
     * @param topK 返回前k个结果
     * @return 搜索结果列表
     */
    List<RagSearchResult> search(String query, int topK);

    /**
     * 清空知识库
     */
    void clear();

    /**
     * 获取知识库文档数量
     */
    int getDocumentCount();
}
