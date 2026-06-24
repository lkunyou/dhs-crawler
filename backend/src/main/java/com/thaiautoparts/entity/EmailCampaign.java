package com.thaiautoparts.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@TableName("p_email_campaign")
public class EmailCampaign {
    @TableId(type = IdType.AUTO)
    private Long id;
    private String campaignName;
    private String campaignType;
    private String status;
    private Integer totalRecipients;
    private Integer sentCount;
    private Integer openedCount;
    private Integer repliedCount;
    private Integer bouncedCount;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private LocalDateTime startedAt;
    private LocalDateTime completedAt;
}
