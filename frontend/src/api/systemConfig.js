import request from '@/utils/request'

export function getConfigList() {
  return request.get('/system-configs')
}

export function createConfig(data) {
  return request.post('/system-configs', data)
}

export function updateConfig(id, data) {
  return request.put(`/system-configs/${id}`, data)
}

export function deleteConfig(id) {
  return request.delete(`/system-configs/${id}`)
}

export function getConfigByKey(configKey) {
  return request.get(`/system-configs/key/${configKey}`)
}

export function initDefaultConfigs() {
  return request.post('/system-configs/init-defaults')
}
