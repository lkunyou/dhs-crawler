package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("ai_model_config")
public class AiModelConfig {
    @TableId(type = IdType.AUTO)
    private Long id;
    
    private String provider;
    
    private String modelName;
    
    private String apiEndpoint;
    
    private String apiKey;
    
    private String baseUrl;
    
    private Boolean enabled;
    
    private Integer sortOrder;
    
    private String description;
    
    @TableField(fill = FieldFill.INSERT)
    private LocalDateTime createdAt;
    
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private LocalDateTime updatedAt;
}
