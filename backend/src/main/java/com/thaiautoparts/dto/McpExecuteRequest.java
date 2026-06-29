package com.thaiautoparts.dto;

import lombok.Data;

@Data
public class McpExecuteRequest {
    private Long toolId;
    private String toolName;
    private String parameters;
}
