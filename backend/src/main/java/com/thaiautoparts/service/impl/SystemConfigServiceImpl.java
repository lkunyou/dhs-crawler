package com.thaiautoparts.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.thaiautoparts.entity.SystemConfig;
import com.thaiautoparts.repository.SystemConfigMapper;
import com.thaiautoparts.service.SystemConfigService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
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
