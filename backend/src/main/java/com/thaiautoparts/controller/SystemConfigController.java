package com.thaiautoparts.controller;

import com.thaiautoparts.config.TwilioConfig;
import com.thaiautoparts.dto.Result;
import com.thaiautoparts.entity.SystemConfig;
import com.thaiautoparts.service.SystemConfigService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/system-configs")
@RequiredArgsConstructor
public class SystemConfigController {

    private final SystemConfigService systemConfigService;
    private final TwilioConfig twilioConfig;

    @GetMapping
    public Result<List<SystemConfig>> listAll() {
        return Result.success(systemConfigService.listAll());
    }

    @GetMapping("/{id}")
    public Result<SystemConfig> getById(@PathVariable Long id) {
        return Result.success(systemConfigService.getById(id));
    }

    @GetMapping("/key/{configKey}")
    public Result<SystemConfig> getByKey(@PathVariable String configKey) {
        return Result.success(systemConfigService.getByKey(configKey));
    }

    @PostMapping
    public Result<SystemConfig> createConfig(@RequestBody SystemConfig config) {
        return Result.success(systemConfigService.saveConfig(config));
    }

    @PutMapping("/{id}")
    public Result<SystemConfig> updateConfig(@PathVariable Long id, @RequestBody SystemConfig config) {
        return Result.success(systemConfigService.updateConfig(id, config));
    }

    @DeleteMapping("/{id}")
    public Result<Void> deleteConfig(@PathVariable Long id) {
        systemConfigService.deleteConfig(id);
        return Result.success();
    }

    @PostMapping("/init-defaults")
    public Result<Void> initDefaults() {
        systemConfigService.initDefaultConfigs();
        return Result.success();
    }

    @PostMapping("/refresh-twilio")
    public Result<Void> refreshTwilioConfig() {
        twilioConfig.refreshConfig();
        return Result.success();
    }
}
