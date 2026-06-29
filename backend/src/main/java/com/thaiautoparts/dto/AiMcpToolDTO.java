package com.thaiautoparts.dto;

import lombok.Data;

@Data
public class AiMcpToolDTO {
    private Long id;
    private String name;
    private String description;
    private String toolType;
    private String endpoint;
    private String config;
    private String capabilities;
    private Boolean enabled;
}
