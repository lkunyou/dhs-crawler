package com.thaiautoparts.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.thaiautoparts.dto.AiAgentDTO;
import com.thaiautoparts.entity.AiAgent;
import com.thaiautoparts.repository.AiAgentMapper;
import com.thaiautoparts.service.AiAgentService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class AiAgentServiceImpl implements AiAgentService {

    private final AiAgentMapper agentMapper;

    @Override
    public List<AiAgentDTO> getAgents() {
        return agentMapper.selectList(new LambdaQueryWrapper<AiAgent>()
                .orderByAsc(AiAgent::getName))
            .stream()
            .map(this::convertToDTO)
            .collect(Collectors.toList());
    }

    @Override
    public AiAgentDTO getAgentByType(String agentType) {
        AiAgent agent = agentMapper.selectOne(
            new LambdaQueryWrapper<AiAgent>().eq(AiAgent::getAgentType, agentType)
        );
        return agent != null ? convertToDTO(agent) : null;
    }

    @Override
    @Transactional
    public AiAgentDTO createAgent(AiAgentDTO dto) {
        AiAgent agent = new AiAgent();
        agent.setAgentType(dto.getAgentType());
        agent.setName(dto.getName());
        agent.setDescription(dto.getDescription());
        agent.setPrompt(dto.getPrompt());
        agent.setConfig(dto.getConfig());
        agent.setEnabled(dto.getEnabled() != null ? dto.getEnabled() : true);
        agent.setCreatedAt(LocalDateTime.now());
        agent.setUpdatedAt(LocalDateTime.now());
        agentMapper.insert(agent);
        return convertToDTO(agent);
    }

    @Override
    @Transactional
    public AiAgentDTO updateAgent(Long id, AiAgentDTO dto) {
        AiAgent agent = agentMapper.selectById(id);
        if (agent == null) {
            throw new RuntimeException("Agent not found");
        }
        if (dto.getName() != null) agent.setName(dto.getName());
        if (dto.getDescription() != null) agent.setDescription(dto.getDescription());
        if (dto.getPrompt() != null) agent.setPrompt(dto.getPrompt());
        if (dto.getConfig() != null) agent.setConfig(dto.getConfig());
        if (dto.getEnabled() != null) agent.setEnabled(dto.getEnabled());
        agent.setUpdatedAt(LocalDateTime.now());
        agentMapper.updateById(agent);
        return convertToDTO(agent);
    }

    @Override
    @Transactional
    public void deleteAgent(Long id) {
        agentMapper.deleteById(id);
    }

    @Override
    @Transactional
    public void toggleAgent(Long id, Boolean enabled) {
        AiAgent agent = agentMapper.selectById(id);
        if (agent != null) {
            agent.setEnabled(enabled);
            agent.setUpdatedAt(LocalDateTime.now());
            agentMapper.updateById(agent);
        }
    }

    private AiAgentDTO convertToDTO(AiAgent agent) {
        AiAgentDTO dto = new AiAgentDTO();
        dto.setId(agent.getId());
        dto.setAgentType(agent.getAgentType());
        dto.setName(agent.getName());
        dto.setDescription(agent.getDescription());
        dto.setPrompt(agent.getPrompt());
        dto.setConfig(agent.getConfig());
        dto.setEnabled(agent.getEnabled());
        return dto;
    }
}
