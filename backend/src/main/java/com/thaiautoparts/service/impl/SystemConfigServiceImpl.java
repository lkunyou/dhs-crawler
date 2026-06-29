package com.thaiautoparts.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.thaiautoparts.entity.SystemConfig;
import com.thaiautoparts.repository.SystemConfigMapper;
import com.thaiautoparts.service.SystemConfigService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;

@Service
@RequiredArgsConstructor
public class SystemConfigServiceImpl implements SystemConfigService {

    private final SystemConfigMapper systemConfigMapper;

    @Override
    public List<SystemConfig> listAll() {
        return systemConfigMapper.selectList(new LambdaQueryWrapper<SystemConfig>().orderByAsc(SystemConfig::getConfigKey));
    }

    @Override
    public SystemConfig getById(Long id) {
        return systemConfigMapper.selectById(id);
    }

    @Override
    public SystemConfig getByKey(String configKey) {
        return systemConfigMapper.selectOne(
            new LambdaQueryWrapper<SystemConfig>().eq(SystemConfig::getConfigKey, configKey)
        );
    }

    @Override
    public String getValue(String configKey, String defaultValue) {
        SystemConfig config = systemConfigMapper.selectOne(
            new LambdaQueryWrapper<SystemConfig>().eq(SystemConfig::getConfigKey, configKey)
        );
        if (config == null || config.getConfigValue() == null) {
            return defaultValue;
        }
        return config.getConfigValue();
    }

