import request from '@/utils/request'

export function getAiModels() {
  return request({
    url: '/api/ai/models',
    method: 'get'
  })
}

export function getEnabledAiModels() {
  return request({
    url: '/api/ai/models/enabled',
    method: 'get'
  })
}

export function getAiModel(id) {
  return request({
    url: `/api/ai/models/${id}`,
    method: 'get'
  })
}

export function getAiModelByProvider(provider) {
  return request({
    url: `/api/ai/models/provider/${provider}`,
    method: 'get'
  })
}

export function createAiModel(data) {
  return request({
    url: '/api/ai/models',
    method: 'post',
    data
  })
}

export function updateAiModel(id, data) {
  return request({
    url: `/api/ai/models/${id}`,
    method: 'put',
    data
  })
}

export function deleteAiModel(id) {
  return request({
    url: `/api/ai/models/${id}`,
    method: 'delete'
  })
}

export function toggleAiModel(id, enabled) {
  return request({
    url: `/api/ai/models/${id}/toggle`,
    method: 'post',
    params: { enabled }
  })
}

export function chatWithAi(data) {
  return request({
    url: '/api/ai/models/chat',
    method: 'post',
    data
  })
}
