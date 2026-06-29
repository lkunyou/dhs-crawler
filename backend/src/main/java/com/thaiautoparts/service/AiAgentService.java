package com.thaiautoparts.service;

import com.thaiautoparts.dto.AiAgentDTO;
import java.util.List;

public interface AiAgentService {
    List<AiAgentDTO> getAgents();
    AiAgentDTO getAgentByType(String agentType);
    AiAgentDTO createAgent(AiAgentDTO dto);
    AiAgentDTO updateAgent(Long id, AiAgentDTO dto);
    void deleteAgent(Long id);
    void toggleAgent(Long id, Boolean enabled);
}
