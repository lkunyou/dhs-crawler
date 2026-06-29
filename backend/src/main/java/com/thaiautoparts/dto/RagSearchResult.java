package com.thaiautoparts.dto;

import lombok.Data;

/**
 * RAG 搜索结果
 */
@Data
public class RagSearchResult {
    private String content;
    private String source;
    private String sourceId;
    private double score;        // 相似度分数
}
