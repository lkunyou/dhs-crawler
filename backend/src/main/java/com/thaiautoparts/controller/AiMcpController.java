package com.thaiautoparts.controller;

import com.thaiautoparts.dto.AiMcpToolDTO;
import com.thaiautoparts.dto.McpExecuteRequest;
import com.thaiautoparts.dto.McpExecuteResponse;
import com.thaiautoparts.dto.Result;
import com.thaiautoparts.service.AiMcpService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/ai/mcp")
@RequiredArgsConstructor
public class AiMcpController {

    private final AiMcpService mcpService;

    @GetMapping
    public Result<List<AiMcpToolDTO>> getTools() {
        return Result.success(mcpService.getTools());
    }

    @GetMapping("/{id}")
    public Result<AiMcpToolDTO> getTool(@PathVariable Long id) {
        return Result.success(mcpService.getTool(id));
    }

    @PostMapping
    public Result<AiMcpToolDTO> createTool(@RequestBody AiMcpToolDTO dto) {
        return Result.success(mcpService.createTool(dto));
    }

    @PutMapping("/{id}")
    public Result<AiMcpToolDTO> updateTool(@PathVariable Long id, @RequestBody AiMcpToolDTO dto) {
        return Result.success(mcpService.updateTool(id, dto));
    }

    @DeleteMapping("/{id}")
    public Result<Void> deleteTool(@PathVariable Long id) {
        mcpService.deleteTool(id);
        return Result.success();
    }

    @PostMapping("/{id}/toggle")
    public Result<Void> toggleTool(@PathVariable Long id, @RequestParam Boolean enabled) {
        mcpService.toggleTool(id, enabled);
        return Result.success();
    }

    @PostMapping("/execute")
    public Result<McpExecuteResponse> executeTool(@RequestBody McpExecuteRequest request) {
        return Result.success(mcpService.executeTool(request));
    }
}
