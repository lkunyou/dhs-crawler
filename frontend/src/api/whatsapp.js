import request from '@/utils/request'

export function getWhatsappRecords(companyId) {
  return request.get(`/whatsapp/records/${companyId}`)
}

export function sendWhatsappText(data) {
  return request.post('/whatsapp/send-text', data)
}
