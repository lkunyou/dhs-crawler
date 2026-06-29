package com.thaiautoparts.controller;

import com.thaiautoparts.dto.AiAgentDTO;
import com.thaiautoparts.dto.Result;
import com.thaiautoparts.service.AiAgentService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/ai/agent")
@RequiredArgsConstructor
public class AiAgentController {

    private final AiAgentService agentService;

    @GetMapping
    public Result<List<AiAgentDTO>> getAgents() {
        return Result.success(agentService.getAgents());
    }

    @GetMapping("/{agentType}")
    public Result<AiAgentDTO> getAgentByType(@PathVariable String agentType) {
        return Result.success(agentService.getAgentByType(agentType));
    }

    @PostMapping
    public Result<AiAgentDTO> createAgent(@RequestBody AiAgentDTO dto) {
        return Result.success(agentService.createAgent(dto));
    }

    @PutMapping("/{id}")
    public Result<AiAgentDTO> updateAgent(@PathVariable Long id, @RequestBody AiAgentDTO dto) {
        return Result.success(agentService.updateAgent(id, dto));
    }

    @DeleteMapping("/{id}")
    public Result<Void> deleteAgent(@PathVariable Long id) {
        agentService.deleteAgent(id);
        return Result.success();
    }

    @PostMapping("/{id}/toggle")
    public Result<Void> toggleAgent(@PathVariable Long id, @RequestParam Boolean enabled) {
        agentService.toggleAgent(id, enabled);
        return Result.success();
    }
}
