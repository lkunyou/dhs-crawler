package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("p_product_interest")
public class ProductInterest {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long companyId;
    private String productCategory;
    private String productName;
    private String interestLevel;
    private String source;
    private String notes;
    private LocalDateTime createdAt;
}
