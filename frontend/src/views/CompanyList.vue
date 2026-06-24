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
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getCompanies, createCompany, deleteCompany } from '@/api/company'
import { ElMessage, ElMessageBox } from 'element-plus'
import { BaseTable, TableSearch, FormField, DialogForm } from '@/components'

const router = useRouter()
const loading = ref(false)
const submitting = ref(false)
const tableData = ref([])
const selectedRows = ref([])
const showAddDialog = ref(false)

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
  { prop: 'companyType', label: '类型', width: 120 },
  { prop: 'city', label: '城市', width: 100 },
  { prop: 'website', label: '网站', width: 150, type: 'custom', render: (row) => row.website ? `<a href="${row.website}" target="_blank" class="el-link el-link--primary">访问</a>` : '' },
  { prop: 'leadGrade', label: '等级', width: 80, type: 'tag', tagType: (row) => ({ S: 'danger', A: 'warning', B: '', C: 'info' }[row.leadGrade]) },
  { prop: 'leadScore', label: '评分', width: 80 },
  { prop: 'status', label: '状态', width: 100, type: 'tag', tagType: (row) => getStatusType(row.status), tagLabel: (row) => getStatusLabel(row.status) },
  { prop: 'source', label: '来源', width: 100 },
  { label: '操作', width: 200, fixed: 'right', type: 'button', buttons: [
    { label: '详情', type: 'primary', size: 'small', handler: (row) => viewDetail(row.id) },
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

function handleBatchEmail() {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请先选择客户')
    return
  }
  const ids = selectedRows.value.map(r => r.id)
  router.push({ path: '/email-campaign', query: { companyIds: ids.join(',') } })
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