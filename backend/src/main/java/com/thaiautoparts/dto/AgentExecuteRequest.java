package com.thaiautoparts.dto;

import lombok.Data;

@Data
public class AgentExecuteRequest {
    private String agentType;
    private String input;
    private String config;
}
