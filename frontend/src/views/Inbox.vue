<template>
  <div class="inbox-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>收件箱</span>
          <div class="header-actions">
            <el-button type="primary" @click="fetchNewEmails" size="small">获取新邮件</el-button>
            <el-button @click="loadLatest20" size="small">最新20条</el-button>
            <el-button @click="refreshInbox" size="small">刷新</el-button>
          </div>
        </div>
      </template>

      <div class="search-form">
        <el-form :model="searchForm" inline class="search-inline-form">
          <el-form-item label="关键词">
            <el-input 
              v-model="searchForm.keyword" 
              placeholder="姓名/邮箱/标题/内容" 
              clearable 
              @keyup.enter="handleSearch"
            />
          </el-form-item>
          <el-form-item label="发件人">
            <el-input 
              v-model="searchForm.fromName" 
              placeholder="发件人姓名" 
              clearable 
            />
          </el-form-item>
          <el-form-item label="邮箱">
            <el-input 
              v-model="searchForm.fromEmail" 
              placeholder="发件人邮箱" 
              clearable 
            />
          </el-form-item>
          <el-form-item label="标题">
            <el-input 
              v-model="searchForm.subject" 
              placeholder="邮件标题" 
              clearable 
            />
          </el-form-item>
          <el-form-item label="日期范围">
            <el-date-picker
              v-model="searchForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="inbox-content">
        <div class="email-list">
          <div 
            v-for="email in emails" 
            :key="email.id" 
            :class="['email-item', { active: selectedEmail?.id === email.id, unread: !email.isRead }]"
            @click="selectEmail(email)"
          >
            <div class="email-star" @click.stop="toggleStar(email)">
              <el-icon :size="16" :color="email.isStarred ? '#f59e0b' : '#94a3b8'"><Star /></el-icon>
            </div>
            <div class="email-content">
              <div class="email-header">
                <div class="email-from-wrapper">
                  <span class="email-from">{{ email.fromName || email.fromEmail }}</span>
                  <el-tag 
                    v-if="email.isReplied"
                    type="success" 
                    size="small" 
                    class="priority-tag"
                    effect="plain"
                  >
                    已回复
                  </el-tag>
                  <el-tag 
                    v-else
                    :type="getPriorityType(email.priority)" 
                    size="small" 
                    class="priority-tag"
                    effect="plain"
                  >
                    {{ getPriorityLabel(email.priority) }}
                  </el-tag>
                </div>
                <span class="email-time">{{ formatTime(email.createdAt) }}</span>
              </div>
              <div class="email-subject">{{ email.subject }}</div>
              <div class="email-preview-text">{{ truncateContent(email.content) }}</div>
            </div>
            <div class="email-actions" @click.stop>
              <el-button 
                type="primary" 
                size="small" 
                link 
                @click="viewEmailDetail(email)"
              >
                查看详情
              </el-button>
            </div>
          </div>
          
          <div v-if="emails.length === 0" class="empty-state">
            <el-icon :size="48" color="#cbd5e1"><Message /></el-icon>
            <p>暂无邮件</p>
            <el-button type="primary" @click="fetchNewEmails">获取新邮件</el-button>
          </div>
        </div>

        <div class="email-detail" v-if="selectedEmail">
          <el-card>
            <template #header>
              <div class="detail-header">
                <h3>{{ selectedEmail.subject }}</h3>
                <div class="detail-actions">
                  <el-button type="primary" @click="openReplyDialog(selectedEmail)" size="small">
                    <el-icon><ChatDotRound /></el-icon>
                    回复
                  </el-button>
                  <el-button @click="loadReplies(selectedEmail.id)" size="small" :type="showReplies ? 'success' : 'default'">
                    <el-icon><Plus /></el-icon>
                    回复列表
                  </el-button>
                  <el-dropdown @command="handlePriorityChange" trigger="click">
                    <el-button size="small">
                      <el-icon><Flag /></el-icon>
                      标记级别
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="urgent">
                          <el-tag type="danger" size="small">紧急</el-tag>
                        </el-dropdown-item>
                        <el-dropdown-item command="high">
                          <el-tag type="warning" size="small">高</el-tag>
                        </el-dropdown-item>
                        <el-dropdown-item command="normal">
                          <el-tag type="info" size="small">普通</el-tag>
                        </el-dropdown-item>
                        <el-dropdown-item command="low">
                          <el-tag type="success" size="small">低</el-tag>
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                  <el-button @click="toggleStar(selectedEmail)" size="small">
                    <el-icon :size="16" :color="selectedEmail.isStarred ? '#f59e0b' : '#94a3b8'"><Star /></el-icon>
                  </el-button>
                  <el-button @click="handleDeleteEmail(selectedEmail.id)" size="small" type="danger">
                    <el-icon :size="16"><Delete /></el-icon>
                  </el-button>
                </div>
              </div>
            </template>
            
            <div class="detail-info">
              <div class="info-row">
                <span class="label">发件人:</span>
                <span class="value">{{ selectedEmail.fromName || selectedEmail.fromEmail }}</span>
                <el-tag v-if="selectedEmail.isReplied" type="success" size="small" style="margin-left: 10px">已回复</el-tag>
                <el-tag v-else :type="getPriorityType(selectedEmail.priority)" size="small" style="margin-left: 10px">{{ getPriorityLabel(selectedEmail.priority) }}</el-tag>
              </div>
              <div class="info-row">
                <span class="label">收件人:</span>
                <span class="value">{{ selectedEmail.toEmail }}</span>
              </div>
              <div class="info-row">
                <span class="label">时间:</span>
                <span class="value">{{ formatFullTime(selectedEmail.createdAt) }}</span>
              </div>
            </div>
            
            <div class="email-body" v-html="selectedEmail.content || '<p style=\'color:#999;text-align:center;\'>邮件内容为空</p>'"></div>
            
            <!-- 回复列表面板 -->
            <div v-if="showReplies" class="replies-panel">
              <div class="replies-header">
                <span>回复列表 ({{ repliesList.length }})</span>
                <el-button size="small" @click="showReplies = false">收起</el-button>
              </div>
              <div class="replies-list">
                <div v-if="repliesList.length === 0" class="empty-replies">暂无回复</div>
                <div 
                  v-for="reply in repliesList" 
                  :key="reply.id" 
                  class="reply-item"
                  @click="viewReplyDetail(reply)"
                >
                  <div class="reply-subject">{{ reply.subject }}</div>
                  <div class="reply-info">
                    <span>发给: {{ reply.recipientEmail }}</span>
                    <span>{{ formatFullTime(reply.sentAt) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </el-card>
        </div>

        <div class="email-detail empty-detail" v-else>
          <el-icon :size="64" color="#e2e8f0"><MessageBox /></el-icon>
          <p>选择一封邮件查看详情</p>
        </div>
      </div>
    </el-card>

    <!-- 邮件详情弹窗 -->
    <el-dialog
      v-model="emailDialogVisible"
      :title="dialogEmail?.subject"
      width="800px"
      destroy-on-close
    >
      <div v-if="dialogEmail" class="dialog-email-content">
        <div class="dialog-email-info">
          <div class="info-row">
            <span class="label">发件人:</span>
            <span class="value">{{ dialogEmail.fromName || dialogEmail.fromEmail }}</span>
          </div>
          <div class="info-row">
            <span class="label">收件人:</span>
            <span class="value">{{ dialogEmail.toEmail }}</span>
          </div>
          <div class="info-row">
            <span class="label">时间:</span>
            <span class="value">{{ formatFullTime(dialogEmail.createdAt) }}</span>
          </div>
          <div class="info-row">
            <span class="label">级别:</span>
            <el-tag v-if="dialogEmail.isReplied" type="success" size="small">已回复</el-tag>
            <el-tag v-else :type="getPriorityType(dialogEmail.priority)" size="small">{{ getPriorityLabel(dialogEmail.priority) }}</el-tag>
          </div>
        </div>
        <el-divider />
        <div class="dialog-email-body" v-html="dialogEmail.content"></div>
      </div>
      <template #footer>
        <el-button type="primary" @click="openReplyDialog(dialogEmail)">
          <el-icon><ChatDotRound /></el-icon>
          回复
        </el-button>
        <el-dropdown @command="handleDialogPriorityChange" trigger="click" style="margin-right: 10px">
          <el-button>
            <el-icon><Flag /></el-icon>
            标记级别
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="urgent">
                <el-tag type="danger" size="small">紧急</el-tag>
              </el-dropdown-item>
              <el-dropdown-item command="high">
                <el-tag type="warning" size="small">高</el-tag>
              </el-dropdown-item>
              <el-dropdown-item command="normal">
                <el-tag type="info" size="small">普通</el-tag>
              </el-dropdown-item>
              <el-dropdown-item command="low">
                <el-tag type="success" size="small">低</el-tag>
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-button @click="toggleStar(dialogEmail)">
          <el-icon :color="dialogEmail?.isStarred ? '#f59e0b' : '#94a3b8'"><Star /></el-icon>
          {{ dialogEmail?.isStarred ? '取消标星' : '标星' }}
        </el-button>
        <el-button type="primary" @click="emailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 回复邮件弹窗 -->
    <el-dialog
      v-model="replyDialogVisible"
      title="回复邮件"
      width="700px"
      destroy-on-close
    >
      <el-form :model="replyForm" label-width="80px">
        <el-form-item label="收件人">
          <el-input v-model="replyForm.toEmail" placeholder="请输入收件人邮箱" />
        </el-form-item>
        <el-form-item label="主题">
          <el-input v-model="replyForm.subject" placeholder="请输入邮件主题" />
        </el-form-item>
        <el-form-item label="内容">
          <el-input
            v-model="replyForm.content"
            type="textarea"
            :rows="10"
            placeholder="请输入邮件内容"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="replyDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="sendReply" :loading="replyLoading">发送</el-button>
      </template>
    </el-dialog>

    <!-- 回复详情弹窗 -->
    <el-dialog
      v-model="replyDetailVisible"
      title="回复详情"
      width="700px"
      destroy-on-close
    >
      <div v-if="selectedReply" class="reply-detail-content">
        <div class="info-row">
          <span class="label">主题:</span>
          <span class="value">{{ selectedReply.subject }}</span>
        </div>
        <div class="info-row">
          <span class="label">发给:</span>
          <span class="value">{{ selectedReply.recipientEmail }}</span>
        </div>
        <div class="info-row">
          <span class="label">状态:</span>
          <el-tag :type="selectedReply.status === 'Sent' ? 'success' : 'danger'" size="small">
            {{ selectedReply.status === 'Sent' ? '已发送' : selectedReply.status }}
          </el-tag>
        </div>
        <div class="info-row">
          <span class="label">时间:</span>
          <span class="value">{{ formatFullTime(selectedReply.sentAt) }}</span>
        </div>
        <el-divider />
        <div class="reply-content">{{ selectedReply.content }}</div>
      </div>
      <template #footer>
        <el-button type="primary" @click="replyDetailVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Star, Delete, Message, MessageBox, Flag, ChatDotRound, Plus } from '@element-plus/icons-vue'
import { sendCustomEmail } from '@/api/email'
import { getInbox, getLatestEmails, markAsRead, markAsStarred, setPriority, deleteEmail, fetchEmails, getEmailById, markAsReplied, getRepliesByEmailId } from '@/api/email'
import { findCompanyByEmail } from '@/api/company'

const emails = ref([])
const selectedEmail = ref(null)
const loading = ref(false)
const emailDialogVisible = ref(false)
const dialogEmail = ref(null)
const replyDialogVisible = ref(false)
const replyForm = ref({
  toEmail: '',
  subject: '',
  content: '',
  inReplyToEmailId: null,
  companyId: null
})
const replyLoading = ref(false)
const replyingToEmail = ref(null)
const showReplies = ref(false)
const repliesList = ref([])
const selectedReply = ref(null)
const replyDetailVisible = ref(false)

const searchForm = ref({
  keyword: '',
  fromName: '',
  fromEmail: '',
  subject: '',
  dateRange: null
})

onMounted(() => {
  loadInbox()
})

async function loadInbox(params = {}) {
  loading.value = true
  try {
    const res = await getInbox(params)
    emails.value = res.data
  } catch (e) {
    console.error(e)
    ElMessage.error('加载邮件失败')
  } finally {
    loading.value = false
  }
}

async function handleSearch() {
  const params = {}
  if (searchForm.value.keyword) {
    params.keyword = searchForm.value.keyword
  }
  if (searchForm.value.fromName) {
    params.fromName = searchForm.value.fromName
  }
  if (searchForm.value.fromEmail) {
    params.fromEmail = searchForm.value.fromEmail
  }
  if (searchForm.value.subject) {
    params.subject = searchForm.value.subject
  }
  if (searchForm.value.dateRange && searchForm.value.dateRange.length === 2) {
    params.startDate = searchForm.value.dateRange[0]
    params.endDate = searchForm.value.dateRange[1]
  }
  selectedEmail.value = null
  await loadInbox(params)
}

function handleReset() {
  searchForm.value = {
    keyword: '',
    fromName: '',
    fromEmail: '',
    subject: '',
    dateRange: null
  }
  selectedEmail.value = null
  loadInbox()
}

async function loadReplies(emailId) {
  try {
    const res = await getRepliesByEmailId(emailId)
    repliesList.value = res.data || []
    showReplies.value = true
  } catch (e) {
    console.error(e)
    ElMessage.error('加载回复列表失败')
  }
}

function viewReplyDetail(reply) {
  selectedReply.value = reply
  replyDetailVisible.value = true
}

async function refreshInbox() {
  await loadInbox()
}

async function loadLatest20() {
  loading.value = true
  try {
    const res = await getLatestEmails(20)
    emails.value = res.data
    selectedEmail.value = null
  } catch (e) {
    console.error(e)
    ElMessage.error('加载最新邮件失败')
  } finally {
    loading.value = false
  }
}

async function fetchNewEmails() {
  loading.value = true
  try {
    await fetchEmails()
    ElMessage.success('邮件获取任务已启动')
    setTimeout(() => loadInbox(), 3000)
  } catch (e) {
    console.error(e)
    ElMessage.error('获取邮件失败')
  } finally {
    loading.value = false
  }
}

async function selectEmail(email) {
  selectedEmail.value = email
  if (!email.isRead) {
    await markAsRead(email.id)
    email.isRead = true
  }
}

async function viewEmailDetail(email) {
  // 先标记已读
  if (!email.isRead) {
    await markAsRead(email.id)
    email.isRead = true
  }
  // 获取完整邮件内容
  try {
    const res = await getEmailById(email.id)
    console.log('Email detail API response:', res)
    console.log('Email content:', res.data?.content)
    selectedEmail.value = res.data
  } catch (e) {
    console.error(e)
    ElMessage.error('加载邮件详情失败')
  }
}

function openEmailDialog(email) {
  dialogEmail.value = email
  emailDialogVisible.value = true
  if (!email.isRead) {
    markAsRead(email.id)
    email.isRead = true
  }
}

async function toggleStar(email) {
  const newStarred = !email.isStarred
  try {
    await markAsStarred(email.id, newStarred)
    email.isStarred = newStarred
    ElMessage.success(newStarred ? '已标星' : '已取消标星')
  } catch (e) {
    console.error(e)
    ElMessage.error('操作失败')
  }
}

async function handlePriorityChange(command) {
  if (!selectedEmail.value) return
  try {
    await setPriority(selectedEmail.value.id, command)
    selectedEmail.value.priority = command
    ElMessage.success('级别已更新')
  } catch (e) {
    console.error(e)
    ElMessage.error('更新失败')
  }
}

async function handleDialogPriorityChange(command) {
  if (!dialogEmail.value) return
  try {
    await setPriority(dialogEmail.value.id, command)
    dialogEmail.value.priority = command
    // 同步更新列表中的邮件
    const email = emails.value.find(e => e.id === dialogEmail.value.id)
    if (email) email.priority = command
    ElMessage.success('级别已更新')
  } catch (e) {
    console.error(e)
    ElMessage.error('更新失败')
  }
}

async function handleDeleteEmail(id) {
  try {
    await deleteEmail(id)
    emails.value = emails.value.filter(e => e.id !== id)
    if (selectedEmail.value?.id === id) {
      selectedEmail.value = null
    }
    if (dialogEmail.value?.id === id) {
      dialogEmail.value = null
      emailDialogVisible.value = false
    }
    ElMessage.success('已删除')
  } catch (e) {
    console.error(e)
    ElMessage.error('删除失败')
  }
}

function getPriorityType(priority) {
  switch (priority) {
    case 'urgent': return 'danger'
    case 'high': return 'warning'
    case 'normal': return 'info'
    case 'low': return 'success'
    default: return 'info'
  }
}

function getPriorityLabel(priority) {
  switch (priority) {
    case 'urgent': return '紧急'
    case 'high': return '高'
    case 'normal': return '普通'
    case 'low': return '低'
    default: return '普通'
  }
}

function formatTime(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) {
    return '刚刚'
  } else if (diff < 3600000) {
    return `${Math.floor(diff / 60000)}分钟前`
  } else if (diff < 86400000) {
    return `${Math.floor(diff / 3600000)}小时前`
  } else {
    return `${date.getMonth() + 1}/${date.getDate()}`
  }
}

function formatFullTime(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

function truncateContent(content) {
  if (!content) return ''
  const text = content.replace(/<[^>]*>/g, '')
  return text.length > 100 ? text.substring(0, 100) + '...' : text
}

async function openReplyDialog(email) {
  replyingToEmail.value = email
  const replyTo = email.fromEmail
  const subject = email.subject.startsWith('Re:') ? email.subject : 'Re: ' + email.subject
  const originalContent = email.content ? email.content.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').replace(/&lt;/g, '<').replace(/&gt;/g, '>') : ''
  
  let companyId = email.companyId || null
  if (!companyId && replyTo) {
    try {
      const res = await findCompanyByEmail(replyTo)
      if (res.data) {
        companyId = res.data.id
      }
    } catch (e) {
      console.error('查找公司失败:', e)
    }
  }
  
  replyForm.value = {
    toEmail: replyTo,
    subject: subject,
    content: '\n\n\n--- Original Message ---\n' + originalContent,
    inReplyToEmailId: email.id,
    companyId: companyId
  }
  replyDialogVisible.value = true
}

async function sendReply() {
  if (!replyForm.value.toEmail) {
    ElMessage.warning('请填写收件人邮箱')
    return
  }
  if (!replyForm.value.content.trim()) {
    ElMessage.warning('请填写邮件内容')
    return
  }
  replyLoading.value = true
  try {
    await sendCustomEmail({
      toEmail: replyForm.value.toEmail,
      subject: replyForm.value.subject,
      content: replyForm.value.content,
      html: false,
      inReplyToEmailId: replyForm.value.inReplyToEmailId,
      companyId: replyForm.value.companyId
    })
    // 标记原邮件为已回复
    if (replyingToEmail.value) {
      await markAsReplied(replyingToEmail.value.id)
      replyingToEmail.value.isReplied = true
      // 同步更新列表中的邮件
      const email = emails.value.find(e => e.id === replyingToEmail.value.id)
      if (email) email.isReplied = true
    }
    ElMessage.success('回复邮件已发送')
    replyDialogVisible.value = false
  } catch (e) {
    console.error(e)
    ElMessage.error('发送失败')
  } finally {
    replyLoading.value = false
  }
}
</script>

<style scoped>
.inbox-page {
  padding: 20px;
  height: calc(100vh - 52px);
  box-sizing: border-box;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.search-form {
  padding: 16px;
  background-color: #f8fafc;
  border-radius: 8px;
  margin-bottom: 20px;
}

.search-inline-form {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.inbox-content {
  display: flex;
  gap: 20px;
  height: calc(100% - 140px);
  margin-top: 20px;
}

.email-list {
  width: 400px;
  border: 1px solid #e8f4f8;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.email-item {
  display: flex;
  gap: 12px;
  padding: 12px 16px;
  border-bottom: 1px solid #f1f5f9;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.email-item:hover {
  background-color: #eff6ff;
}

.email-item.active {
  background-color: #dbeafe;
}

.email-item.unread {
  background-color: #fef3c7;
}

.email-star {
  flex-shrink: 0;
  display: flex;
  align-items: flex-start;
  padding-top: 4px;
}

.email-content {
  flex: 1;
  min-width: 0;
}

.email-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.email-from-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 0;
}

.email-from {
  font-weight: 500;
  color: #1e293b;
  font-size: 13px;
}

.priority-tag {
  flex-shrink: 0;
}

.email-time {
  font-size: 12px;
  color: #64748b;
  flex-shrink: 0;
  margin-left: 8px;
}

.email-subject {
  font-size: 13px;
  color: #334155;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.email-preview-text {
  font-size: 12px;
  color: #64748b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.email-actions {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  padding-left: 8px;
}

.email-detail {
  flex: 1;
  border: 1px solid #e8f4f8;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.empty-detail {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}

.empty-detail p {
  margin-top: 16px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-header h3 {
  margin: 0;
  font-size: 16px;
}

.detail-actions {
  display: flex;
  gap: 8px;
}

.detail-info {
  padding: 16px;
  background-color: #f8fafc;
  border-bottom: 1px solid #e8f4f8;
}

.info-row {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.info-row:last-child {
  margin-bottom: 0;
}

.info-row .label {
  color: #64748b;
  font-size: 13px;
  width: 60px;
  flex-shrink: 0;
}

.info-row .value {
  color: #1e293b;
  font-size: 13px;
}

.email-body {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
  font-size: 14px;
  line-height: 1.6;
  color: #334155;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #94a3b8;
}

.empty-state p {
  margin: 16px 0 24px;
}

.dialog-email-content {
  max-height: 600px;
  overflow-y: auto;
}

.dialog-email-info {
  padding: 10px 0;
}

.dialog-email-info .info-row {
  margin-bottom: 12px;
}

.dialog-email-info .label {
  width: 80px;
}

.dialog-email-body {
  padding: 20px 0;
  font-size: 14px;
  line-height: 1.8;
  color: #334155;
}

.replies-panel {
  border-top: 1px solid #e8f4f8;
  padding: 16px;
  background-color: #f8fafc;
}

.replies-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-weight: 500;
  color: #334155;
}

.replies-list {
  max-height: 300px;
  overflow-y: auto;
}

.empty-replies {
  text-align: center;
  color: #94a3b8;
  padding: 20px;
}

.reply-item {
  padding: 12px;
  border-bottom: 1px solid #f1f5f9;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

.reply-item:hover {
  background-color: #e0f2fe;
}

.reply-item:last-child {
  border-bottom: none;
}

.reply-subject {
  font-size: 13px;
  color: #1e293b;
  margin-bottom: 4px;
}

.reply-info {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #64748b;
}

.reply-detail-content {
  padding: 10px 0;
}

.reply-content {
  padding: 16px;
  background-color: #f8fafc;
  border-radius: 4px;
  white-space: pre-wrap;
  font-size: 14px;
  line-height: 1.6;
  color: #334155;
  max-height: 400px;
  overflow-y: auto;
}
</style>