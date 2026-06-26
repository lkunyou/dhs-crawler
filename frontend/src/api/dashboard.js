import request from '@/utils/request'

export function getDashboardStats() {
  return request({
    url: '/dashboard/stats',
    method: 'get'
  })
}

export function getGradeDistribution() {
  return request({
    url: '/dashboard/grade-distribution',
    method: 'get'
  })
}

export function getSourceDistribution() {
  return request({
    url: '/dashboard/source-distribution',
    method: 'get'
  })
}

export function getFunnelData() {
  return request({
    url: '/dashboard/funnel',
    method: 'get'
  })
}
