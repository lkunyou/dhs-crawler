<template>
  <div class="email-campaign">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>邮件营销活动</span>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="16">
          <el-card>
            <template #header>发送邮件</template>
            <BaseForm :model-value="emailForm" label-width="100px">
              <FormField type="select" label="目标客户" prop="targetType" v-model="emailForm.targetType" :options="targetTypeOptions" @change="handleTargetTypeChange" />
              
              <FormField v-if="emailForm.targetType === 'single'" type="select" label="选择客户" prop="companyId" v-model="emailForm.companyId" :options="companyOptions" :filterable="true" placeholder="搜索客户" />
              
              <FormField v-if="emailForm.targetType === 'grade'" type="select" label="客户等级" prop="gradeFilter" v-model="emailForm.gradeFilter" :options="gradeOptions" />
              
              <FormField type="select" label="邮件模板" prop="templateId" v-model="emailForm.templateId" :options="templateOptions" @change="handleTemplateChange" />
              
              <el-form-item label="预览">
                <div class="email-preview" v-html="emailPreview"></div>
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="handleSend" :loading="sending">发送邮件</el-button>
                <el-button @click="handleSchedule">定时发送</el-button>
              </el-form-item>
            </BaseForm>
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
        <BaseTable :data="sendRecords" :columns="sendRecordColumns" :show-pagination="false" />
      </el-card>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { BaseForm, BaseTable, FormField } from '@/components'

const route = useRoute()
const sending = ref(false)

const emailForm = reactive({
  targetType: 'single',
  companyId: null,
  gradeFilter: '',
  templateId: null
})

const targetTypeOptions = [
  { label: '单个客户', value: 'single' },
  { label: '客户等级筛选', value: 'grade' },
  { label: '全部S/A级客户', value: 'high_grade' }
]

const gradeOptions = [
  { label: 'S级', value: 'S' },
  { label: 'A级', value: 'A' },
  { label: 'B级', value: 'B' },
  { label: 'S/A级', value: 'SA' }
]

const sendRecordColumns = [
  { prop: 'recipientEmail', label: '收件人', width: 200 },
  { prop: 'subject', label: '主题', minWidth: 200 },
  { prop: 'status', label: '状态', width: 100, type: 'tag', tagType: (row) => getRecordStatusType(row.status), tagLabel: (row) => getRecordStatusLabel(row.status) },
  { prop: 'sentAt', label: '发送时间', width: 180 },
  { prop: 'openedAt', label: '打开时间', width: 180 },
  { prop: 'repliedAt', label: '回复时间', width: 180 }
]

const emailPreview = ref('')
const companies = ref([])
const templates = ref([
  { id: 1, templateName: 'Day1-公司介绍', subject: 'Professional Auto Parts Manufacturer from China', category: 'Cold_Outreach', daySequence: 1 },
  { id: 2, templateName: 'Day3-热销产品', subject: 'Hot Selling Auto Parts for Thai Market', category: 'Product_Promo', daySequence: 3 },
  { id: 3, templateName: 'Day6-OEM案例', subject: 'OEM Partnership Success Story', category: 'OEM_Case', daySequence: 6 },
  { id: 4, templateName: 'Day10-报价引导', subject: 'Exclusive Price List', category: 'Quote', daySequence: 10 },
  { id: 5, templateName: 'Day15-促销提醒', subject: 'Limited-Time Promotion', category: 'Promotion', daySequence: 15 }
])

const companyOptions = computed(() => companies.value.map(c => ({ label: c.companyName, value: c.id })))
const templateOptions = computed(() => templates.value.map(t => ({ label: t.templateName, value: t.id })))

const sendRecords = ref([])

onMounted(() => {
  if (route.query.companyId) {
    emailForm.companyId = parseInt(route.query.companyId)
    emailForm.targetType = 'single'
  }
})

function handleTargetTypeChange() {}

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
  
  sending.value = true
  try {
    ElMessage.success('邮件发送任务已创建')
  } catch (e) {
    console.error(e)
  } finally {
    sending.value = false
  }
}

function handleSchedule() {
  ElMessage.info('定时发送功能开发中')
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
  font-weight: bold;
}

.email-preview {
  border: 1px solid #dcdfe6;
  padding: 15px;
  border-radius: 4px;
  background: #f5f7fa;
  min-height: 200px;
}
</style>