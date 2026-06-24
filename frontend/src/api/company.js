import request from '@/utils/request'

export function getCompanies(params) {
  return request({
    url: '/companies',
    method: 'get',
    params
  })
}

export function getCompany(id) {
  return request({
    url: `/companies/${id}`,
    method: 'get'
  })
}

export function createCompany(data) {
  return request({
    url: '/companies',
    method: 'post',
    data
  })
}

export function updateCompany(id, data) {
  return request({
    url: `/companies/${id}`,
    method: 'put',
    data
  })
}

export function deleteCompany(id) {
  return request({
    url: `/companies/${id}`,
    method: 'delete'
  })
}

export function updateLeadScore(id) {
  return request({
    url: `/companies/${id}/score`,
    method: 'post'
  })
}

export function getGradeStats() {
  return request({
    url: '/companies/stats/grade',
    method: 'get'
  })
}

export function getStatusStats() {
  return request({
    url: '/companies/stats/status',
    method: 'get'
  })
}

export function getSourceStats() {
  return request({
    url: '/companies/stats/source',
    method: 'get'
  })
}
