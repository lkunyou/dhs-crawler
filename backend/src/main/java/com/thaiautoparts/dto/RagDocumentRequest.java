package com.thaiautoparts.dto;

import lombok.Data;

/**
 * RAG 文档请求
 */
@Data
public class RagDocumentRequest {
    private String content;     // 文档内容
    private String source;     // 来源类型
    private String sourceId;   // 来源ID
}
