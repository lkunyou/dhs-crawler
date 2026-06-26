import request from '@/utils/request'

export function getFollowUpRecords(companyId) {
  return request.get(`/crm/follow-up/${companyId}`)
}

export function addFollowUpRecord(data) {
  return request.post('/crm/follow-up', data)
}
