package com.thaiautoparts.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.thaiautoparts.dto.*;
import com.thaiautoparts.entity.*;
import com.thaiautoparts.repository.*;
import com.thaiautoparts.service.AiLlmService;
import com.thaiautoparts.service.AiService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class AiServiceImpl implements AiService {

    private final AiConversationMapper conversationMapper;
    private final AiMessageMapper messageMapper;
    private final AiSkillMapper skillMapper;
    private final AiAgentTaskMapper agentTaskMapper;
    private final AiLlmService aiLlmService;

    @Override
    public ChatResponse chat(ChatRequest request) {
        // 获取或创建对话
        AiConversation conversation;
        if (request.getConversationId() == null) {
            conversation = createConversation("新对话");
        } else {
            conversation = conversationMapper.selectById(request.getConversationId());
            if (conversation == null) {
                conversation = createConversation("新对话");
            }
        }

        // 保存用户消息
        AiMessage userMessage = new AiMessage();
        userMessage.setConversationId(conversation.getId());
        userMessage.setRole("user");
        userMessage.setContent(request.getMessage());
        userMessage.setModel(request.getModel());
        userMessage.setCreatedAt(LocalDateTime.now());
        messageMapper.insert(userMessage);

        // 调用 LangChain4j LLM 服务获取 AI 回复
        ChatResponse llmResponse = aiLlmService.chat(request);

        // 保存 AI 助手消息
        AiMessage assistantMessage = new AiMessage();
        assistantMessage.setConversationId(conversation.getId());
        assistantMessage.setRole("assistant");
        assistantMessage.setContent(llmResponse.getContent());
        assistantMessage.setModel(llmResponse.getModel() != null ? llmResponse.getModel() : request.getModel());
        assistantMessage.setCreatedAt(LocalDateTime.now());
        messageMapper.insert(assistantMessage);

        // 更新对话时间
        conversation.setUpdatedAt(LocalDateTime.now());
        conversationMapper.updateById(conversation);

        // 返回响应
        llmResponse.setConversationId(conversation.getId());
        llmResponse.setMessageId(String.valueOf(assistantMessage.getId()));
        return llmResponse;
    }

    @Override
    public List<AiConversation> getConversations() {
        return conversationMapper.selectList(
            new LambdaQueryWrapper<AiConversation>()
                .orderByDesc(AiConversation::getUpdatedAt)
        );
    }

    @Override
    public List<AiMessage> getMessages(Long conversationId) {
        return messageMapper.selectList(
            new LambdaQueryWrapper<AiMessage>()
                .eq(AiMessage::getConversationId, conversationId)
                .orderByAsc(AiMessage::getCreatedAt)
        );
    }

    @Override
    @Transactional
    public AiConversation createConversation(String title) {
        AiConversation conversation = new AiConversation();
        conversation.setTitle(title != null ? title : "新对话");
        conversation.setModel("gpt-3.5-turbo");
        conversation.setCreatedAt(LocalDateTime.now());
        conversation.setUpdatedAt(LocalDateTime.now());
        conversationMapper.insert(conversation);
        return conversation;
    }

    @Override
    @Transactional
    public void deleteConversation(Long id) {
        messageMapper.delete(new LambdaQueryWrapper<AiMessage>().eq(AiMessage::getConversationId, id));
        conversationMapper.deleteById(id);
    }

    @Override
    @Transactional
    public AgentExecuteResponse executeAgent(AgentExecuteRequest request) {
        String taskId = UUID.randomUUID().toString();
        
        AiAgentTask task = new AiAgentTask();
        task.setTaskId(taskId);
        task.setAgentType(request.getAgentType());
        task.setInput(request.getInput());
        task.setStatus("running");
        task.setCreatedAt(LocalDateTime.now());
        task.setUpdatedAt(LocalDateTime.now());
        agentTaskMapper.insert(task);
        
        String result = "Agent [" + request.getAgentType() + "] 执行完成: " + request.getInput();
        
        task.setStatus("completed");
        task.setResult(result);
        task.setUpdatedAt(LocalDateTime.now());
        agentTaskMapper.updateById(task);
        
        AgentExecuteResponse response = new AgentExecuteResponse();
        response.setTaskId(taskId);
        response.setStatus("completed");
        response.setResult(result);
        
        return response;
    }

    @Override
    public String getAgentStatus(String taskId) {
        AiAgentTask task = agentTaskMapper.selectOne(
            new LambdaQueryWrapper<AiAgentTask>()
                .eq(AiAgentTask::getTaskId, taskId)
        );
        return task != null ? task.getStatus() : "not_found";
    }

    @Override
    public List<AiSkillDTO> getSkills() {
        return skillMapper.selectList(new LambdaQueryWrapper<AiSkill>().orderByAsc(AiSkill::getName))
            .stream()
            .map(this::convertToDTO)
            .collect(Collectors.toList());
    }

    @Override
    public AiSkillDTO createSkill(AiSkillDTO dto) {
        AiSkill skill = new AiSkill();
        skill.setName(dto.getName());
        skill.setDescription(dto.getDescription());
        skill.setType(dto.getType());
        skill.setConfig(dto.getConfig());
        skill.setEnabled(dto.getEnabled() != null ? dto.getEnabled() : true);
        skill.setCreatedAt(LocalDateTime.now());
        skill.setUpdatedAt(LocalDateTime.now());
        skillMapper.insert(skill);
        return convertToDTO(skill);
    }

    @Override
    public AiSkillDTO updateSkill(Long id, AiSkillDTO dto) {
        AiSkill skill = skillMapper.selectById(id);
        if (skill == null) {
            throw new RuntimeException("Skill not found");
        }
        if (dto.getName() != null) skill.setName(dto.getName());
        if (dto.getDescription() != null) skill.setDescription(dto.getDescription());
        if (dto.getType() != null) skill.setType(dto.getType());
        if (dto.getConfig() != null) skill.setConfig(dto.getConfig());
        if (dto.getEnabled() != null) skill.setEnabled(dto.getEnabled());
        skill.setUpdatedAt(LocalDateTime.now());
        skillMapper.updateById(skill);
        return convertToDTO(skill);
    }

    @Override
    public void deleteSkill(Long id) {
        skillMapper.deleteById(id);
    }

    private AiSkillDTO convertToDTO(AiSkill skill) {
        AiSkillDTO dto = new AiSkillDTO();
        dto.setId(skill.getId());
        dto.setName(skill.getName());
        dto.setDescription(skill.getDescription());
        dto.setType(skill.getType());
        dto.setConfig(skill.getConfig());
        dto.setEnabled(skill.getEnabled());
        return dto;
    }
}
