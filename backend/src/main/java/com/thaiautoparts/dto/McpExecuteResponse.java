package com.thaiautoparts.dto;

import lombok.Data;

@Data
public class McpExecuteResponse {
    private String result;
    private String error;
    private Long toolId;
    private String toolName;
}
