package com.thaiautoparts.service;

import com.thaiautoparts.dto.AiModelConfigDTO;
import java.util.List;

public interface AiModelService {
    List<AiModelConfigDTO> getModels();
    List<AiModelConfigDTO> getEnabledModels();
    AiModelConfigDTO getModel(Long id);
    AiModelConfigDTO getModelByProvider(String provider);
    AiModelConfigDTO createModel(AiModelConfigDTO dto);
    AiModelConfigDTO updateModel(Long id, AiModelConfigDTO dto);
    void deleteModel(Long id);
    void toggleModel(Long id, Boolean enabled);
    
    String chat(String provider, String message, String systemPrompt);
    String chatWithHistory(String provider, List<ChatMessage> history, String systemPrompt);
    
    public static class ChatMessage {
        private String role;
        private String content;
        public String getRole() { return role; }
        public void setRole(String role) { this.role = role; }
        public String getContent() { return content; }
        public void setContent(String content) { this.content = content; }
    }
}
