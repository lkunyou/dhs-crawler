<template>
  <div class="email-campaign">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>邮件营销活动</span>
          <el-button type="primary" @click="refreshRecords" size="small">刷新记录</el-button>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="16">
          <el-card>
            <template #header>发送邮件</template>
            <el-form :model="emailForm" label-width="100px">
              <el-form-item label="目标客户" required>
                <el-select v-model="emailForm.targetType" @change="handleTargetTypeChange" placeholder="选择发送方式">
                  <el-option label="单个客户" value="single" />
                  <el-option label="客户等级筛选" value="grade" />
                  <el-option label="全部客户" value="all" />
                </el-select>
              </el-form-item>
              
              <el-form-item v-if="emailForm.targetType === 'single'" label="选择客户" required>
                <el-select v-model="emailForm.companyId" filterable placeholder="搜索客户" style="width: 100%">
                  <el-option v-for="c in companies" :key="c.id" :label="c.companyName" :value="c.id" />
                </el-select>
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
                <div class="email-preview" v-html="emailPreview"></div>
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="handleSend" :loading="sending">发送邮件</el-button>
                <el-button @click="handleBatchSend" :loading="sending" v-if="emailForm.targetType !== 'single'">批量发送</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card>
            <template #header>邮件模板列表</template>
            <el-timeline>
              <el-timeline-item v-for="t in templates" :key="t.id" :timestamp="`第${t.daySequence}天`" placement="top">
                <el-card>
                  <h4>{{ t.templateName }}</h4>
                  <p>{{ t.subject }}</p>
                  <el-tag size="small">{{ t.category }}</el-tag>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </el-card>
        </el-col>
      </el-row>

      <el-card style="margin-top: 20px">
        <template #header>发送记录</template>
        <el-table :data="sendRecords" border>
          <el-table-column prop="recipientEmail" label="收件人" width="200" />
          <el-table-column prop="subject" label="主题" min-width="200" />
          <el-table-column prop="status" label="状态" width="120">
            <template #default="{ row }">
              <el-tag :type="getRecordStatusType(row.status)">{{ getRecordStatusLabel(row.status) }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="sentAt" label="发送时间" width="180" />
          <el-table-column prop="openedAt" label="打开时间" width="180" />
          <el-table-column prop="repliedAt" label="回复时间" width="180" />
        </el-table>
      </el-card>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { sendEmail, sendBatchEmail, getAllEmailRecords } from '@/api/email'
import { getCompanies } from '@/api/company'

const route = useRoute()
const sending = ref(false)

const emailForm = reactive({
  targetType: 'single',
  companyId: null,
  gradeFilter: '',
  templateId: null
})

const emailPreview = ref('')
const companies = ref([])
const templates = ref([
  { id: 1, templateName: 'Day1-公司介绍', subject: 'Professional Auto Parts Manufacturer from China', category: 'Cold_Outreach', daySequence: 1 },
  { id: 2, templateName: 'Day3-热销产品', subject: 'Hot Selling Auto Parts for Thai Market', category: 'Product_Promo', daySequence: 3 },
  { id: 3, templateName: 'Day6-OEM案例', subject: 'OEM Partnership Success Story', category: 'OEM_Case', daySequence: 6 },
  { id: 4, templateName: 'Day10-报价引导', subject: 'Exclusive Price List', category: 'Quote', daySequence: 10 },
  { id: 5, templateName: 'Day15-促销提醒', subject: 'Limited-Time Promotion', category: 'Promotion', daySequence: 15 }
])

const sendRecords = ref([])

onMounted(async () => {
  if (route.query.companyId) {
    emailForm.companyId = parseInt(route.query.companyId)
    emailForm.targetType = 'single'
  }
  await loadCompanies()
  await loadRecords()
})

async function loadCompanies() {
  try {
    const res = await getCompanies()
    companies.value = res.data
  } catch (e) {
    console.error(e)
  }
}

async function loadRecords() {
  try {
    const res = await getAllEmailRecords()
    sendRecords.value = res.data
  } catch (e) {
    console.error(e)
  }
}

function refreshRecords() {
  loadRecords()
}

function handleTargetTypeChange() {
  emailForm.companyId = null
  emailForm.gradeFilter = ''
}

function handleTemplateChange() {
  const template = templates.value.find(t => t.id === emailForm.templateId)
  if (template) {
    emailPreview.value = `<p><strong>主题:</strong> ${template.subject}</p><p>邮件内容预览...</p>`
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
    await loadRecords()
  } catch (e) {
    ElMessage.error('批量发送失败')
    console.error(e)
  } finally {
    sending.value = false
  }
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

.email-preview {
  border: 1px solid #e8f4f8;
  padding: 15px;
  border-radius: 8px;
  background: #f8fafc;
  min-height: 150px;
}
</style>