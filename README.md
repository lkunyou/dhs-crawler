# Thailand Auto Parts B2B Lead Generation System

## 系统概述

泰国汽配B2B获客系统 - 专为中国汽配工厂设计的全自动化外贸获客SaaS平台。

**核心目标**：自动找到泰国经销商/进口商/OEM供应链客户 → 自动筛选 → 自动触达 → 自动跟进 → 形成询盘

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    前端 (Vue3 + Element Plus)                │
│  客户管理 | 邮件营销 | WhatsApp | CRM跟进 | 数据分析         │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    后端 (Spring Boot 3.2)                    │
│  客户管理API | 邮件服务 | WhatsApp服务 | CRM服务 | 分析服务   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    爬虫层 (Python + Playwright)              │
│  Google搜索 | Google Maps | LinkedIn | B2B平台 | 行业目录    │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    数据存储 (MySQL + Redis)                  │
│  客户数据 | 跟进记录 | 邮件模板 | 消息记录 | 统计数据         │
└─────────────────────────────────────────────────────────────┘
```

## 功能模块

### 1. 客户获取 (Customer Acquisition)
- **Google搜索爬虫**：通过SerpAPI搜索泰国汽配公司
- **Google Maps爬虫**：抓取汽配商店/经销商地理位置信息
- **LinkedIn爬虫**：通过PhantomBuster抓取采购决策人
- **B2B平台爬虫**：ThaiTrade、Alibaba买家市场
- **行业目录爬虫**：TAPAA协会成员、Thai Yellow Pages

### 2. 客户识别 (Customer Identification)
- **智能评分模型**：100分制评分系统
  - 公司名称匹配度（20分）
  - 网站质量（15分）
  - 联系人职位（20分）
  - 公司规模（15分）
  - 地理位置（10分）
  - 产品匹配度（20分）
- **自动分级**：S级(≥85) / A级(70-84) / B级(50-69) / C级(<50)
- **去重机制**：基于公司名称+网站+电话的智能去重

### 3. 数据补全 (Data Completion)
- 自动搜索公司官网
- 提取联系人信息
- 补全邮箱/电话/地址
- 社交媒体账号关联

### 4. 自动触达 (Automatic Outreach)
- **邮件营销**：
  - 5阶段跟进序列（Day1/3/6/10/15）
  - 邮件模板管理
  - 打开率/回复率追踪
- **WhatsApp开发**：
  - 快捷话术模板
  - 文本/图片消息发送
  - 已读/回复状态追踪
- **LinkedIn开发**：
  - 自动添加联系人
  - 消息发送
  - 主页查看

### 5. 跟进转化 (Follow-up & Conversion)
- **CRM跟进记录**：完整的客户交互历史
- **任务管理**：自动创建跟进任务
- **报价管理**：报价单生成与状态追踪
- **客户状态流转**：New → Contacted → Replied → Quoted → Negotiation → Won/Lost

### 6. 数据分析 (Data Analysis)
- **看板统计**：实时业务指标
- **邮件/WA效果分析**：打开率、回复率趋势
- **转化漏斗**：从线索到成交的全流程可视化
- **渠道质量分析**：各获客渠道的ROI对比
- **30天趋势图**：新增客户、触达、回复趋势

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue3, Element Plus, Vue Router, Pinia, Axios, ECharts |
| 后端 | Spring Boot 3.2, Java 17, MyBatis Plus, Spring Security, JWT |
| 爬虫 | Python 3.11, Playwright, SerpAPI, PhantomBuster API |
| 数据库 | MySQL 8.0, Redis 7 |
| 部署 | Docker, Docker Compose, Nginx |

## 快速开始

### 环境要求
- Docker & Docker Compose
- Java 17 (本地开发)
- Node.js 18+ (本地开发)
- Python 3.11+ (爬虫开发)

### Docker一键部署

```bash
# 1. 克隆项目
git clone <repository-url>
cd thai-auto-parts-crm

# 2. 配置环境变量
cp .env.example .env
# 编辑.env文件，填入API密钥

# 3. 启动所有服务
docker-compose up -d

