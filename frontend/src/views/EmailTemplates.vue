<template>
  <div class="email-templates">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>邮件模板管理</span>
          <el-button type="primary" @click="showAddDialog = true">
            <el-icon><Plus /></el-icon> 新建模板
          </el-button>
        </div>
      </template>

      <BaseTable :data="templates" :columns="columns" :show-pagination="false" />
    </el-card>

    <el-dialog v-model="showPreviewDialog" title="邮件预览" width="700px">
      <div class="email-preview">
        <h3>{{ previewTemplate.subject }}</h3>
        <div v-html="previewTemplate.content"></div>
      </div>
    </el-dialog>

    <DialogForm
      v-model:visible="showAddDialog"
      :title="isEdit ? '编辑模板' : '新建模板'"
      width="800px"
      @submit="handleSave"
    >
      <FormField type="input" label="模板名称" prop="templateName" v-model="templateForm.templateName" />
      <FormField type="input" label="邮件主题" prop="subject" v-model="templateForm.subject" />
      <FormField type="select" label="分类" prop="category" v-model="templateForm.category" :options="categoryOptions" />
      <FormField type="number" label="发送序列" prop="daySequence" v-model="templateForm.daySequence" :min="1" :max="30" />
      <FormField type="textarea" label="邮件内容" prop="content" v-model="templateForm.content" :rows="15" />
      <FormField type="switch" label="是否启用" prop="isActive" v-model="templateForm.isActive" />
    </DialogForm>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { BaseTable, DialogForm, FormField } from '@/components'

const showPreviewDialog = ref(false)
const showAddDialog = ref(false)
const isEdit = ref(false)
const previewTemplate = reactive({ subject: '', content: '' })

const categoryOptions = [
  { label: '开发信', value: 'Cold_Outreach' },
  { label: '产品推广', value: 'Product_Promo' },
  { label: 'OEM案例', value: 'OEM_Case' },
  { label: '报价引导', value: 'Quote' },
  { label: '促销活动', value: 'Promotion' }
]

const columns = [
  { prop: 'templateName', label: '模板名称', width: 200 },
  { prop: 'subject', label: '邮件主题', minWidth: 250 },
  { prop: 'category', label: '分类', width: 120, type: 'tag', tagLabel: (row) => getCategoryLabel(row.category) },
  { prop: 'daySequence', label: '发送序列', width: 100, type: 'custom', render: (row) => `第${row.daySequence}天` },
  { prop: 'openRate', label: '打开率', width: 100, type: 'custom', render: (row) => `${row.openRate}%` },
  { prop: 'replyRate', label: '回复率', width: 100, type: 'custom', render: (row) => `${row.replyRate}%` },
  { prop: 'isActive', label: '状态', width: 80, type: 'tag', tagType: (row) => row.isActive ? 'success' : 'info', tagLabel: (row) => row.isActive ? '启用' : '禁用' },
  { label: '操作', width: 200, fixed: 'right', type: 'button', buttons: [
    { label: '预览', type: '', size: 'small', handler: (row) => handlePreviewTemplate(row) },
    { label: '编辑', type: 'primary', size: 'small', handler: (row) => editTemplate(row) },
    { label: '删除', type: 'danger', size: 'small', handler: (row) => deleteTemplate(row.id) }
  ]}
]

const templates = ref([
  { id: 1, templateName: 'Day1-公司介绍', subject: 'Professional Auto Parts Manufacturer from China - [Your Company]', category: 'Cold_Outreach', daySequence: 1, openRate: 42.5, replyRate: 12.3, isActive: true, content: '<p>Dear [Name],</p><p>I hope this email finds you well.</p><p>I am writing to introduce [Your Company]...</p>' },
  { id: 2, templateName: 'Day3-热销产品', subject: 'Hot Selling Auto Parts for Thai Market - Special Offer', category: 'Product_Promo', daySequence: 3, openRate: 38.2, replyRate: 9.8, isActive: true, content: '<p>Hi [Name],</p><p>Following up on my previous email...</p>' },
  { id: 3, templateName: 'Day6-OEM案例', subject: 'OEM Partnership Success Story', category: 'OEM_Case', daySequence: 6, openRate: 35.1, replyRate: 8.5, isActive: true, content: '<p>Dear [Name],</p><p>I thought you might be interested...</p>' },
  { id: 4, templateName: 'Day10-报价引导', subject: 'Exclusive Price List - Auto Parts for Your Review', category: 'Quote', daySequence: 10, openRate: 32.8, replyRate: 15.2, isActive: true, content: '<p>Hi [Name],</p><p>I have prepared a special price list...</p>' },
  { id: 5, templateName: 'Day15-促销提醒', subject: 'Limited-Time Promotion - Auto Parts Special Deal', category: 'Promotion', daySequence: 15, openRate: 28.5, replyRate: 6.7, isActive: true, content: '<p>Dear [Name],</p><p>This is a friendly reminder...</p>' }
])

const templateForm = reactive({
  id: null,
  templateName: '',
  subject: '',
  content: '',
  category: 'Cold_Outreach',
  daySequence: 1,
  isActive: true
})

function handlePreviewTemplate(row) {
  previewTemplate.subject = row.subject
  previewTemplate.content = row.content
  showPreviewDialog.value = true
}

function editTemplate(row) {
  Object.assign(templateForm, row)
  isEdit.value = true
  showAddDialog.value = true
}

function handleSave() {
  ElMessage.success(isEdit.value ? '模板已更新' : '模板已创建')
  showAddDialog.value = false
}

async function deleteTemplate(id) {
  try {
    await ElMessageBox.confirm('确定删除该模板吗?', '提示', { type: 'warning' })
    ElMessage.success('删除成功')
  } catch (e) {}
}

function getCategoryLabel(category) {
  const labels = {
    Cold_Outreach: '开发信',
    Product_Promo: '产品推广',
    OEM_Case: 'OEM案例',
    Quote: '报价引导',
    Promotion: '促销活动'
  }
  return labels[category] || category
}
</script>

<style scoped>
.email-templates { padding: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; font-weight: bold; }
.email-preview { padding: 20px; line-height: 1.8; }
.email-preview h3 { margin-bottom: 20px; color: #303133; }
</style>