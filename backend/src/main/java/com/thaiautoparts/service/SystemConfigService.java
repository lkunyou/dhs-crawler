package com.thaiautoparts.service;

import com.thaiautoparts.entity.SystemConfig;
import java.util.List;

public interface SystemConfigService {
    List<SystemConfig> listAll();
    SystemConfig getById(Long id);
    SystemConfig getByKey(String configKey);
    String getValue(String configKey, String defaultValue);
    SystemConfig saveConfig(SystemConfig config);
    SystemConfig updateConfig(Long id, SystemConfig config);
    void deleteConfig(Long id);
    void initDefaultConfigs();
}
