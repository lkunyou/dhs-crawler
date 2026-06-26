<template>
  <div class="email-templates">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>邮件模板管理</span>
          <el-button type="primary" @click="openNewTemplate">
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

    <el-dialog v-model="showAddDialog" :title="isEdit ? '编辑模板' : '新建模板'" width="800px" @close="handleDialogClose">
      <el-form :model="templateForm" label-width="100px" ref="templateFormRef">
        <FormField type="input" label="模板名称" prop="templateName" v-model="templateForm.templateName" />
        <FormField type="input" label="邮件主题" prop="subject" v-model="templateForm.subject" />
        <FormField type="select" label="分类" prop="category" v-model="templateForm.category" :options="categoryOptions" />
        <FormField type="number" label="发送序列" prop="daySequence" v-model="templateForm.daySequence" :min="1" :max="30" />
        <FormField type="textarea" label="邮件内容" prop="content" v-model="templateForm.content" :rows="15" />
        <FormField type="switch" label="是否启用" prop="isActive" v-model="templateForm.isActive" />
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSave">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { BaseTable, FormField } from '@/components'
import { getEmailTemplates, createEmailTemplate, updateEmailTemplate, deleteEmailTemplate } from '@/api/email'

const showPreviewDialog = ref(false)
const showAddDialog = ref(false)
const isEdit = ref(false)
const dialogOpening = ref(false)
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

const templates = ref([])

const templateForm = reactive({
  id: null,
  templateName: '',
  subject: '',
  content: '',
  category: 'Cold_Outreach',
  daySequence: 1,
  isActive: true
})

onMounted(() => {
  loadTemplates()
})

async function loadTemplates() {
  try {
    const res = await getEmailTemplates()
    templates.value = res.data || []
  } catch (e) {
    ElMessage.error('加载模板失败')
  }
}

watch(showAddDialog, (val) => {
  if (val && !dialogOpening.value) {
    // Only reset when opening for NEW template (not editing)
    templateForm.id = null
    templateForm.templateName = ''
    templateForm.subject = ''
    templateForm.content = ''
    templateForm.category = 'Cold_Outreach'
    templateForm.daySequence = 1
    templateForm.isActive = true
    isEdit.value = false
  }
  if (!val) {
    dialogOpening.value = false
  }
})

function handleDialogClose() {
  // Reset form when dialog closes
  templateForm.id = null
  templateForm.templateName = ''
  templateForm.subject = ''
  templateForm.content = ''
  templateForm.category = 'Cold_Outreach'
  templateForm.daySequence = 1
  templateForm.isActive = true
}

function openNewTemplate() {
  dialogOpening.value = true
  showAddDialog.value = true
}

function handlePreviewTemplate(row) {
  previewTemplate.subject = row.subject
  previewTemplate.content = row.content
  showPreviewDialog.value = true
}

function editTemplate(row) {
  dialogOpening.value = true
  isEdit.value = true
  // Set form data for editing
  templateForm.id = row.id
  templateForm.templateName = row.templateName
  templateForm.subject = row.subject
  templateForm.content = row.content
  templateForm.category = row.category
  templateForm.daySequence = row.daySequence
  templateForm.isActive = row.isActive
  showAddDialog.value = true
}

async function handleSave() {
  try {
    if (templateForm.id) {
      await updateEmailTemplate(templateForm.id, { ...templateForm })
      ElMessage.success('模板已更新')
    } else {
      await createEmailTemplate({ ...templateForm })
      ElMessage.success('模板已创建')
    }
    showAddDialog.value = false
    await loadTemplates()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

async function deleteTemplate(id) {
  try {
    await ElMessageBox.confirm('确定删除该模板吗?', '提示', { type: 'warning' })
    await deleteEmailTemplate(id)
    ElMessage.success('删除成功')
    await loadTemplates()
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
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