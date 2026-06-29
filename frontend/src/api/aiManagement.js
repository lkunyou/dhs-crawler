import request from '@/utils/request'

export function getAgents() {
  return request({
    url: '/api/ai/agent',
    method: 'get'
  })
}

export function getAgentByType(agentType) {
  return request({
    url: `/api/ai/agent/${agentType}`,
    method: 'get'
  })
}

export function createAgent(data) {
  return request({
    url: '/api/ai/agent',
    method: 'post',
    data
  })
}

export function updateAgent(id, data) {
  return request({
    url: `/api/ai/agent/${id}`,
    method: 'put',
    data
  })
}

export function deleteAgent(id) {
  return request({
    url: `/api/ai/agent/${id}`,
    method: 'delete'
  })
}

export function toggleAgent(id, enabled) {
  return request({
    url: `/api/ai/agent/${id}/toggle`,
    method: 'post',
    params: { enabled }
  })
}

export function getMcpTools() {
  return request({
    url: '/api/ai/mcp',
    method: 'get'
  })
}

export function getMcpTool(id) {
  return request({
    url: `/api/ai/mcp/${id}`,
    method: 'get'
  })
}

export function createMcpTool(data) {
  return request({
    url: '/api/ai/mcp',
    method: 'post',
    data
  })
}

export function updateMcpTool(id, data) {
  return request({
    url: `/api/ai/mcp/${id}`,
    method: 'put',
    data
  })
}

export function deleteMcpTool(id) {
  return request({
    url: `/api/ai/mcp/${id}`,
    method: 'delete'
  })
}

export function toggleMcpTool(id, enabled) {
  return request({
    url: `/api/ai/mcp/${id}/toggle`,
    method: 'post',
    params: { enabled }
  })
}

export function executeMcpTool(data) {
  return request({
    url: '/api/ai/mcp/execute',
    method: 'post',
    data
  })
}
