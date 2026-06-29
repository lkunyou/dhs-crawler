package com.thaiautoparts.controller;

import com.thaiautoparts.dto.*;
import com.thaiautoparts.entity.AiConversation;
import com.thaiautoparts.entity.AiMessage;
import com.thaiautoparts.service.AiAgentChatService;
import com.thaiautoparts.service.AiRagService;
import com.thaiautoparts.service.AiService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/ai")
@RequiredArgsConstructor
public class AiController {

    private final AiService aiService;
    private final AiAgentChatService agentChatService;
    private final AiRagService ragService;

    @PostMapping("/chat")
    public Result<ChatResponse> chat(@RequestBody ChatRequest request) {
        return Result.success(aiService.chat(request));
    }

    /**
     * Agent 聊天接口 - 支持工具调用
     */
    @PostMapping("/agent/chat")
    public Result<AgentChatResponse> agentChat(@RequestBody AgentChatRequest request) {
        return Result.success(agentChatService.chat(request));
    }

    /**
     * 获取 Agent 可用工具列表
     */
    @GetMapping("/agent/{agentType}/tools")
    public Result<String[]> getAgentTools(@PathVariable String agentType) {
        return Result.success(agentChatService.getAvailableTools(agentType));
    }

    /**
     * 搜索知识库
     */
    @GetMapping("/rag/search")
    public Result<List<RagSearchResult>> searchRag(@RequestParam String query,
                                                   @RequestParam(defaultValue = "5") int topK) {
        return Result.success(ragService.search(query, topK));
    }

    /**
     * 将公司添加到知识库
     */
    @PostMapping("/rag/index/company/{companyId}")
    public Result<Void> indexCompany(@PathVariable Long companyId) {
        ragService.indexCompany(companyId);
        return Result.success();
    }

    /**
     * 将产品添加到知识库
     */
    @PostMapping("/rag/index/product/{productId}")
    public Result<Void> indexProduct(@PathVariable Long productId) {
        ragService.indexProduct(productId);
        return Result.success();
    }

    /**
     * 添加自定义文档到知识库
     */
    @PostMapping("/rag/document")
    public Result<Void> addDocument(@RequestBody RagDocumentRequest request) {
        ragService.addDocument(request.getContent(), request.getSource(), request.getSourceId());
        return Result.success();
    }

    /**
     * 清空知识库
     */
    @DeleteMapping("/rag/clear")
    public Result<Void> clearRag() {
        ragService.clear();
        return Result.success();
    }

    /**
     * 获取知识库文档数量
     */
    @GetMapping("/rag/count")
    public Result<Integer> getRagCount() {
        return Result.success(ragService.getDocumentCount());
    }

    @GetMapping("/conversations")
    public Result<List<AiConversation>> getConversations() {
        return Result.success(aiService.getConversations());
    }

    @GetMapping("/conversations/{id}/messages")
    public Result<List<AiMessage>> getMessages(@PathVariable Long id) {
        return Result.success(aiService.getMessages(id));
    }

    @PostMapping("/conversations")
    public Result<AiConversation> createConversation(@RequestParam(required = false) String title) {
        return Result.success(aiService.createConversation(title));
    }

    @DeleteMapping("/conversations/{id}")
    public Result<Void> deleteConversation(@PathVariable Long id) {
        aiService.deleteConversation(id);
        return Result.success();
    }

    @PostMapping("/agent/execute")
    public Result<AgentExecuteResponse> executeAgent(@RequestBody AgentExecuteRequest request) {
        return Result.success(aiService.executeAgent(request));
    }

    @GetMapping("/agent/status/{taskId}")
    public Result<String> getAgentStatus(@PathVariable String taskId) {
        return Result.success(aiService.getAgentStatus(taskId));
    }

    @GetMapping("/skills")
    public Result<List<AiSkillDTO>> getSkills() {
        return Result.success(aiService.getSkills());
    }

    @PostMapping("/skills")
    public Result<AiSkillDTO> createSkill(@RequestBody AiSkillDTO dto) {
        return Result.success(aiService.createSkill(dto));
    }

    @PutMapping("/skills/{id}")
    public Result<AiSkillDTO> updateSkill(@PathVariable Long id, @RequestBody AiSkillDTO dto) {
        return Result.success(aiService.updateSkill(id, dto));
    }

    @DeleteMapping("/skills/{id}")
    public Result<Void> deleteSkill(@PathVariable Long id) {
        aiService.deleteSkill(id);
        return Result.success();
    }
}
