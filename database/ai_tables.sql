-- AI 对话系统数据库表
-- 运行此脚本以创建所需的数据库表

USE thai_auto_parts;

-- AI 对话会话表
CREATE TABLE IF NOT EXISTS ai_conversation (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    model VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- AI 消息表
CREATE TABLE IF NOT EXISTS ai_message (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    conversation_id BIGINT,
    role VARCHAR(50),
    content TEXT,
    model VARCHAR(100),
    agent_type VARCHAR(100),
    mcp_tool VARCHAR(100),
    mcp_result TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES ai_conversation(id) ON DELETE CASCADE
);

-- AI Skill 表
CREATE TABLE IF NOT EXISTS ai_skill (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type VARCHAR(50),
    config TEXT,
    enabled BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- AI Agent 任务表
CREATE TABLE IF NOT EXISTS ai_agent_task (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    task_id VARCHAR(100) UNIQUE NOT NULL,
    agent_type VARCHAR(100),
    input TEXT,
    status VARCHAR(50),
    result TEXT,
    error_message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- AI Agent 配置表
CREATE TABLE IF NOT EXISTS ai_agent (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    agent_type VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    prompt TEXT,
    config TEXT,
    enabled BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- AI MCP 工具表
CREATE TABLE IF NOT EXISTS ai_mcp_tool (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    tool_type VARCHAR(50),
    endpoint VARCHAR(500),
    config TEXT,
    capabilities TEXT,
    enabled BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 插入默认 Agent 配置
INSERT INTO ai_agent (agent_type, name, description, prompt, enabled) VALUES
('code_assistant', '代码助手', '帮助编写和审查代码的 AI 助手', '你是一个专业的代码助手，擅长编写、审查和优化代码。', TRUE),
('data_analyst', '数据分析', '帮助分析数据和生成报告', '你是一个专业的数据分析师，擅长数据分析、可视化和报告生成。', TRUE),
('customer_service', '客服助手', '处理客户咨询和问题的 AI 助手', '你是一个专业的客服助手，擅长回答客户问题和处理咨询。', TRUE),
('general', '通用助手', '处理各种任务的通用 AI 助手', '你是一个智能助手，可以帮助用户完成各种任务。', TRUE)
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- 插入示例 MCP 工具配置
INSERT INTO ai_mcp_tool (name, description, tool_type, endpoint, capabilities, enabled) VALUES
('web_search', '网络搜索', 'http', 'https://api.example.com/search', '["search", "find"]', TRUE),
('database_query', '数据库查询', 'database', 'jdbc:mysql://localhost:3306/thai_auto_parts', '["query", "select"]', TRUE),
('file_operations', '文件操作', 'file', '/data/uploads', '["read", "write", "delete"]', TRUE)
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- AI 模型配置表
CREATE TABLE IF NOT EXISTS ai_model_config (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    provider VARCHAR(100) NOT NULL COMMENT '模型提供商',
    model_name VARCHAR(100) NOT NULL COMMENT '模型名称',
    api_endpoint VARCHAR(255) COMMENT 'API端点',
    api_key VARCHAR(500) COMMENT 'API密钥',
    base_url VARCHAR(255) COMMENT 'API基础地址',
    enabled BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    sort_order INT DEFAULT 0 COMMENT '排序',
    description TEXT COMMENT '描述',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 插入默认 AI 模型配置
INSERT INTO ai_model_config (provider, model_name, base_url, api_endpoint, description, sort_order, enabled) VALUES
('deepseek', 'deepseek-chat', 'https://api.deepseek.com', '/chat/completions', '深度求索 AI 助手', 1, FALSE),
('kimi', 'moonshot-v1-8k', 'https://api.moonshot.cn/v1', '/chat/completions', '月之暗面 AI 助手', 2, FALSE),
('glm', 'glm-4', 'https://open.bigmodel.cn/api/paas/v4', '/chat/completions', '智谱 AI 大模型', 3, FALSE),
('doubao', 'doubao-pro-32k', 'https://ark.cn-beijing.volces.com/api/v3', '/chat/completions', '字节跳动豆包', 4, FALSE),
('qwen', 'qwen-plus', 'https://dashscope.aliyuncs.com/compatible-mode/v1', '/chat/completions', '阿里云通义千问', 5, FALSE),
('minimax', 'abab6-chat', 'https://api.minimax.chat/v1', '/chat/completions', '稀宇科技 MiniMax', 6, FALSE),
('openai', 'gpt-4', 'https://api.openai.com/v1', '/chat/completions', 'OpenAI GPT-4', 7, FALSE),
('claude', 'claude-3-sonnet-20240229', 'https://api.anthropic.com/v1', '/messages', 'Anthropic Claude', 8, FALSE)
ON DUPLICATE KEY UPDATE provider = VALUES(provider);

-- 插入 AI 配置类型到系统配置表（如果表存在）
INSERT INTO p_system_config (config_key, config_value, config_type, description) VALUES
('ai.default-provider', 'deepseek', 'ai', '默认AI模型提供商'),
('ai.deepseek.api-key', '', 'ai', 'DeepSeek API密钥'),
('ai.kimi.api-key', '', 'ai', 'Kimi API密钥'),
('ai.glm.api-key', '', 'ai', '智谱GLM API密钥'),
('ai.doubao.api-key', '', 'ai', '豆包Doubao API密钥'),
('ai.qwen.api-key', '', 'ai', '通义千问Qwen API密钥'),
('ai.minimax.api-key', '', 'ai', 'MiniMax API密钥')
ON DUPLICATE KEY UPDATE config_type = 'ai';

-- AI Agent 工作流表
CREATE TABLE IF NOT EXISTS ai_agent_workflow (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL COMMENT '工作流名称',
    description TEXT COMMENT '工作流描述',
    agent_type VARCHAR(100) COMMENT '关联Agent类型',
    steps TEXT COMMENT '步骤定义JSON',
    edges TEXT COMMENT '连线定义JSON',
    variables TEXT COMMENT '变量定义JSON',
    timeout INT DEFAULT 300 COMMENT '超时时间(秒)',
    enabled BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- AI Agent 工作流执行记录表
CREATE TABLE IF NOT EXISTS ai_agent_workflow_exec (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    workflow_id VARCHAR(100) NOT NULL COMMENT '工作流ID',
    status VARCHAR(50) DEFAULT 'pending' COMMENT '状态:pending/running/completed/failed/stopped',
    input TEXT COMMENT '输入参数JSON',
    output TEXT COMMENT '输出结果JSON',
    error_message TEXT COMMENT '错误信息',
    current_step INT DEFAULT 0 COMMENT '当前步骤',
    started_at DATETIME COMMENT '开始时间',
    completed_at DATETIME COMMENT '完成时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 插入示例工作流
INSERT INTO ai_agent_workflow (name, description, agent_type, steps, timeout, enabled) VALUES
('客户开发流程', '自动执行客户开发和邮件发送流程', 'general', 
 '[{"order":1,"name":"获取客户列表","type":"agent","config":"{}","nextStep":""},{"order":2,"name":"分析客户需求","type":"mcp","config":"{}","nextStep":""},{"order":3,"name":"生成开发信","type":"agent","config":"{}","nextStep":""},{"order":4,"name":"发送邮件","type":"mcp","config":"{}","nextStep":""}]',
 600, TRUE),
('数据采集流程', '自动从多个数据源采集数据', 'data_analyst',
 '[{"order":1,"name":"网络搜索","type":"mcp","config":"{}","nextStep":""},{"order":2,"name":"数据清洗","type":"agent","config":"{}","nextStep":""},{"order":3,"name":"数据存储","type":"mcp","config":"{}","nextStep":""}]',
 300, TRUE)
ON DUPLICATE KEY UPDATE name = VALUES(name);
