<template>
  <div class="company-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>客户管理</span>
          <div class="header-actions">
            <el-button type="primary" @click="showAddDialog = true">
              <el-icon><Plus /></el-icon> 新增客户
            </el-button>
            <el-button type="success" @click="handleBatchEmail">
              <el-icon><Message /></el-icon> 批量发邮件
            </el-button>
            <el-button type="warning" @click="exportCompanies">导出</el-button>
            <el-upload
              action=""
              :auto-upload="false"
              :show-file-list="false"
              :on-change="handleImport"
              accept=".xlsx,.xls"
              style="display: inline-block"
            >
              <el-button type="info">导入</el-button>
            </el-upload>
          </div>
        </div>
      </template>

      <TableSearch :fields="searchFields" @search="loadData" @reset="loadData" />

      <BaseTable
        :data="tableData"
        :columns="columns"
        :loading="loading"
        :pagination="pagination"
        :show-selection="true"
        @selection-change="handleSelectionChange"
        @link-click="handleLinkClick"
        @page-change="loadData"
        @size-change="loadData"
      />
    </el-card>

    <DialogForm
      v-model:visible="showAddDialog"
      title="新增客户"
      :model-value="newCompany"
      :loading="submitting"
      @submit="handleAdd"
    >
      <FormField type="input" label="公司名称" prop="companyName" v-model="newCompany.companyName" />
      <FormField type="select" label="公司类型" prop="companyType" v-model="newCompany.companyType" :options="companyTypeOptions" />
      <FormField type="input" label="官网" prop="website" v-model="newCompany.website" />
      <FormField type="input" label="地址" prop="address" v-model="newCompany.address" />
      <FormField type="input" label="城市" prop="city" v-model="newCompany.city" />
      <FormField type="input" label="电话" prop="phone" v-model="newCompany.phone" />
      <FormField type="input" label="邮箱" prop="email" v-model="newCompany.email" />
      <FormField type="input" label="WhatsApp" prop="whatsapp" v-model="newCompany.whatsapp" />
    </DialogForm>

    <!-- WhatsApp 聊天窗口 -->
    <el-dialog v-model="whatsappDialogVisible" :title="`WhatsApp - ${whatsappCompany?.companyName || ''}`" width="600px">
      <div v-loading="whatsappLoading" style="max-height: 400px; overflow-y: auto; padding: 10px; background: #f5f5f5; border-radius: 8px;">
        <div v-if="whatsappRecords.length === 0" style="text-align: center; color: #999; padding: 40px 0;">暂无聊天记录</div>
        <div v-for="record in whatsappRecords" :key="record.id" style="margin-bottom: 12px;">
          <div :style="{ textAlign: record.direction === 'Outbound' ? 'right' : 'left' }">
            <div :style="{ display: 'inline-block', maxWidth: '70%', padding: '10px 14px', borderRadius: '12px', background: record.direction === 'Outbound' ? '#dcf8c6' : '#fff', border: '1px solid #e0e0e0', wordBreak: 'break-word' }">
              <div style="font-size: 13px; color: #333; line-height: 1.5;">{{ record.content }}</div>
              <div style="font-size: 11px; color: #999; margin-top: 4px; text-align: right;">{{ record.sentAt }}</div>
            </div>
          </div>
        </div>
      </div>
      <div style="margin-top: 16px; display: flex; gap: 10px;">
        <el-input v-model="whatsappSendForm.content" placeholder="输入消息内容..." @keyup.enter="sendWhatsappMessage" />
        <el-button type="success" @click="sendWhatsappMessage">发送</el-button>
      </div>
    </el-dialog>

    <!-- 导入预览弹窗 -->
    <el-dialog v-model="importPreviewVisible" title="导入预览" width="900px" :close-on-click-modal="false" :before-close="cancelImport">
      <div style="margin-bottom: 12px;">共解析到 <b>{{ importPreviewTotal }}</b> 条数据，确认后导入正式表</div>
      <el-table :data="importPreviewList" height="400" border>
        <el-table-column prop="companyName" label="公司名称" min-width="150" />
        <el-table-column prop="companyNameEn" label="英文名称" min-width="150" />
        <el-table-column prop="country" label="国家" width="100" />
        <el-table-column prop="city" label="城市" width="100" />
        <el-table-column prop="email" label="邮箱" min-width="150" />
        <el-table-column prop="phone" label="电话" width="120" />
        <el-table-column prop="companyType" label="类型" width="80" />
        <el-table-column prop="status" label="状态" width="80" />
      </el-table>
      <template #footer>
        <el-button @click="cancelImport">取消</el-button>
        <el-button type="primary" :loading="importLoading" @click="confirmImport">确认导入</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCompanies, createCompany, deleteCompany } from '@/api/company'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getWhatsappRecords, sendWhatsappText } from '@/api/whatsapp'
