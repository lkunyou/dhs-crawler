package com.thaiautoparts.dto;

import lombok.Data;

/**
 * RAG 文档
 */
@Data
public class RagDocument {
    private String id;
    private String content;
    private String source;      // 来源类型：company, product, manual
    private String sourceId;    // 来源ID
}
