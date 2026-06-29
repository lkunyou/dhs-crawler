package com.thaiautoparts.dto;

import lombok.Data;

@Data
public class AiAgentDTO {
    private Long id;
    private String agentType;
    private String name;
    private String description;
    private String prompt;
    private String config;
    private Boolean enabled;
}
