import request from '@/utils/request'

export function chat(data) {
  return request({
    url: '/api/ai/chat',
    method: 'post',
    data
  })
}

export function getConversations() {
  return request({
    url: '/api/ai/conversations',
    method: 'get'
  })
}

export function getMessages(conversationId) {
  return request({
    url: `/api/ai/conversations/${conversationId}/messages`,
    method: 'get'
  })
}

export function createConversation(title) {
  return request({
    url: '/api/ai/conversations',
    method: 'post',
    params: { title }
  })
}

export function deleteConversation(id) {
  return request({
    url: `/api/ai/conversations/${id}`,
    method: 'delete'
  })
}

export function executeAgent(data) {
  return request({
    url: '/api/ai/agent/execute',
    method: 'post',
    data
  })
}

export function getAgentStatus(taskId) {
  return request({
    url: `/api/ai/agent/status/${taskId}`,
    method: 'get'
  })
}

export function getSkills() {
  return request({
    url: '/api/ai/skills',
    method: 'get'
  })
}

export function createSkill(data) {
  return request({
    url: '/api/ai/skills',
    method: 'post',
    data
  })
}

export function updateSkill(id, data) {
  return request({
    url: `/api/ai/skills/${id}`,
    method: 'put',
    data
  })
}

export function deleteSkill(id) {
  return request({
    url: `/api/ai/skills/${id}`,
    method: 'delete'
  })
}
