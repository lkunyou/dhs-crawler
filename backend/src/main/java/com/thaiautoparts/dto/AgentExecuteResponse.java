package com.thaiautoparts.dto;

import lombok.Data;

@Data
public class AgentExecuteResponse {
    private String taskId;
    private String status;
    private String result;
    private String errorMessage;
}
