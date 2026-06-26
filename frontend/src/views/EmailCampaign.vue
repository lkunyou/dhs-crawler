<template>
  <div class="email-campaign">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>发送邮件</span>
          <el-button type="primary" @click="openSendDialog" size="small">发送邮件</el-button>
        </div>
      </template>

      <!-- 查询条件 -->
      <el-row :gutter="20" class="search-row">
        <el-col :span="6">
          <el-input v-model="searchForm.email" placeholder="按邮箱查询" clearable />
        </el-col>
        <el-col :span="6">
          <el-input v-model="searchForm.username" placeholder="按用户名查询" clearable />
        </el-col>
        <el-col :span="8">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 100%"
          />
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-col>
      </el-row>

      <!-- 发送记录列表 -->
      <el-table :data="sendRecords" border class="records-table">
        <el-table-column type="index" label="序号" width="60" />
        <el-table-column prop="recipientEmail" label="收件人" min-width="250">
          <template #default="{ row }">
            <div style="font-weight: 500;">{{ row.recipientEmail }}</div>
            <div v-if="row.recipientName">
              <el-link type="primary" style="font-size: 12px;" @click="viewRecipient(row)">{{ row.recipientName }}</el-link>
            </div>
            <div v-if="row.companyName" style="font-size: 12px; color: #909399;">{{ row.companyName }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="subject" label="邮件主题" min-width="200" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getRecordStatusType(row.status)">{{ getRecordStatusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sentAt" label="发送时间" width="180" />
        <el-table-column prop="openedAt" label="打开时间" width="180" />
        <el-table-column prop="repliedAt" label="回复时间" width="180" />
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewDetail(row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadRecords"
          @current-change="loadRecords"
        />
      </div>
    </el-card>

    <!-- 发送邮件弹窗 -->
    <el-dialog v-model="sendDialogVisible" title="发送邮件" width="700px">
      <el-form :model="emailForm" label-width="100px">
        <el-form-item label="目标客户" required>
          <el-select v-model="emailForm.targetType" @change="handleTargetTypeChange" placeholder="选择发送方式">
            <el-option label="单个客户" value="single" />
            <el-option label="客户等级筛选" value="grade" />
            <el-option label="全部客户" value="all" />
          </el-select>
        </el-form-item>
        
        <el-form-item v-if="emailForm.targetType === 'single'" label="选择客户" required>
          <el-select v-model="emailForm.companyId" filterable placeholder="搜索客户" style="width: 100%" @change="handleCompanySelect">
            <el-option v-for="c in companies" :key="c.id" :label="c.companyName + (c.email ? ` (${c.email})` : '')" :value="c.id" />
          </el-select>
        </el-form-item>
        
        <el-form-item v-if="selectedCompany" label="客户信息">
          <el-card size="small">
            <div><strong>公司名称：</strong>{{ selectedCompany.companyName }}</div>
            <div><strong>邮箱：</strong>{{ selectedCompany.email || '-' }}</div>
            <div><strong>电话：</strong>{{ selectedCompany.phone || '-' }}</div>
            <div><strong>客户等级：</strong>{{ selectedCompany.leadGrade || '-' }}</div>
          </el-card>
        </el-form-item>
        
        <el-form-item v-if="emailForm.targetType === 'grade'" label="客户等级">
          <el-select v-model="emailForm.gradeFilter" placeholder="选择等级">
            <el-option label="S级" value="S" />
            <el-option label="A级" value="A" />
            <el-option label="B级" value="B" />
            <el-option label="S/A级" value="SA" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="邮件模板" required>
          <el-select v-model="emailForm.templateId" @change="handleTemplateChange" placeholder="选择模板" style="width: 100%">
            <el-option v-for="t in templates" :key="t.id" :label="t.templateName" :value="t.id" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="预览">
          <div class="email-preview">
            <div v-if="emailForm.templateId" class="preview-header">
              <strong>主题:</strong> {{ templates.find(t => t.id === emailForm.templateId)?.subject || '-' }}
            </div>
            <div class="preview-content" v-html="emailPreview"></div>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="sendDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSend" :loading="sending">发送</el-button>
        <el-button type="warning" @click="handleBatchSend" :loading="sending" v-if="emailForm.targetType !== 'single'">批量发送</el-button>
      </template>
    </el-dialog>

    <!-- 收件人详情弹窗 -->
    <el-dialog v-model="recipientDialogVisible" title="收件人详情" width="500px">
      <div v-if="selectedRecipient" class="email-detail">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="收件人姓名">{{ selectedRecipient.recipientName || '-' }}</el-descriptions-item>
          <el-descriptions-item label="收件人邮箱">
            <a v-if="selectedRecipient.recipientEmail" :href="`mailto:${selectedRecipient.recipientEmail}`" class="el-link el-link--primary">{{ selectedRecipient.recipientEmail }}</a>
            <span v-else>-</span>
          </el-descriptions-item>
          <el-descriptions-item label="公司名称">{{ selectedRecipient.companyName || '-' }}</el-descriptions-item>
          <el-descriptions-item label="邮件主题">{{ selectedRecipient.subject || '-' }}</el-descriptions-item>
          <el-descriptions-item label="发送时间">{{ selectedRecipient.sentAt || '-' }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="recipientDialogVisible = false">关闭</el-button>
        <el-button v-if="selectedRecipient?.companyId" type="primary" @click="goToCompany(selectedRecipient.companyId)">查看客户详情</el-button>
      </template>
    </el-dialog>

    <!-- 邮件详情弹窗 -->
    <el-dialog v-model="detailDialogVisible" title="邮件详情" width="800px">
      <div v-if="selectedRecord" class="email-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="收件人邮箱">{{ selectedRecord.recipientEmail }}</el-descriptions-item>
          <el-descriptions-item label="收件人姓名">{{ selectedRecord.recipientName || '-' }}</el-descriptions-item>
          <el-descriptions-item label="邮件主题" :span="2">{{ selectedRecord.subject }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getRecordStatusType(selectedRecord.status)">{{ getRecordStatusLabel(selectedRecord.status) }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="模板ID">{{ selectedRecord.templateId }}</el-descriptions-item>
          <el-descriptions-item label="发送时间">{{ selectedRecord.sentAt || '-' }}</el-descriptions-item>
          <el-descriptions-item label="打开时间">{{ selectedRecord.openedAt || '-' }}</el-descriptions-item>
          <el-descriptions-item label="回复时间" :span="2">{{ selectedRecord.repliedAt || '-' }}</el-descriptions-item>
          <el-descriptions-item v-if="selectedRecord.status === 'Failed' && selectedRecord.errorMessage" label="失败原因" :span="2">
            <el-alert type="error" :closable="false" show-icon>
              {{ selectedRecord.errorMessage }}
            </el-alert>
          </el-descriptions-item>
          <el-descriptions-item label="邮件内容" :span="2">
            <div class="email-content" v-html="selectedRecord.content || '-'"></div>
          </el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { sendEmail, sendBatchEmail, getAllEmailRecords, getEmailTemplates } from '@/api/email'
import { getCompanies } from '@/api/company'

const route = useRoute()
const router = useRouter()
const sending = ref(false)
const sendDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const recipientDialogVisible = ref(false)
const selectedRecipient = ref(null)

// 查询表单
const searchForm = reactive({
  email: '',
  username: '',
  dateRange: null
})

// 分页
const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 发送邮件表单
const emailForm = reactive({
  targetType: 'single',
  companyId: null,
  gradeFilter: '',
  templateId: null
})

const emailPreview = ref('')
const companies = ref([])
const selectedCompany = ref(null)
const selectedRecord = ref(null)
const templates = ref([])

const sendRecords = ref([])

onMounted(async () => {
  if (route.query.companyId) {
    emailForm.companyId = parseInt(route.query.companyId)
    emailForm.targetType = 'single'
  }
  await Promise.all([loadCompanies(), loadTemplates(), loadRecords()])
})

async function loadTemplates() {
  try {
    const res = await getEmailTemplates()
    templates.value = res.data || []
  } catch (e) {
    console.error('加载邮件模板失败:', e)
  }
}

async function loadCompanies() {
  try {
    const res = await getCompanies({ size: 1000 })
    companies.value = res.data?.records || res.data || []
    if (emailForm.companyId) {
      handleCompanySelect(emailForm.companyId)
    }
  } catch (e) {
    console.error('加载客户列表失败:', e)
    ElMessage.error('加载客户列表失败')
  }
}

async function loadRecords() {
  try {
    const params = {
      page: pagination.page,
      size: pagination.size,
      email: searchForm.email,
      username: searchForm.username
    }
    
    if (searchForm.dateRange && searchForm.dateRange.length === 2) {
      const startDate = formatDate(searchForm.dateRange[0])
      const endDate = formatDate(searchForm.dateRange[1])
      params.startDate = startDate
      params.endDate = endDate
    }
    
    const res = await getAllEmailRecords(params)
    sendRecords.value = res.data?.records || []
    pagination.total = res.data?.total || 0
  } catch (e) {
    console.error(e)
  }
}

function formatDate(date) {
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

function handleSearch() {
  pagination.page = 1
  loadRecords()
}

function handleReset() {
  searchForm.email = ''
  searchForm.username = ''
  searchForm.dateRange = null
  pagination.page = 1
  loadRecords()
}

function openSendDialog() {
  sendDialogVisible.value = true
}

function handleTargetTypeChange() {
  emailForm.companyId = null
  emailForm.gradeFilter = ''
  selectedCompany.value = null
}

function handleCompanySelect(companyId) {
  selectedCompany.value = companies.value.find(c => c.id === companyId) || null
}

function handleTemplateChange() {
  const template = templates.value.find(t => t.id === emailForm.templateId)
  if (template) {
    emailPreview.value = template.content || ''
  } else {
    emailPreview.value = ''
  }
}

async function handleSend() {
  if (!emailForm.templateId) {
    ElMessage.warning('请选择邮件模板')
    return
  }
  
  if (emailForm.targetType === 'single' && !emailForm.companyId) {
    ElMessage.warning('请选择客户')
    return
  }
  
  sending.value = true
  try {
    await sendEmail({
      companyId: emailForm.companyId,
      contactId: null,
      templateId: emailForm.templateId
    })
    ElMessage.success('邮件发送任务已创建')
    sendDialogVisible.value = false
    await loadRecords()
  } catch (e) {
    ElMessage.error('发送失败')
    console.error(e)
  } finally {
    sending.value = false
  }
}

async function handleBatchSend() {
  if (!emailForm.templateId) {
    ElMessage.warning('请选择邮件模板')
    return
  }
  
  let companyIds = []
  if (emailForm.targetType === 'all') {
    companyIds = companies.value.map(c => c.id)
  } else if (emailForm.targetType === 'grade') {
    const grades = emailForm.gradeFilter === 'SA' ? ['S', 'A'] : [emailForm.gradeFilter]
    companyIds = companies.value.filter(c => grades.includes(c.grade)).map(c => c.id)
  }
  
  if (companyIds.length === 0) {
    ElMessage.warning('没有符合条件的客户')
    return
  }
  
  sending.value = true
  try {
    await sendBatchEmail({
      companyIds,
      templateId: emailForm.templateId
    })
    ElMessage.success(`已创建批量发送任务，将发送给 ${companyIds.length} 个客户`)
    sendDialogVisible.value = false
    await loadRecords()
  } catch (e) {
    ElMessage.error('批量发送失败')
    console.error(e)
  } finally {
    sending.value = false
  }
}

function viewDetail(row) {
  selectedRecord.value = row
  detailDialogVisible.value = true
}

function viewRecipient(row) {
  selectedRecipient.value = row
  recipientDialogVisible.value = true
}

function goToCompany(companyId) {
  router.push(`/companies?companyId=${companyId}`)
}

function getRecordStatusType(status) {
  const types = { Pending: 'info', Sent: '', Delivered: 'success', Opened: 'warning', Replied: 'success', Failed: 'danger' }
  return types[status] || ''
}

function getRecordStatusLabel(status) {
  const labels = { Pending: '待发送', Sent: '已发送', Delivered: '已送达', Opened: '已打开', Replied: '已回复', Failed: '发送失败' }
  return labels[status] || status
}
</script>

<style scoped>
.email-campaign {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.search-row {
  margin-bottom: 20px;
}

.records-table {
  margin-bottom: 20px;
}

.pagination {
  display: flex;
  justify-content: flex-end;
}

.email-preview {
  border: 1px solid #e8f4f8;
  border-radius: 8px;
  background: #fff;
  overflow: hidden;
}

.email-preview .preview-header {
  padding: 10px 15px;
  background: #f0f9ff;
  border-bottom: 1px solid #e8f4f8;
  font-size: 13px;
  color: #334155;
}

.email-preview .preview-content {
  padding: 15px;
  min-height: 150px;
  max-height: 300px;
  overflow-y: auto;
  font-size: 13px;
  line-height: 1.6;
  color: #334155;
}

.email-preview .preview-content img {
  max-width: 100%;
  height: auto;
}

.email-detail {
  padding: 10px;
}

.email-content {
  max-height: 400px;
  overflow-y: auto;
  padding: 10px;
  background: #f8fafc;
  border-radius: 4px;
}
</style>