import request from '@/utils/request'
import { BaseTable, TableSearch, FormField, DialogForm } from '@/components'

const router = useRouter()
const loading = ref(false)
const submitting = ref(false)
const tableData = ref([])
const selectedRows = ref([])
const showAddDialog = ref(false)
const importPreviewVisible = ref(false)
const importPreviewList = ref([])
const importPreviewTotal = ref(0)
const importTempId = ref('')
const importLoading = ref(false)
const whatsappDialogVisible = ref(false)
const whatsappLoading = ref(false)
const whatsappRecords = ref([])
const whatsappCompany = ref(null)
const whatsappSendForm = reactive({
  content: ''
})

const searchFields = [
  { type: 'input', prop: 'keyword', label: '关键词', placeholder: '公司名/网站' },
  { type: 'select', prop: 'leadGrade', label: '客户等级', placeholder: '全部', options: [
    { label: 'S级', value: 'S' },
    { label: 'A级', value: 'A' },
    { label: 'B级', value: 'B' },
    { label: 'C级', value: 'C' }
  ]},
  { type: 'select', prop: 'status', label: '状态', placeholder: '全部', options: [
    { label: '新客户', value: 'New' },
    { label: '已联系', value: 'Contacted' },
    { label: '有回复', value: 'Replied' },
    { label: '已报价', value: 'Quoted' },
    { label: '谈判中', value: 'Negotiation' },
    { label: '已成交', value: 'Won' },
    { label: '已流失', value: 'Lost' }
  ]}
]

const companyTypeOptions = [
  { label: 'Distributor', value: 'Distributor' },
  { label: 'Importer', value: 'Importer' },
  { label: 'OEM', value: 'OEM' },
  { label: 'Retailer', value: 'Retailer' },
  { label: 'Manufacturer', value: 'Manufacturer' }
]

const columns = [
  { prop: 'companyName', label: '公司名称', minWidth: 200, type: 'link' },
  { prop: 'coreContact', label: '核心联系人', width: 150 },
  
  { prop: 'purchasePotential', label: '采购潜力', width: 100, type: 'tag', tagType: (row) => {
    const map = { '极高': 'danger', '高': 'warning', '中': 'info', '低': 'default' }
    return map[row.purchasePotential] || 'default'
  }, tagLabel: (row) => row.purchasePotential || '-' },
  { prop: 'email', label: '邮箱', width: 180, type: 'custom', render: (row) => row.email ? `<a href="mailto:${row.email}" class="el-link el-link--primary">${row.email}</a>` : '-' },
  { prop: 'website', label: '网站', width: 180, type: 'custom', render: (row) => {
    if (!row.website) return '-'
    let url = row.website.trim()
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      url = 'https://' + url
    }
    const display = url.replace(/^https?:\/\//, '').replace(/\/$/, '')
    return `<a href="${url}" target="_blank" class="el-link el-link--primary" title="${url}">${display.length > 22 ? display.substring(0, 22) + '...' : display}</a>`
  } },
  { prop: 'status', label: '状态', width: 100, type: 'tag', tagType: (row) => getStatusType(row.status), tagLabel: (row) => getStatusLabel(row.status) },
  { prop: 'source', label: '来源', width: 100 },
  { prop: 'emailCount', label: '邮件', width: 80, type: 'custom', render: (row) => row.emailCount ? `<span style="color:#409eff;font-weight:600">${row.emailCount}</span>` : '-', onClick: (row) => { if (row.emailCount) router.push(`/email-campaign?companyId=${row.id}`) } },
  { prop: 'whatsappCount', label: 'WhatsApp', width: 95, type: 'custom', render: (row) => row.whatsappCount ? `<span style="color:#67c23a;font-weight:600">${row.whatsappCount}</span>` : '-', onClick: (row) => { if (row.whatsappCount) openWhatsappDialog(row) } },
  { prop: 'quoteCount', label: '报价', width: 80, type: 'custom', render: (row) => row.quoteCount ? `<span style="color:#e6a23c;font-weight:600">${row.quoteCount}</span>` : '-', onClick: (row) => { if (row.quoteCount) router.push(`/quotes?companyId=${row.id}`) } },
  { label: '操作', width: 200, fixed: 'right', type: 'button', buttons: [
    { label: '发邮件', type: 'success', size: 'small', handler: (row) => sendEmail(row.id) },
    { label: '删除', type: 'danger', size: 'small', handler: (row) => handleDelete(row.id) }
  ]}
]

const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

