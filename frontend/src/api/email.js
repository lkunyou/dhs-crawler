import request from '@/utils/request'

export function sendEmail(data) {
  return request({
    url: '/email/send',
    method: 'post',
    data
  })
}

export function sendCustomEmail(data) {
  return request({
    url: '/email/send-custom',
    method: 'post',
    data
  })
}

export function getRepliesByEmailId(emailId) {
  return request({
    url: `/email/replies/${emailId}`,
    method: 'get'
  })
}

export function sendBatchEmail(data) {
  return request({
    url: '/email/send-batch',
    method: 'post',
    data
  })
}

export function getEmailRecords(companyId) {
  return request({
    url: `/email/records/${companyId}`,
    method: 'get'
  })
}

export function getAllEmailRecords() {
  return request({
    url: '/email/records',
    method: 'get'
  })
}

export function getEmailStats() {
  return request({
    url: '/email/stats',
    method: 'get'
  })
}

export function trackOpen(trackingId) {
  return request({
    url: '/email/track/open',
    method: 'get',
    params: { trackingId }
  })
}

export function getInbox() {
  return request({
    url: '/email/inbox',
    method: 'get'
  })
}

export function getLatestEmails(limit = 20) {
  return request({
    url: '/email/inbox/latest',
    method: 'get',
    params: { limit }
  })
}

export function getUnreadEmails() {
  return request({
    url: '/email/inbox/unread',
    method: 'get'
  })
}

export function getUnreadCount() {
  return request({
    url: '/email/inbox/count',
    method: 'get'
  })
}

export function getEmailById(id) {
  return request({
    url: `/email/inbox/${id}`,
    method: 'get'
  })
}

export function markAsRead(id) {
  return request({
    url: `/email/inbox/${id}/read`,
    method: 'post'
  })
}

export function markAsStarred(id, starred) {
  return request({
    url: `/email/inbox/${id}/star`,
    method: 'post',
    params: { starred }
  })
}

export function setPriority(id, priority) {
  return request({
    url: `/email/inbox/${id}/priority`,
    method: 'post',
    params: { priority }
  })
}

export function markAsReplied(id) {
  return request({
    url: `/email/inbox/${id}/replied`,
    method: 'post'
  })
}

export function deleteEmail(id) {
  return request({
    url: `/email/inbox/${id}`,
    method: 'delete'
  })
}

export function fetchEmails() {
  return request({
    url: '/email/inbox/fetch',
    method: 'post'
  })
}

export function getEmailTemplates() {
  return request({
    url: '/email/templates',
    method: 'get'
  })
}

export function getEmailTemplateById(id) {
  return request({
    url: `/email/templates/${id}`,
    method: 'get'
  })
}

export function createEmailTemplate(data) {
  return request({
    url: '/email/templates',
    method: 'post',
    data
  })
}

export function updateEmailTemplate(id, data) {
  return request({
    url: `/email/templates/${id}`,
    method: 'put',
    data
  })
}

export function deleteEmailTemplate(id) {
  return request({
    url: `/email/templates/${id}`,
    method: 'delete'
  })
}