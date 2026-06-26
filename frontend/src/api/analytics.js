import request from '@/utils/request'

export function getEmailStats() {
  return request({
    url: '/analytics/email-stats',
    method: 'get'
  })
}

export function getWhatsappStats() {
  return request({
    url: '/analytics/whatsapp-stats',
    method: 'get'
  })
}

export function getSourceQuality() {
  return request({
    url: '/analytics/source-quality',
    method: 'get'
  })
}

export function getTrend(days = 30) {
  return request({
    url: '/analytics/trend',
    method: 'get',
    params: { days }
  })
}

export function getFunnel() {
  return request({
    url: '/analytics/funnel',
    method: 'get'
  })
}
