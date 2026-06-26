package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@TableName("p_cmdt_code")
public class CmdtCode {

    @TableId(value = "id", type = IdType.AUTO)
    private Long id;

    @TableField("section")
    private String section;

    @TableField("section_code")
    private String sectionCode;

    @TableField("chapter")
    private String chapter;

    @TableField("chapter_code")
    private String chapterCode;

    @TableField("cmdt_code")
    private String cmdtCode;

    @TableField("description_en")
    private String descriptionEn;

    @TableField("description_cn")
    private String descriptionCn;

    @TableField("created_at")
    private LocalDateTime createdAt;

    @TableField("updated_at")
    private LocalDateTime updatedAt;
}