# 4. 访问系统
# 前端: http://localhost
# 后端API: http://localhost:8080/api
# 数据库: localhost:3306
```

### 本地开发

#### 后端
```bash
cd backend
mvn spring-boot:run
```

#### 前端
```bash
cd frontend
npm install
npm run dev
```

#### 爬虫
```bash
cd crawler
pip install -r requirements.txt
playwright install chromium
python task_scheduler.py
```

## 项目结构

```
thai-auto-parts-crm/
├── backend/                    # Spring Boot后端
│   ├── src/main/java/com/thaiautoparts/
│   │   ├── config/             # 配置类
│   │   ├── controller/         # REST API控制器
│   │   ├── dto/                # 数据传输对象
│   │   ├── entity/             # 数据库实体
│   │   ├── mapper/             # MyBatis Mapper
│   │   ├── service/            # 业务逻辑层
│   │   └── util/               # 工具类
│   └── src/main/resources/
│       └── application.yml     # 应用配置
├── frontend/                   # Vue3前端
│   ├── src/
│   │   ├── api/                # API调用
│   │   ├── router/             # 路由配置
│   │   ├── stores/             # Pinia状态管理
│   │   └── views/              # 页面组件
│   └── package.json
├── crawler/                    # Python爬虫
│   ├── google_crawler.py       # Google搜索/Maps爬虫
│   ├── linkedin_crawler.py     # LinkedIn爬虫
│   ├── b2b_crawler.py          # B2B平台爬虫
│   └── task_scheduler.py       # 任务调度器
├── database/
│   └── schema.sql              # 数据库建表脚本
├── docker-compose.yml          # Docker编排
└── README.md
```

## 数据库表结构

| 表名 | 说明 |
|------|------|
| company | 客户公司主表 |
| contact_person | 联系人信息 |
| email_campaign | 邮件营销活动 |
| email_record | 邮件发送记录 |
| email_template | 邮件模板 |
| whatsapp_record | WhatsApp消息记录 |
| linkedin_record | LinkedIn操作记录 |
| follow_up_record | 跟进记录 |
| task | 任务管理 |
| quotation | 报价单 |
| crawler_task | 爬虫任务 |
| daily_stats | 每日统计数据 |
| system_config | 系统配置 |

## API密钥配置

系统需要以下第三方API密钥：

| API | 用途 | 获取地址 |
|-----|------|----------|
| SerpAPI | Google搜索数据 | https://serpapi.com |
| PhantomBuster | LinkedIn自动化 | https://phantombuster.com |
| WhatsApp Business API | WhatsApp消息 | https://developers.facebook.com |
| Google Maps API | 地理位置数据 | https://console.cloud.google.com |

## 客户评分算法

```
总分 = 100分

1. 公司名称匹配度 (20分)
   - 包含"auto parts"/"automotive"等关键词: 20分
   - 包含"car"/"motor"等关键词: 10分
   - 其他: 5分

2. 网站质量 (15分)
   - 有官网且内容丰富: 15分
   - 有官网但内容简单: 10分
   - 无官网: 0分

3. 联系人职位 (20分)
   - Owner/CEO/Director: 20分
   - Purchasing/Procurement Manager: 18分
   - Import/Export Manager: 15分
   - 其他: 5分

4. 公司规模 (15分)
   - 大型(员工>100): 15分
   - 中型(员工20-100): 10分
   - 小型(员工<20): 5分

5. 地理位置 (10分)
   - 曼谷/工业区: 10分
   - 其他主要城市: 7分
   - 偏远地区: 3分

6. 产品匹配度 (20分)
   - 明确经营汽配产品: 20分
   - 可能经营汽配: 10分
   - 不相关: 0分

等级划分:
- S级: ≥85分 (重点跟进)
- A级: 70-84分 (优先跟进)
- B级: 50-69分 (常规跟进)
- C级: <50分 (暂缓跟进)
```

## 邮件跟进序列

| 阶段 | 发送时间 | 邮件类型 | 目标 |
|------|----------|----------|------|
| Day 1 | 获取线索后立即 | 公司介绍 | 建立初步联系 |
| Day 3 | 第3天 | 热销产品推荐 | 展示产品优势 |
| Day 6 | 第6天 | OEM合作案例 | 增强信任 |
| Day 10 | 第10天 | 报价引导 | 引导询盘 |
| Day 15 | 第15天 | 促销提醒 | 促成决策 |

## 部署说明

### 生产环境建议
- **服务器**：4核8G以上，100G SSD
- **数据库**：MySQL主从复制，定期备份
- **缓存**：Redis集群
- **负载均衡**：Nginx反向代理
- **SSL证书**：Let's Encrypt免费证书
- **监控**：Prometheus + Grafana

### 安全注意事项
- 修改默认数据库密码
- 配置JWT密钥
- 启用HTTPS
- 定期更新依赖包
- 配置防火墙规则

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue或联系开发团队。
