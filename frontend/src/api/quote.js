import request from '@/utils/request'

export function getQuotes(params) {
  return request({
    url: '/quotes',
    method: 'get',
    params
  })
}

export function getQuote(id) {
  return request({
    url: `/quotes/${id}`,
    method: 'get'
  })
}

export function createQuote(data) {
  return request({
    url: '/quotes',
    method: 'post',
    data
  })
}

export function updateQuote(id, data) {
  return request({
    url: `/quotes/${id}`,
    method: 'put',
    data
  })
}

export function deleteQuote(id) {
  return request({
    url: `/quotes/${id}`,
    method: 'delete'
  })
}