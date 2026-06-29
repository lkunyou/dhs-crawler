package com.thaiautoparts.service;

import com.thaiautoparts.dto.*;
import com.thaiautoparts.entity.AiConversation;
import com.thaiautoparts.entity.AiMessage;
import java.util.List;

public interface AiService {
    ChatResponse chat(ChatRequest request);
    List<AiConversation> getConversations();
    List<AiMessage> getMessages(Long conversationId);
    AiConversation createConversation(String title);
    void deleteConversation(Long id);
    
    AgentExecuteResponse executeAgent(AgentExecuteRequest request);
    String getAgentStatus(String taskId);
    
    List<AiSkillDTO> getSkills();
    AiSkillDTO createSkill(AiSkillDTO dto);
    AiSkillDTO updateSkill(Long id, AiSkillDTO dto);
    void deleteSkill(Long id);
}
