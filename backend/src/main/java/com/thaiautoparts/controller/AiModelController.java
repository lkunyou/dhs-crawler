package com.thaiautoparts.controller;

import com.thaiautoparts.dto.AiModelConfigDTO;
import com.thaiautoparts.dto.Result;
import com.thaiautoparts.service.AiModelService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/ai/models")
@RequiredArgsConstructor
public class AiModelController {

    private final AiModelService modelService;

    @GetMapping
    public Result<List<AiModelConfigDTO>> getModels() {
        return Result.success(modelService.getModels());
    }

    @GetMapping("/enabled")
    public Result<List<AiModelConfigDTO>> getEnabledModels() {
        return Result.success(modelService.getEnabledModels());
    }

    @GetMapping("/{id}")
    public Result<AiModelConfigDTO> getModel(@PathVariable Long id) {
        return Result.success(modelService.getModel(id));
    }

    @GetMapping("/provider/{provider}")
    public Result<AiModelConfigDTO> getModelByProvider(@PathVariable String provider) {
        return Result.success(modelService.getModelByProvider(provider));
    }

    @PostMapping
    public Result<AiModelConfigDTO> createModel(@RequestBody AiModelConfigDTO dto) {
        return Result.success(modelService.createModel(dto));
    }

    @PutMapping("/{id}")
    public Result<AiModelConfigDTO> updateModel(@PathVariable Long id, @RequestBody AiModelConfigDTO dto) {
        return Result.success(modelService.updateModel(id, dto));
    }

    @DeleteMapping("/{id}")
    public Result<Void> deleteModel(@PathVariable Long id) {
        modelService.deleteModel(id);
        return Result.success();
    }

    @PostMapping("/{id}/toggle")
    public Result<Void> toggleModel(@PathVariable Long id, @RequestParam Boolean enabled) {
        modelService.toggleModel(id, enabled);
        return Result.success();
    }

    @PostMapping("/chat")
    public Result<Map<String, String>> chat(@RequestBody Map<String, Object> request) {
        String provider = (String) request.get("provider");
        String message = (String) request.get("message");
        String systemPrompt = (String) request.get("systemPrompt");
        
        String response = modelService.chat(provider, message, systemPrompt);
        return Result.success(Map.of("content", response));
    }
}
