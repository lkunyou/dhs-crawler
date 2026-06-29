package com.thaiautoparts.service;

import com.thaiautoparts.dto.AiMcpToolDTO;
import com.thaiautoparts.dto.McpExecuteRequest;
import com.thaiautoparts.dto.McpExecuteResponse;
import java.util.List;

public interface AiMcpService {
    List<AiMcpToolDTO> getTools();
    AiMcpToolDTO getTool(Long id);
    AiMcpToolDTO createTool(AiMcpToolDTO dto);
    AiMcpToolDTO updateTool(Long id, AiMcpToolDTO dto);
    void deleteTool(Long id);
    void toggleTool(Long id, Boolean enabled);
    McpExecuteResponse executeTool(McpExecuteRequest request);
}
