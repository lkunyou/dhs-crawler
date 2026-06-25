-- ============================================
-- 泰国汽配B2B获客系统 - 数据库设计
-- Database: thai_auto_parts_crm
-- ============================================

CREATE DATABASE IF NOT EXISTS thai_auto_parts_crm DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE thai_auto_parts_crm;

-- ============================================
-- 1. 客户公司表 (核心表)
-- ============================================
CREATE TABLE `p_company` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `company_name` VARCHAR(255) NOT NULL COMMENT '公司名称',
    `company_name_th` VARCHAR(255) COMMENT '公司名称(泰文)',
    `company_name_en` VARCHAR(255) COMMENT '公司名称(英文)',
    `country` VARCHAR(50) DEFAULT 'Thailand' COMMENT '国家',
    `company_type` ENUM('Distributor', 'Importer', 'OEM', 'Retailer', 'Manufacturer', 'Other') COMMENT '公司类型',
    `website` VARCHAR(255) COMMENT '官网URL',
    `address` VARCHAR(500) COMMENT '详细地址',
    `city` VARCHAR(100) COMMENT '城市',
    `province` VARCHAR(100) COMMENT '省份',
    `phone` VARCHAR(50) COMMENT '电话',
    `whatsapp` VARCHAR(50) COMMENT 'WhatsApp号码',
    `email` VARCHAR(100) COMMENT '公司邮箱',
    
    -- 评分相关
    `lead_score` INT DEFAULT 0 COMMENT '客户评分(0-100)',
    `lead_grade` ENUM('S', 'A', 'B', 'C') DEFAULT 'C' COMMENT '客户等级',
    `score_details` JSON COMMENT '评分明细JSON',
    
    -- 业务特征
    `is_auto_parts_core` BOOLEAN DEFAULT FALSE COMMENT '是否汽配核心业务',
    `is_importer_distributor` BOOLEAN DEFAULT FALSE COMMENT '是否进口/分销商',
    `has_oem_cooperation` BOOLEAN DEFAULT FALSE COMMENT '是否有OEM合作',
    `employee_count` VARCHAR(50) COMMENT '员工规模',
    `website_completeness` INT DEFAULT 0 COMMENT '官网完整度(0-100)',
    
    -- 来源追踪
    `source` ENUM('Google', 'LinkedIn', 'B2B_Platform', 'Industry_Directory', 'Manual', 'API') COMMENT '数据来源',
    `source_url` VARCHAR(500) COMMENT '来源URL',
    `raw_data` JSON COMMENT '原始数据JSON',
    
    -- 状态管理
    `status` ENUM('New', 'Contacted', 'Replied', 'Quoted', 'Negotiation', 'Sample_Sent', 'Won', 'Lost', 'Invalid') DEFAULT 'New' COMMENT '客户状态',
    `is_duplicate` BOOLEAN DEFAULT FALSE COMMENT '是否重复',
    `duplicate_of` BIGINT COMMENT '重复指向的公司ID',
    `assigned_to` BIGINT COMMENT '分配给的销售人员ID',
    
    -- 时间戳
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    `last_contacted_at` DATETIME COMMENT '最后联系时间',
    
    INDEX `idx_company_name` (`company_name`),
    INDEX `idx_lead_grade` (`lead_grade`),
    INDEX `idx_status` (`status`),
    INDEX `idx_source` (`source`),
    INDEX `idx_country_city` (`country`, `city`),
    UNIQUE KEY `uk_company_name_country` (`company_name`, `country`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='客户公司表';

-- ============================================
-- 2. 联系人表 (决策人信息)
-- ============================================
CREATE TABLE `p_contact_person` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '主键ID',
    `company_id` BIGINT NOT NULL COMMENT '所属公司ID',
    `first_name` VARCHAR(100) COMMENT '名',
    `last_name` VARCHAR(100) COMMENT '姓',
    `full_name` VARCHAR(200) COMMENT '全名',
    `name_th` VARCHAR(200) COMMENT '泰文名',
    
    -- 职位信息
    `job_title` VARCHAR(200) COMMENT '职位',
    `department` VARCHAR(100) COMMENT '部门',
    `is_decision_maker` BOOLEAN DEFAULT FALSE COMMENT '是否决策人',
    `seniority_level` ENUM('C-Level', 'VP', 'Director', 'Manager', 'Staff', 'Other') COMMENT '职级',
    
    -- 联系方式
    `email` VARCHAR(100) COMMENT '个人邮箱',
    `email_verified` BOOLEAN DEFAULT FALSE COMMENT '邮箱是否验证',
    `phone` VARCHAR(50) COMMENT '电话',
    `whatsapp` VARCHAR(50) COMMENT 'WhatsApp',
    `linkedin_url` VARCHAR(500) COMMENT 'LinkedIn主页',
    
    -- 互动信息
    `last_contacted_at` DATETIME COMMENT '最后联系时间',
    `contact_count` INT DEFAULT 0 COMMENT '联系次数',
    `reply_count` INT DEFAULT 0 COMMENT '回复次数',
    `notes` TEXT COMMENT '备注',
    
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (`company_id`) REFERENCES `p_company`(`id`) ON DELETE CASCADE,
    INDEX `idx_company_id` (`company_id`),
    INDEX `idx_job_title` (`job_title`),
    INDEX `idx_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='联系人表';

-- ============================================
-- 3. 产品兴趣表
-- ============================================
CREATE TABLE `p_product_interest` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `company_id` BIGINT NOT NULL,
    `product_category` ENUM('Exterior', 'Interior', 'Structural', 'Electrical', 'Engine', 'Suspension', 'Brake', 'Lighting', 'Mirror', 'Grille', 'Bumper', 'Other') COMMENT '产品类别',
    `product_name` VARCHAR(200) COMMENT '具体产品名称',
    `interest_level` ENUM('High', 'Medium', 'Low') DEFAULT 'Medium' COMMENT '兴趣程度',
    `source` VARCHAR(200) COMMENT '来源(从什么渠道得知)',
    `notes` TEXT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (`company_id`) REFERENCES `p_company`(`id`) ON DELETE CASCADE,
    INDEX `idx_company_id` (`company_id`),
    INDEX `idx_product_category` (`product_category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='产品兴趣表';

-- ============================================
-- 4. 邮件发送记录表
-- ============================================
CREATE TABLE `p_email_campaign` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '活动ID',
    `campaign_name` VARCHAR(200) NOT NULL COMMENT '活动名称',
    `campaign_type` ENUM('Cold_Outreach', 'Follow_Up', 'Product_Promo', 'Quote', 'Reactivation') COMMENT '活动类型',
    `status` ENUM('Draft', 'Active', 'Paused', 'Completed', 'Cancelled') DEFAULT 'Draft' COMMENT '状态',
    `total_recipients` INT DEFAULT 0 COMMENT '总收件人数',
    `sent_count` INT DEFAULT 0 COMMENT '已发送数',
    `opened_count` INT DEFAULT 0 COMMENT '打开数',
    `replied_count` INT DEFAULT 0 COMMENT '回复数',
    `bounced_count` INT DEFAULT 0 COMMENT '退信数',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    `started_at` DATETIME COMMENT '开始时间',
    `completed_at` DATETIME COMMENT '完成时间',
    
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='邮件活动表';

CREATE TABLE `p_email_template` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `template_name` VARCHAR(200) NOT NULL COMMENT '模板名称',
    `subject` VARCHAR(300) NOT NULL COMMENT '邮件主题',
    `content` TEXT NOT NULL COMMENT '邮件内容(HTML)',
    `language` ENUM('EN', 'TH', 'ZH') DEFAULT 'EN' COMMENT '语言',
    `category` VARCHAR(100) COMMENT '分类',
    `day_sequence` INT COMMENT '发送序列(第几天)',
    `is_active` BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    `open_rate` DECIMAL(5,2) DEFAULT 0 COMMENT '打开率',
    `reply_rate` DECIMAL(5,2) DEFAULT 0 COMMENT '回复率',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX `idx_category` (`category`),
    INDEX `idx_language` (`language`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='邮件模板表';

CREATE TABLE `p_email_record` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `campaign_id` BIGINT COMMENT '活动ID',
    `company_id` BIGINT NOT NULL COMMENT '公司ID',
    `contact_id` BIGINT COMMENT '联系人ID',
    `template_id` BIGINT COMMENT '模板ID',
    `recipient_email` VARCHAR(100) NOT NULL COMMENT '收件人邮箱',
    `subject` VARCHAR(300) COMMENT '邮件主题',
    `content` TEXT COMMENT '邮件内容',
    
    -- 状态追踪
    `status` ENUM('Pending', 'Sent', 'Delivered', 'Opened', 'Replied', 'Bounced', 'Failed') DEFAULT 'Pending' COMMENT '状态',
    `sent_at` DATETIME COMMENT '发送时间',
    `opened_at` DATETIME COMMENT '打开时间',
    `replied_at` DATETIME COMMENT '回复时间',
    `reply_content` TEXT COMMENT '回复内容',
    `error_message` TEXT COMMENT '错误信息',
    
    -- 追踪参数
    `tracking_id` VARCHAR(100) COMMENT '追踪ID',
    `message_id` VARCHAR(200) COMMENT '邮件服务器Message-ID',
    
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (`company_id`) REFERENCES `p_company`(`id`),
    INDEX `idx_campaign_id` (`campaign_id`),
    INDEX `idx_company_id` (`company_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_tracking_id` (`tracking_id`),
    INDEX `idx_sent_at` (`sent_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='邮件发送记录表';

-- ============================================
-- 5. WhatsApp消息记录表
-- ============================================
CREATE TABLE `p_whatsapp_record` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `company_id` BIGINT NOT NULL,
    `contact_id` BIGINT,
    `phone_number` VARCHAR(50) NOT NULL COMMENT '收件人号码',
    `message_type` ENUM('Text', 'Image', 'Document', 'Video', 'Audio') DEFAULT 'Text' COMMENT '消息类型',
    `content` TEXT COMMENT '文本内容',
    `media_url` VARCHAR(500) COMMENT '媒体文件URL',
    
    `direction` ENUM('Outbound', 'Inbound') COMMENT '方向',
    `status` ENUM('Pending', 'Sent', 'Delivered', 'Read', 'Replied', 'Failed') DEFAULT 'Pending' COMMENT '状态',
    
    `sent_at` DATETIME COMMENT '发送时间',
    `delivered_at` DATETIME COMMENT '送达时间',
    `read_at` DATETIME COMMENT '已读时间',
    `replied_at` DATETIME COMMENT '回复时间',
    `reply_content` TEXT COMMENT '回复内容',
    `error_message` TEXT,
    
    `message_id` VARCHAR(200) COMMENT 'WA消息ID',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (`company_id`) REFERENCES `p_company`(`id`),
    INDEX `idx_company_id` (`company_id`),
    INDEX `idx_phone_number` (`phone_number`),
    INDEX `idx_status` (`status`),
    INDEX `idx_sent_at` (`sent_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='WhatsApp消息记录表';

-- ============================================
-- 6. LinkedIn互动记录表
-- ============================================
CREATE TABLE `p_linkedin_record` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `company_id` BIGINT NOT NULL,
    `contact_id` BIGINT,
    `linkedin_profile_url` VARCHAR(500) COMMENT 'LinkedIn主页',
    `linkedin_id` VARCHAR(100) COMMENT 'LinkedIn用户ID',
    
    `action_type` ENUM('View_Profile', 'Connect', 'Message', 'Follow', 'Engage_Post') COMMENT '操作类型',
    `status` ENUM('Pending', 'Success', 'Failed', 'Ignored', 'Blocked') DEFAULT 'Pending' COMMENT '状态',
    
    `message_content` TEXT COMMENT '消息内容',
    `response_content` TEXT COMMENT '回复内容',
    
    `scheduled_at` DATETIME COMMENT '计划执行时间',
    `executed_at` DATETIME COMMENT '执行时间',
    `error_message` TEXT,
    
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (`company_id`) REFERENCES `p_company`(`id`),
    INDEX `idx_company_id` (`company_id`),
    INDEX `idx_action_type` (`action_type`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='LinkedIn互动记录表';

-- ============================================
-- 7. 跟进记录表 (CRM核心)
-- ============================================
CREATE TABLE `p_follow_up_record` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `company_id` BIGINT NOT NULL,
    `contact_id` BIGINT,
    
    `follow_up_type` ENUM('Email', 'WhatsApp', 'LinkedIn', 'Phone', 'Meeting', 'Sample', 'Quote', 'Other') COMMENT '跟进方式',
    `direction` ENUM('Outbound', 'Inbound') COMMENT '方向',
    
    `summary` VARCHAR(500) COMMENT '跟进摘要',
    `detail` TEXT COMMENT '详细内容',
    `next_action` VARCHAR(500) COMMENT '下一步行动',
    `next_action_date` DATE COMMENT '下次行动日期',
    
    `outcome` ENUM('Positive', 'Neutral', 'Negative', 'No_Response', 'Invalid_Contact') COMMENT '结果',
    `sentiment` ENUM('Positive', 'Neutral', 'Negative') COMMENT '客户情绪',
    
    `attachments` JSON COMMENT '附件列表',
    
    `created_by` BIGINT COMMENT '创建人',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (`company_id`) REFERENCES `p_company`(`id`) ON DELETE CASCADE,
    INDEX `idx_company_id` (`company_id`),
    INDEX `idx_follow_up_type` (`follow_up_type`),
    INDEX `idx_created_at` (`created_at`),
    INDEX `idx_next_action_date` (`next_action_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='跟进记录表';

-- ============================================
-- 8. 任务/提醒表
-- ============================================
CREATE TABLE `p_task` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `company_id` BIGINT,
    `contact_id` BIGINT,
    `assigned_to` BIGINT NOT NULL COMMENT '负责人',
    
    `task_type` ENUM('Follow_Up', 'Send_Quote', 'Send_Sample', 'Call', 'Meeting', 'Other') COMMENT '任务类型',
    `title` VARCHAR(200) NOT NULL COMMENT '任务标题',
    `description` TEXT COMMENT '任务描述',
    `priority` ENUM('High', 'Medium', 'Low') DEFAULT 'Medium' COMMENT '优先级',
    
    `status` ENUM('Pending', 'In_Progress', 'Completed', 'Cancelled') DEFAULT 'Pending' COMMENT '状态',
    `due_date` DATETIME COMMENT '截止日期',
    `completed_at` DATETIME COMMENT '完成时间',
    
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (`company_id`) REFERENCES `p_company`(`id`),
    INDEX `idx_assigned_to` (`assigned_to`),
    INDEX `idx_status` (`status`),
    INDEX `idx_due_date` (`due_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='任务表';

-- ============================================
-- 9. 报价单表
-- ============================================
CREATE TABLE `p_quotation` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `company_id` BIGINT NOT NULL,
    `contact_id` BIGINT,
    `quotation_no` VARCHAR(50) NOT NULL UNIQUE COMMENT '报价单号',
    
    `product_name` VARCHAR(200) COMMENT '产品名称',
    `product_description` TEXT COMMENT '产品描述',
    `quantity` INT COMMENT '数量',
    `unit_price` DECIMAL(10,2) COMMENT '单价(USD)',
    `total_amount` DECIMAL(12,2) COMMENT '总金额',
    `currency` VARCHAR(10) DEFAULT 'USD' COMMENT '货币',
    
    `valid_until` DATE COMMENT '有效期至',
    `terms` TEXT COMMENT '条款',
    `notes` TEXT COMMENT '备注',
    
    `status` ENUM('Draft', 'Sent', 'Viewed', 'Negotiating', 'Accepted', 'Rejected', 'Expired') DEFAULT 'Draft' COMMENT '状态',
    `sent_at` DATETIME COMMENT '发送时间',
    `viewed_at` DATETIME COMMENT '查看时间',
    `accepted_at` DATETIME COMMENT '接受时间',
    
    `attachments` JSON COMMENT '附件(报价单PDF等)',
    `created_by` BIGINT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (`company_id`) REFERENCES `p_company`(`id`),
    INDEX `idx_company_id` (`company_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_quotation_no` (`quotation_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='报价单表';

-- ============================================
-- 10. 爬虫任务表
-- ============================================
CREATE TABLE `p_crawler_task` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `task_name` VARCHAR(200) NOT NULL COMMENT '任务名称',
    `source_type` ENUM('Google_Search', 'Google_Maps', 'LinkedIn', 'B2B_Platform', 'Industry_Directory') COMMENT '数据源',
    
    `keywords` JSON COMMENT '搜索关键词列表',
    `target_country` VARCHAR(50) DEFAULT 'Thailand' COMMENT '目标国家',
    `target_city` VARCHAR(100) COMMENT '目标城市',
    `filters` JSON COMMENT '过滤条件',
    
    `status` ENUM('Pending', 'Running', 'Completed', 'Failed', 'Paused') DEFAULT 'Pending' COMMENT '状态',
    `progress` INT DEFAULT 0 COMMENT '进度(0-100)',
    
    `total_found` INT DEFAULT 0 COMMENT '发现总数',
    `new_companies` INT DEFAULT 0 COMMENT '新增公司数',
    `duplicates` INT DEFAULT 0 COMMENT '重复数',
    `errors` INT DEFAULT 0 COMMENT '错误数',
    
    `started_at` DATETIME COMMENT '开始时间',
    `completed_at` DATETIME COMMENT '完成时间',
    `error_message` TEXT,
    
    `created_by` BIGINT,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX `idx_source_type` (`source_type`),
    INDEX `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='爬虫任务表';

-- ============================================
-- 10.1 爬虫抓取结果表 (待确认的原始数据)
-- ============================================
CREATE TABLE `p_crawler_result` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `task_id` BIGINT NOT NULL COMMENT '爬虫任务ID',
    `source_type` ENUM('Google_Search', 'Google_Maps', 'LinkedIn', 'B2B_Platform', 'Industry_Directory') COMMENT '数据源',
    
    -- 公司基本信息
    `company_name` VARCHAR(255) NOT NULL COMMENT '公司名称',
    `company_name_th` VARCHAR(255) COMMENT '公司名称(泰文)',
    `company_name_en` VARCHAR(255) COMMENT '公司名称(英文)',
    `website` VARCHAR(500) COMMENT '官网URL',
    `address` VARCHAR(500) COMMENT '地址',
    `city` VARCHAR(100) COMMENT '城市',
    `province` VARCHAR(100) COMMENT '省份',
    `phone` VARCHAR(50) COMMENT '电话',
    `whatsapp` VARCHAR(50) COMMENT 'WhatsApp号码',
    `email` VARCHAR(100) COMMENT '邮箱',
    
    -- 业务信息
    `company_type` VARCHAR(100) COMMENT '公司类型',
    `business_description` TEXT COMMENT '业务描述',
    `product_categories` JSON COMMENT '产品类别',
    `employee_count` VARCHAR(50) COMMENT '员工规模',
    
    -- 来源信息
    `source_url` VARCHAR(500) COMMENT '来源URL',
    `search_keyword` VARCHAR(200) COMMENT '搜索关键词',
    `raw_data` JSON COMMENT '原始数据JSON',
    
    -- 状态管理
    `status` ENUM('Pending', 'Confirmed', 'Synced', 'Rejected', 'Duplicate') DEFAULT 'Pending' COMMENT '状态',
    `synced_company_id` BIGINT COMMENT '同步后的公司ID',
    `duplicate_of` BIGINT COMMENT '重复指向的公司ID',
    `rejection_reason` VARCHAR(500) COMMENT '拒绝原因',
    
    -- 评分
    `lead_score` INT DEFAULT 0 COMMENT '客户评分(0-100)',
    `lead_grade` ENUM('S', 'A', 'B', 'C') DEFAULT 'C' COMMENT '客户等级',
    `is_auto_parts_core` BOOLEAN DEFAULT FALSE COMMENT '是否汽配核心业务',
    `is_importer_distributor` BOOLEAN DEFAULT FALSE COMMENT '是否进口/分销商',
    
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `confirmed_at` DATETIME COMMENT '确认时间',
    `synced_at` DATETIME COMMENT '同步时间',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (`task_id`) REFERENCES `p_crawler_task`(`id`),
    INDEX `idx_task_id` (`task_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_source_type` (`source_type`),
    INDEX `idx_company_name` (`company_name`),
    INDEX `idx_lead_grade` (`lead_grade`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='爬虫抓取结果表(待确认)';

-- ============================================
-- 11. 数据统计表 (每日汇总)
-- ============================================
CREATE TABLE `p_daily_stats` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `stat_date` DATE NOT NULL UNIQUE COMMENT '统计日期',
    
    -- 获客数据
    `new_leads` INT DEFAULT 0 COMMENT '新增线索',
    `leads_by_source` JSON COMMENT '按来源分类',
    `leads_by_grade` JSON COMMENT '按等级分类',
    
    -- 触达数据
    `emails_sent` INT DEFAULT 0 COMMENT '邮件发送数',
    `emails_opened` INT DEFAULT 0 COMMENT '邮件打开数',
    `emails_replied` INT DEFAULT 0 COMMENT '邮件回复数',
    `whatsapp_sent` INT DEFAULT 0 COMMENT 'WA发送数',
    `whatsapp_replied` INT DEFAULT 0 COMMENT 'WA回复数',
    `linkedin_actions` INT DEFAULT 0 COMMENT 'LinkedIn操作数',
    
    -- 转化数据
    `new_replies` INT DEFAULT 0 COMMENT '新增回复',
    `new_quotations` INT DEFAULT 0 COMMENT '新增报价',
    `new_samples` INT DEFAULT 0 COMMENT '新增样品',
    `deals_won` INT DEFAULT 0 COMMENT '成交数',
    `deals_lost` INT DEFAULT 0 COMMENT '流失数',
    
    -- 转化率
    `email_open_rate` DECIMAL(5,2) DEFAULT 0 COMMENT '邮件打开率',
    `email_reply_rate` DECIMAL(5,2) DEFAULT 0 COMMENT '邮件回复率',
    `whatsapp_reply_rate` DECIMAL(5,2) DEFAULT 0 COMMENT 'WA回复率',
    `overall_conversion_rate` DECIMAL(5,2) DEFAULT 0 COMMENT '总体转化率',
    
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX `idx_stat_date` (`stat_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='每日统计表';

-- ============================================
-- 12. 系统配置表
-- ============================================
CREATE TABLE `p_system_config` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `config_key` VARCHAR(100) NOT NULL UNIQUE COMMENT '配置键',
    `config_value` TEXT COMMENT '配置值',
    `config_type` ENUM('String', 'Number', 'Boolean', 'JSON') DEFAULT 'String' COMMENT '值类型',
    `description` VARCHAR(500) COMMENT '描述',
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统配置表';

-- ============================================
-- 初始化系统配置
-- ============================================
INSERT INTO `p_system_config` (`config_key`, `config_value`, `config_type`, `description`) VALUES
('email_daily_limit', '100', 'Number', '每日邮件发送上限'),
('whatsapp_daily_limit', '50', 'Number', '每日WhatsApp发送上限'),
('linkedin_daily_limit', '100', 'Number', '每日LinkedIn操作上限'),
('lead_score_threshold_S', '80', 'Number', 'S级客户分数阈值'),
('lead_score_threshold_A', '60', 'Number', 'A级客户分数阈值'),
('lead_score_threshold_B', '40', 'Number', 'B级客户分数阈值'),
('email_follow_up_day_1', '3', 'Number', '邮件跟进间隔-第1次(天)'),
('email_follow_up_day_2', '6', 'Number', '邮件跟进间隔-第2次(天)'),
('email_follow_up_day_3', '10', 'Number', '邮件跟进间隔-第3次(天)'),
('email_follow_up_day_4', '15', 'Number', '邮件跟进间隔-第4次(天)');

-- ============================================
-- 初始化邮件模板（泰国汽配高回复率模板）
-- ============================================
INSERT INTO `p_email_template` (`template_name`, `subject`, `content`, `language`, `category`, `day_sequence`, `is_active`) VALUES
('Day1-公司介绍', 'Professional Auto Parts Manufacturer from China - [Your Company]', 
'<p>Dear [Name],</p>
<p>I hope this email finds you well.</p>
<p>I am writing to introduce [Your Company], a professional automotive parts manufacturer based in China with over [X] years of experience.</p>
<p><strong>Our main products include:</strong></p>
<ul>
<li>Exterior Parts: Bumpers, Grilles, Mirror Covers, Fenders</li>
<li>Interior Parts: Dashboards, Door Panels, Trim</li>
<li>Structural Parts: Body Panels, Frames</li>
</ul>
<p>We currently supply to distributors in Southeast Asia and would love to explore partnership opportunities with your company.</p>
<p>Would you be interested in receiving our product catalog and price list?</p>
<p>Best regards,<br/>[Your Name]<br/>[Your Title]<br/>[Company]<br/>WhatsApp: [Number]</p>',
'EN', 'Cold_Outreach', 1, TRUE),

('Day3-热销产品', 'Hot Selling Auto Parts for Thai Market - Special Offer',
'<p>Hi [Name],</p>
<p>Following up on my previous email, I wanted to share our best-selling products in the Thai market:</p>
<p><strong>Top Sellers:</strong></p>
<ul>
<li>Toyota Hilux Revo Mirror Covers (2015-2023)</li>
<li>Isuzu D-Max Front Grilles</li>
<li>Fortuner Bumper Assemblies</li>
</ul>
<p>These items have been very popular among Thai distributors due to competitive pricing and reliable quality.</p>
<p>Would you like me to send you a quotation for any of these products?</p>
<p>Best regards,<br/>[Your Name]</p>',
'EN', 'Product_Promo', 3, TRUE),

('Day6-OEM案例', 'OEM Partnership Success Story - How We Help Thai Distributors',
'<p>Dear [Name],</p>
<p>I thought you might be interested in learning about our OEM partnerships:</p>
<p>We currently work with several distributors in Thailand, providing:</p>
<ul>
<li>Custom branding & packaging</li>
<li>Private label manufacturing</li>
<li>Flexible MOQ (starting from 50 pcs)</li>
<li>Sample testing before bulk orders</li>
</ul>
<p>One of our Thai partners increased their profit margin by 35% after switching to our products.</p>
<p>Would you be open to a quick call to discuss how we can support your business?</p>
<p>Best regards,<br/>[Your Name]</p>',
'EN', 'OEM_Case', 6, TRUE),

('Day10-报价引导', 'Exclusive Price List - Auto Parts for Your Review',
'<p>Hi [Name],</p>
<p>I have prepared a special price list for your review.</p>
<p>As a valued potential partner, we can offer:</p>
<ul>
<li>10% discount on first order</li>
<li>Free samples (freight collect)</li>
<li>Flexible payment terms for regular orders</li>
<li>Priority production scheduling</li>
</ul>
<p>Please let me know which products you are most interested in, and I will prepare a detailed quotation for you.</p>
<p>Looking forward to your reply.</p>
<p>Best regards,<br/>[Your Name]</p>',
'EN', 'Quote', 10, TRUE),

('Day15-促销提醒', 'Limited-Time Promotion - Auto Parts Special Deal',
'<p>Dear [Name],</p>
<p>This is a friendly reminder about our current promotion:</p>
<p><strong>Special Offer (Valid until [Date]):</strong></p>
<ul>
<li>15% off on orders over $5,000</li>
<li>Free shipping for orders over $10,000</li>
<li>Buy 100 pcs, get 10 pcs free</li>
</ul>
<p>This is a great opportunity to stock up on popular items at discounted prices.</p>
<p>Please reply to this email or contact me on WhatsApp [Number] to take advantage of this offer.</p>
<p>Best regards,<br/>[Your Name]</p>',
'EN', 'Promotion', 15, TRUE);
