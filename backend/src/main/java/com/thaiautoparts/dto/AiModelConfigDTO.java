package com.thaiautoparts.dto;

import lombok.Data;

@Data
public class AiModelConfigDTO {
    private Long id;
    private String provider;
    private String modelName;
    private String apiEndpoint;
    private String apiKey;
    private String baseUrl;
    private Boolean enabled;
    private Integer sortOrder;
    private String description;
}