const newCompany = reactive({
  companyName: '',
  companyType: '',
  website: '',
  address: '',
  city: '',
  phone: '',
  email: '',
  whatsapp: ''
})

onMounted(() => {
  loadData()
})

async function loadData() {
  loading.value = true
  try {
    const res = await getCompanies(pagination)
    tableData.value = res.data.records
    pagination.total = res.data.total
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function handleSelectionChange(rows) {
  selectedRows.value = rows
}

function handleLinkClick({ row }) {
  viewDetail(row.id)
}

function getStatusType(status) {
  const types = {
    New: 'info',
    Contacted: '',
    Replied: 'warning',
    Quoted: 'success',
    Negotiation: 'danger',
    Won: 'success',
    Lost: 'info'
  }
  return types[status] || ''
}

function getStatusLabel(status) {
  const labels = {
    New: '新客户',
    Contacted: '已联系',
    Replied: '有回复',
    Quoted: '已报价',
    Negotiation: '谈判中',
    Sample_Sent: '已打样',
    Won: '已成交',
    Lost: '已流失',
    Invalid: '无效'
  }
  return labels[status] || status
}

function viewDetail(id) {
  router.push(`/companies/${id}`)
}

function sendEmail(id) {
  router.push(`/email-campaign?companyId=${id}`)
}

async function handleDelete(id) {
  try {
    await ElMessageBox.confirm('确定删除该客户吗?', '提示', { type: 'warning' })
    await deleteCompany(id)
    ElMessage.success('删除成功')
    loadData()
  } catch (e) {
    if (e !== 'cancel') console.error(e)
  }
}

async function handleAdd(data) {
  submitting.value = true
  try {
    await createCompany(data)
    ElMessage.success('添加成功')
    showAddDialog.value = false
    Object.keys(newCompany).forEach(key => newCompany[key] = '')
    loadData()
  } catch (e) {
    console.error(e)
  } finally {
    submitting.value = false
  }
}

async function openWhatsappDialog(row) {
  whatsappCompany.value = row
  whatsappDialogVisible.value = true
  whatsappLoading.value = true
  whatsappSendForm.content = ''
  try {
    const res = await getWhatsappRecords(row.id)
    whatsappRecords.value = res.data || []
  } catch (e) {
    whatsappRecords.value = []
  } finally {
    whatsappLoading.value = false
  }
}

async function sendWhatsappMessage() {
  if (!whatsappSendForm.content.trim()) {
    ElMessage.warning('请输入消息内容')
    return
  }
  if (!whatsappCompany.value) return
  try {
    await sendWhatsappText({
      companyId: whatsappCompany.value.id,
      phoneNumber: whatsappCompany.value.whatsapp || whatsappCompany.value.phone,
      content: whatsappSendForm.content.trim()
    })
    ElMessage.success('消息已发送')
    whatsappSendForm.content = ''
    // 刷新聊天记录
    const res = await getWhatsappRecords(whatsappCompany.value.id)
    whatsappRecords.value = res.data || []
  } catch (e) {
    ElMessage.error('发送失败')
  }
}

function handleBatchEmail() {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请先选择客户')
    return
  }
  const ids = selectedRows.value.map(r => r.id)
  router.push({ path: '/email-campaign', query: { companyIds: ids.join(',') } })
}

async function exportCompanies() {
  try {
    const res = await request.get('/companies/export', { responseType: 'blob' })
    const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = '客户列表.xlsx'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (e) {
    ElMessage.error('导出失败')
  }
}

async function handleImport(file) {
  const formData = new FormData()
  formData.append('file', file.raw)
  try {
    const res = await request.post('/companies/import-preview', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    if (res.data) {
      importTempId.value = res.data.tempId || ''
      importPreviewList.value = res.data.list || []
      importPreviewTotal.value = res.data.total || 0
      importPreviewVisible.value = true
    }
  } catch (e) {
    ElMessage.error('预览解析失败')
  }
}

async function confirmImport() {
  if (!importTempId.value) return
  importLoading.value = true
  try {
    await request.post('/companies/import-confirm', null, { params: { tempId: importTempId.value } })
    ElMessage.success('导入成功')
    importPreviewVisible.value = false
    loadData()
  } catch (e) {
    ElMessage.error('导入失败')
  } finally {
    importLoading.value = false
  }
}

async function cancelImport() {
  if (importTempId.value) {
    try {
      await request.post('/companies/import-cancel', null, { params: { tempId: importTempId.value } })
    } catch (e) {}
  }
  importPreviewVisible.value = false
  importTempId.value = ''
  importPreviewList.value = []
  importPreviewTotal.value = 0
}
</script>

<style scoped>
.company-list {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}
</style>