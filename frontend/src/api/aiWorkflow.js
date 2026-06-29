import request from '@/utils/request'

export function getWorkflows() {
  return request({
    url: '/ai/workflow',
    method: 'get'
  })
}

export function getEnabledWorkflows() {
  return request({
    url: '/ai/workflow/enabled',
    method: 'get'
  })
}

export function getWorkflow(id) {
  return request({
    url: `/ai/workflow/${id}`,
    method: 'get'
  })
}

export function getWorkflowByAgentType(agentType) {
  return request({
    url: `/ai/workflow/agent/${agentType}`,
    method: 'get'
  })
}

export function createWorkflow(data) {
  return request({
    url: '/ai/workflow',
    method: 'post',
    data
  })
}

export function updateWorkflow(id, data) {
  return request({
    url: `/ai/workflow/${id}`,
    method: 'put',
    data
  })
}

export function deleteWorkflow(id) {
  return request({
    url: `/ai/workflow/${id}`,
    method: 'delete'
  })
}

export function toggleWorkflow(id, enabled) {
  return request({
    url: `/ai/workflow/${id}/toggle`,
    method: 'post',
    params: { enabled }
  })
}

export function getWorkflowExecutions(id) {
  return request({
    url: `/ai/workflow/${id}/executions`,
    method: 'get'
  })
}

export function getAllExecutions() {
  return request({
    url: '/ai/workflow/executions',
    method: 'get'
  })
}

export function getExecution(execId) {
  return request({
    url: `/ai/workflow/execution/${execId}`,
    method: 'get'
  })
}

export function executeWorkflow(id, input) {
  return request({
    url: `/ai/workflow/${id}/execute`,
    method: 'post',
    data: input
  })
}

export function stopExecution(execId) {
  return request({
    url: `/ai/workflow/execution/${execId}/stop`,
    method: 'post'
  })
}
