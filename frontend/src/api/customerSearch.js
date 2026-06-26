import request from '@/utils/request'

export function searchCompanies(params) {
  return request({
    url: '/customer-search/search',
    method: 'get',
    params
  })
}

export function batchSearchCompanies(keywords, source, country) {
  return request({
    url: '/customer-search/batch-search',
    method: 'post',
    params: { source, country },
    data: keywords
  })
}

export function importCompany(data) {
  return request({
    url: '/companies',
    method: 'post',
    data
  })
}