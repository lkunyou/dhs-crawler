package com.thaiautoparts.dto;

import lombok.Data;

@Data
public class AiSkillDTO {
    private Long id;
    private String name;
    private String description;
    private String type;
    private String config;
    private Boolean enabled;
}
