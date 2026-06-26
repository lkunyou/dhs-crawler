import request from '@/utils/request'

export function getSysUserList() {
  return request.get('/sys-users')
}

export function createSysUser(data) {
  return request.post('/sys-users', data)
}

export function updateSysUser(id, data) {
  return request.put(`/sys-users/${id}`, data)
}

export function deleteSysUser(id) {
  return request.delete(`/sys-users/${id}`)
}
