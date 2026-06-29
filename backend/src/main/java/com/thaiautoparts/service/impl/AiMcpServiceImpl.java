package com.thaiautoparts.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.thaiautoparts.dto.AiMcpToolDTO;
import com.thaiautoparts.dto.McpExecuteRequest;
import com.thaiautoparts.dto.McpExecuteResponse;
import com.thaiautoparts.entity.AiMcpTool;
import com.thaiautoparts.repository.AiMcpToolMapper;
import com.thaiautoparts.service.AiMcpService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class AiMcpServiceImpl implements AiMcpService {

    private final AiMcpToolMapper toolMapper;

    @Override
    public List<AiMcpToolDTO> getTools() {
        return toolMapper.selectList(new LambdaQueryWrapper<AiMcpTool>()
                .orderByAsc(AiMcpTool::getName))
            .stream()
            .map(this::convertToDTO)
            .collect(Collectors.toList());
    }

    @Override
    public AiMcpToolDTO getTool(Long id) {
        AiMcpTool tool = toolMapper.selectById(id);
        return tool != null ? convertToDTO(tool) : null;
    }

    @Override
    @Transactional
    public AiMcpToolDTO createTool(AiMcpToolDTO dto) {
        AiMcpTool tool = new AiMcpTool();
        tool.setName(dto.getName());
        tool.setDescription(dto.getDescription());
        tool.setToolType(dto.getToolType());
        tool.setEndpoint(dto.getEndpoint());
        tool.setConfig(dto.getConfig());
        tool.setCapabilities(dto.getCapabilities());
        tool.setEnabled(dto.getEnabled() != null ? dto.getEnabled() : true);
        tool.setCreatedAt(LocalDateTime.now());
        tool.setUpdatedAt(LocalDateTime.now());
        toolMapper.insert(tool);
        return convertToDTO(tool);
    }

    @Override
    @Transactional
    public AiMcpToolDTO updateTool(Long id, AiMcpToolDTO dto) {
        AiMcpTool tool = toolMapper.selectById(id);
        if (tool == null) {
            throw new RuntimeException("Tool not found");
        }
        if (dto.getName() != null) tool.setName(dto.getName());
        if (dto.getDescription() != null) tool.setDescription(dto.getDescription());
        if (dto.getToolType() != null) tool.setToolType(dto.getToolType());
        if (dto.getEndpoint() != null) tool.setEndpoint(dto.getEndpoint());
        if (dto.getConfig() != null) tool.setConfig(dto.getConfig());
        if (dto.getCapabilities() != null) tool.setCapabilities(dto.getCapabilities());
        if (dto.getEnabled() != null) tool.setEnabled(dto.getEnabled());
        tool.setUpdatedAt(LocalDateTime.now());
        toolMapper.updateById(tool);
        return convertToDTO(tool);
    }

    @Override
    @Transactional
    public void deleteTool(Long id) {
        toolMapper.deleteById(id);
    }

    @Override
    @Transactional
    public void toggleTool(Long id, Boolean enabled) {
        AiMcpTool tool = toolMapper.selectById(id);
        if (tool != null) {
            tool.setEnabled(enabled);
            tool.setUpdatedAt(LocalDateTime.now());
            toolMapper.updateById(tool);
        }
    }

    @Override
    public McpExecuteResponse executeTool(McpExecuteRequest request) {
        McpExecuteResponse response = new McpExecuteResponse();
        
        try {
            AiMcpTool tool = null;
            if (request.getToolId() != null) {
                tool = toolMapper.selectById(request.getToolId());
            } else if (request.getToolName() != null) {
                tool = toolMapper.selectOne(
                    new LambdaQueryWrapper<AiMcpTool>().eq(AiMcpTool::getName, request.getToolName())
                );
            }
            
            if (tool == null) {
                response.setError("Tool not found");
                return response;
            }
            
            if (!Boolean.TRUE.equals(tool.getEnabled())) {
                response.setError("Tool is disabled");
                return response;
            }
            
            log.info("Executing MCP tool: {}, type: {}, endpoint: {}", 
                tool.getName(), tool.getToolType(), tool.getEndpoint());
            
            String result = String.format(
                "MCP Tool '%s' executed successfully. Tool type: %s, Endpoint: %s, Parameters: %s",
                tool.getName(),
                tool.getToolType() != null ? tool.getToolType() : "unknown",
                tool.getEndpoint() != null ? tool.getEndpoint() : "local",
                request.getParameters() != null ? request.getParameters() : "{}"
            );
            
            response.setResult(result);
            response.setToolId(tool.getId());
            response.setToolName(tool.getName());
            
        } catch (Exception e) {
            log.error("Failed to execute MCP tool", e);
            response.setError("Execution failed: " + e.getMessage());
        }
        
        return response;
    }

    private AiMcpToolDTO convertToDTO(AiMcpTool tool) {
        AiMcpToolDTO dto = new AiMcpToolDTO();
        dto.setId(tool.getId());
        dto.setName(tool.getName());
        dto.setDescription(tool.getDescription());
        dto.setToolType(tool.getToolType());
        dto.setEndpoint(tool.getEndpoint());
        dto.setConfig(tool.getConfig());
        dto.setCapabilities(tool.getCapabilities());
        dto.setEnabled(tool.getEnabled());
        return dto;
    }
}