    @Override
    @Transactional
    public void initDefaultConfigs() {
        List<SystemConfig> defaults = Arrays.asList(
            // 邮件配置
            new SystemConfig() {{ setConfigKey("mail.host"); setConfigValue("smtp.qiye.aliyun.com"); setConfigType("email"); setDescription("SMTP服务器地址"); }},
            new SystemConfig() {{ setConfigKey("mail.port"); setConfigValue("465"); setConfigType("email"); setDescription("SMTP端口"); }},
            new SystemConfig() {{ setConfigKey("mail.host-imap"); setConfigValue("imap.qiye.aliyun.com"); setConfigType("email"); setDescription("IMAP服务器地址"); }},
            new SystemConfig() {{ setConfigKey("mail.port-imap"); setConfigValue("993"); setConfigType("email"); setDescription("IMAP端口"); }},
            new SystemConfig() {{ setConfigKey("mail.username"); setConfigValue("market@carparts-land.com"); setConfigType("email"); setDescription("邮箱账号"); }},
            new SystemConfig() {{ setConfigKey("mail.password"); setConfigValue(""); setConfigType("email"); setDescription("邮箱密码/授权码"); }},
            new SystemConfig() {{ setConfigKey("mail.ssl.enable"); setConfigValue("true"); setConfigType("email"); setDescription("启用SSL"); }},
            new SystemConfig() {{ setConfigKey("mail.connectiontimeout"); setConfigValue("5000"); setConfigType("email"); setDescription("连接超时(ms)"); }},
            new SystemConfig() {{ setConfigKey("mail.timeout"); setConfigValue("5000"); setConfigType("email"); setDescription("读取超时(ms)"); }},
            // 搜索配置
            new SystemConfig() {{ setConfigKey("search.serpapi-key"); setConfigValue(""); setConfigType("search"); setDescription("SerpAPI密钥"); }},
            new SystemConfig() {{ setConfigKey("search.brave-api-key"); setConfigValue(""); setConfigType("search"); setDescription("Brave Search API密钥"); }},
            new SystemConfig() {{ setConfigKey("search.bing-api-key"); setConfigValue(""); setConfigType("search"); setDescription("Bing API密钥"); }},
            // 爬虫配置
            new SystemConfig() {{ setConfigKey("crawler.python.path"); setConfigValue("python"); setConfigType("crawler"); setDescription("Python路径"); }},
            new SystemConfig() {{ setConfigKey("crawler.output-dir"); setConfigValue("/tmp"); setConfigType("crawler"); setDescription("爬虫输出目录"); }},
            new SystemConfig() {{ setConfigKey("crawler.max-concurrent"); setConfigValue("3"); setConfigType("crawler"); setDescription("最大并发任务数"); }},
            new SystemConfig() {{ setConfigKey("crawler.timeout"); setConfigValue("30"); setConfigType("crawler"); setDescription("请求超时(秒)"); }},
            new SystemConfig() {{ setConfigKey("crawler.retry-count"); setConfigValue("3"); setConfigType("crawler"); setDescription("失败重试次数"); }},
            new SystemConfig() {{ setConfigKey("crawler.headless"); setConfigValue("true"); setConfigType("crawler"); setDescription("无头浏览器模式"); }},
            // 爬虫API密钥
            new SystemConfig() {{ setConfigKey("crawler.serp-api-key"); setConfigValue(""); setConfigType("crawler"); setDescription("SerpAPI密钥(Google搜索)"); }},
            new SystemConfig() {{ setConfigKey("crawler.phantombuster-api-key"); setConfigValue(""); setConfigType("crawler"); setDescription("PhantomBuster密钥(LinkedIn)"); }},
            new SystemConfig() {{ setConfigKey("crawler.proxy-url"); setConfigValue(""); setConfigType("crawler"); setDescription("代理服务器地址"); }},
            new SystemConfig() {{ setConfigKey("crawler.proxy-username"); setConfigValue(""); setConfigType("crawler"); setDescription("代理用户名"); }},
            new SystemConfig() {{ setConfigKey("crawler.proxy-password"); setConfigValue(""); setConfigType("crawler"); setDescription("代理密码"); }},
            // 爬虫任务类型配置
            new SystemConfig() {{ setConfigKey("crawler.task.google-search"); setConfigValue("true"); setConfigType("crawler"); setDescription("启用Google搜索爬虫"); }},
            new SystemConfig() {{ setConfigKey("crawler.task.google-maps"); setConfigValue("true"); setConfigType("crawler"); setDescription("启用Google Maps爬虫"); }},
            new SystemConfig() {{ setConfigKey("crawler.task.linkedin"); setConfigValue("true"); setConfigType("crawler"); setDescription("启用LinkedIn爬虫"); }},
            new SystemConfig() {{ setConfigKey("crawler.task.thai-trade"); setConfigValue("true"); setConfigType("crawler"); setDescription("启用ThaiTrade爬虫"); }},
            new SystemConfig() {{ setConfigKey("crawler.task.alibaba"); setConfigValue("true"); setConfigType("crawler"); setDescription("启用Alibaba爬虫"); }},
            new SystemConfig() {{ setConfigKey("crawler.task.tapaa"); setConfigValue("true"); setConfigType("crawler"); setDescription("启用TAPAA爬虫"); }},
            new SystemConfig() {{ setConfigKey("crawler.task.yellow-pages"); setConfigValue("true"); setConfigType("crawler"); setDescription("启用YellowPages爬虫"); }},
            new SystemConfig() {{ setConfigKey("crawler.task.batch"); setConfigValue("true"); setConfigType("crawler"); setDescription("启用批量爬虫"); }},
            // 限流配置
            new SystemConfig() {{ setConfigKey("rate-limit.email-daily"); setConfigValue("100"); setConfigType("rate-limit"); setDescription("每日邮件发送上限"); }},
            new SystemConfig() {{ setConfigKey("rate-limit.whatsapp-daily"); setConfigValue("50"); setConfigType("rate-limit"); setDescription("每日WhatsApp发送上限"); }},
            new SystemConfig() {{ setConfigKey("rate-limit.linkedin-daily"); setConfigValue("100"); setConfigType("rate-limit"); setDescription("每日LinkedIn操作上限"); }},
            // Twilio配置
            new SystemConfig() {{ setConfigKey("twilio.account-sid"); setConfigValue(""); setConfigType("twilio"); setDescription("Twilio Account SID"); }},
            new SystemConfig() {{ setConfigKey("twilio.auth-token"); setConfigValue(""); setConfigType("twilio"); setDescription("Twilio Auth Token"); }},
            new SystemConfig() {{ setConfigKey("twilio.whatsapp-number"); setConfigValue(""); setConfigType("twilio"); setDescription("Twilio WhatsApp号码"); }},
            // 基本配置
            new SystemConfig() {{ setConfigKey("upload_base_path"); setConfigValue("./uploads"); setConfigType("common"); setDescription("文件上传基础路径"); }},
            // AI 大模型配置
            new SystemConfig() {{ setConfigKey("ai.default-provider"); setConfigValue("deepseek"); setConfigType("ai"); setDescription("默认AI模型提供商"); }},
            new SystemConfig() {{ setConfigKey("ai.deepseek.api-key"); setConfigValue(""); setConfigType("ai"); setDescription("DeepSeek API密钥"); }},
            new SystemConfig() {{ setConfigKey("ai.kimi.api-key"); setConfigValue(""); setConfigType("ai"); setDescription("Kimi API密钥"); }},
            new SystemConfig() {{ setConfigKey("ai.glm.api-key"); setConfigValue(""); setConfigType("ai"); setDescription("智谱GLM API密钥"); }},
            new SystemConfig() {{ setConfigKey("ai.doubao.api-key"); setConfigValue(""); setConfigType("ai"); setDescription("豆包Doubao API密钥"); }},
            new SystemConfig() {{ setConfigKey("ai.qwen.api-key"); setConfigValue(""); setConfigType("ai"); setDescription("通义千问Qwen API密钥"); }},
            new SystemConfig() {{ setConfigKey("ai.minimax.api-key"); setConfigValue(""); setConfigType("ai"); setDescription("MiniMax API密钥"); }}
        );
        for (SystemConfig c : defaults) {
            if (getByKey(c.getConfigKey()) == null) {
                c.setUpdatedAt(LocalDateTime.now());
                systemConfigMapper.insert(c);
            }
        }
    }

    @Override
    @Transactional
    public SystemConfig saveConfig(SystemConfig config) {
        config.setUpdatedAt(LocalDateTime.now());
        systemConfigMapper.insert(config);
        return config;
    }

    @Override
    @Transactional
    public SystemConfig updateConfig(Long id, SystemConfig config) {
        SystemConfig existing = systemConfigMapper.selectById(id);
        if (existing == null) {
            throw new RuntimeException("配置不存在: " + id);
        }
        config.setId(id);
        config.setUpdatedAt(LocalDateTime.now());
        systemConfigMapper.updateById(config);
        return systemConfigMapper.selectById(id);
    }

    @Override
    @Transactional
    public void deleteConfig(Long id) {
        systemConfigMapper.deleteById(id);
    }
}
