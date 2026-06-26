<template>
  <div class="quote-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>报价管理</span>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="客户名称">
          <el-input v-model="searchForm.companyName" placeholder="搜索客户名称" style="width: 200px" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" style="width: 140px" clearable>
            <el-option label="草稿" value="draft" />
            <el-option label="已发送" value="sent" />
            <el-option label="已接受" value="accepted" />
            <el-option label="已拒绝" value="rejected" />
            <el-option label="过期" value="expired" />
          </el-select>
        </el-form-item>
        <el-form-item label="时间范围">
          <el-date-picker v-model="searchForm.dateRange" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" style="width: 300px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="primary" @click="openCreateDialog">新建报价</el-button>
          <el-button type="warning" @click="exportQuotes">导出</el-button>
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
        </el-form-item>
      </el-form>

      <!-- 统计卡片 -->
      <div class="stats-row">
        <el-card class="stat-card">
          <div class="stat-icon bg-blue">
            <el-icon :size="24"><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total }}</div>
            <div class="stat-label">总报价</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-icon bg-green">
            <el-icon :size="24"><Check /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.accepted }}</div>
            <div class="stat-label">已接受</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-icon bg-orange">
            <el-icon :size="24"><Clock /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.sent }}</div>
            <div class="stat-label">已发送</div>
          </div>
        </el-card>
        <el-card class="stat-card">
          <div class="stat-icon bg-red">
            <el-icon :size="24"><Close /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.rejected }}</div>
            <div class="stat-label">已拒绝</div>
          </div>
        </el-card>
      </div>

      <!-- 报价列表 -->
      <el-table :data="quotes" border style="margin-top: 20px">
        <el-table-column prop="quoteNo" label="报价编号" width="160" />
        <el-table-column prop="companyName" label="客户名称" min-width="160" />
        <el-table-column prop="companyEmail" label="客户邮箱" min-width="180">
          <template #default="{ row }">
            <a v-if="row.companyEmail" :href="`mailto:${row.companyEmail}`" class="el-link el-link--primary">{{ row.companyEmail }}</a>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="totalAmount" label="总金额(USD)" width="140">
          <template #default="{ row }">
            <strong>{{ row.totalAmount?.toFixed(2) || '-' }}</strong>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusLabel(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="validDate" label="有效期" width="120">
          <template #default="{ row }">
            {{ formatDate(row.validDate) }}
          </template>
        </el-table-column>
        <el-table-column prop="createdAt" label="创建时间" width="160">
          <template #default="{ row }">
            {{ formatDateTime(row.createdAt) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="viewQuote(row)">查看</el-button>
            <el-button size="small" type="primary" v-if="row.status === 'draft'" @click="editQuote(row)">编辑</el-button>
            <el-button size="small" type="success" v-if="row.status === 'draft'" @click="sendQuote(row)">发送</el-button>
            <el-button size="small" type="danger" @click="deleteQuote(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination" v-if="total > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 创建/编辑报价弹窗 -->
    <el-dialog v-model="createDialogVisible" :title="isEdit ? '编辑报价' : '新建报价'" width="960px">
      <el-form :model="quoteForm" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="客户名称" required>
              <el-select v-model="quoteForm.companyId" style="width: 100%" placeholder="选择客户">
                <el-option v-for="company in companies" :key="company.id" :label="company.companyName" :value="company.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="报价编号">
              <el-input v-model="quoteForm.quoteNo" disabled placeholder="自动生成" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="有效期">
              <el-date-picker v-model="quoteForm.validDate" type="date" placeholder="选择有效期" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="总金额">
              <el-input :model-value="quoteTotal" disabled style="width: 100%">
                <template #prefix>USD</template>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 产品明细 -->
        <el-form-item label="产品明细" required>
          <el-table :data="quoteForm.items" border size="small" style="width: 100%">
            <el-table-column label="产品名称" min-width="180">
              <template #default="{ $index }">
                <el-select
                  v-model="quoteForm.items[$index].productId"
                  filterable
                  remote
                  clearable
                  placeholder="搜索产品"
                  :remote-method="searchProducts"
                  style="width: 100%"
                  @change="(val) => handleProductChange($index, val)"
                >
                  <el-option
                    v-for="p in productOptions"
                    :key="p.id"
                    :label="p.name + (p.code ? ' (' + p.code + ')' : '')"
                    :value="p.id"
                  />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="产品型号" min-width="120">
              <template #default="{ $index }">
                <el-input v-model="quoteForm.items[$index].productModel" placeholder="型号" />
              </template>
            </el-table-column>
            <el-table-column label="数量" width="90">
              <template #default="{ $index }">
                <el-input
                  v-model.number="quoteForm.items[$index].quantity"
                  placeholder="数量"
                  style="width: 100%"
                  @input="(val) => { quoteForm.items[$index].quantity = parseInt(val) || 1 }"
                />
              </template>
            </el-table-column>
            <el-table-column label="单价(USD)" width="120">
              <template #default="{ $index }">
                <el-input
                  v-model="quoteForm.items[$index].unitPrice"
                  placeholder="单价"
                  style="width: 100%"
                  @input="(val) => { quoteForm.items[$index].unitPrice = parseFloat(val) || 0 }"
                />
              </template>
            </el-table-column>
            <el-table-column label="小计" width="100">
              <template #default="{ row }">
                {{ (row.quantity * row.unitPrice).toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="70">
              <template #default="{ $index }">
                <el-button size="small" type="danger" link @click="removeItem($index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div style="margin-top: 8px">
            <el-button type="primary" link @click="addItem">
              <el-icon><Plus /></el-icon> 添加产品
            </el-button>
          </div>
        </el-form-item>

        <el-form-item label="备注">
          <el-input v-model="quoteForm.remark" type="textarea" :rows="3" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveQuote">{{ isEdit ? '保存修改' : '创建报价' }}</el-button>
      </template>
    </el-dialog>

    <!-- 报价详情弹窗 -->
    <el-dialog v-model="viewDialogVisible" title="报价详情" width="800px">
      <div v-if="viewQuoteData" class="quote-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="报价编号">{{ viewQuoteData.quoteNo }}</el-descriptions-item>
          <el-descriptions-item label="客户名称">{{ viewQuoteData.companyName }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(viewQuoteData.status)" size="small">
              {{ getStatusLabel(viewQuoteData.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="有效期">{{ formatDate(viewQuoteData.validDate) }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDateTime(viewQuoteData.createdAt) }}</el-descriptions-item>
          <el-descriptions-item label="总金额(USD)">
            <strong style="font-size: 18px; color: #2563eb">USD {{ viewQuoteData.totalAmount?.toFixed(2) }}</strong>
          </el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ viewQuoteData.remark || '-' }}</el-descriptions-item>
        </el-descriptions>

        <div class="detail-section-title">产品明细</div>
        <el-table :data="viewQuoteData.items || []" border size="small" style="width: 100%">
          <el-table-column type="index" label="#" width="50" />
          <el-table-column prop="productName" label="产品名称" min-width="160" />
          <el-table-column prop="productModel" label="产品型号" min-width="120" />
          <el-table-column prop="quantity" label="数量" width="80" />
          <el-table-column prop="unitPrice" label="单价(USD)" width="120">
            <template #default="{ row }">
              {{ row.unitPrice?.toFixed(2) }}
            </template>
          </el-table-column>
          <el-table-column prop="lineTotal" label="小计(USD)" width="120">
            <template #default="{ row }">
              <strong>{{ row.lineTotal?.toFixed(2) }}</strong>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <template #footer>
        <el-button @click="viewDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 导入预览弹窗 -->
    <el-dialog v-model="importPreviewVisible" title="导入预览" width="800px" :close-on-click-modal="false" :before-close="cancelImport">
      <div style="margin-bottom: 12px;">共解析到 <b>{{ importPreviewTotal }}</b> 条数据，确认后导入正式表</div>
      <el-table :data="importPreviewList" height="400" border>
        <el-table-column prop="quoteNo" label="报价编号" min-width="120" />
        <el-table-column prop="status" label="状态" width="100" />
        <el-table-column prop="remark" label="备注" min-width="200" />
      </el-table>
      <template #footer>
        <el-button @click="cancelImport">取消</el-button>
        <el-button type="primary" :loading="importLoading" @click="confirmImport">确认导入</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Document, Check, Clock, Close, Plus } from '@element-plus/icons-vue'
import { getQuotes, createQuote, updateQuote, deleteQuote as deleteQuoteApi, getQuote } from '@/api/quote'
import request from '@/utils/request'
import { getCompanies } from '@/api/company'
import { getProducts } from '@/api/product'

const quotes = ref([])
const companies = ref([])
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const loading = ref(false)
const createDialogVisible = ref(false)
const viewDialogVisible = ref(false)
const isEdit = ref(false)
const viewQuoteData = ref(null)
const importPreviewVisible = ref(false)
const importPreviewList = ref([])
const importPreviewTotal = ref(0)
const importTempId = ref('')
const importLoading = ref(false)

const searchForm = reactive({
  companyName: '',
  status: '',
  dateRange: null
})

const defaultItem = () => ({
  productId: null,
  productName: '',
  productModel: '',
  quantity: 1,
  unitPrice: 0
})

const productOptions = ref([])

async function searchProducts(query) {
  if (!query || query.length < 1) {
    productOptions.value = []
    return
  }
  try {
    const res = await getProducts({ page: 1, size: 20, productName: query, productCode: query })
    const list = res.data?.records || res.data || []
    productOptions.value = list.map(p => ({
      id: p.id,
      name: p.productName,
      code: p.productCode || '',
      model: p.model || p.carModel || '',
      unitPrice: p.unitPrice || 0
    }))
  } catch (e) {
    console.error(e)
    productOptions.value = []
  }
}

function handleProductChange(index, productId) {
  const product = productOptions.value.find(p => p.id === productId)
  if (product) {
    quoteForm.items[index].productId = product.id
    quoteForm.items[index].productName = product.name
    quoteForm.items[index].productModel = product.model
    quoteForm.items[index].unitPrice = product.unitPrice
  }
}

const quoteForm = reactive({
  id: null,
  quoteNo: '',
  companyId: null,
  companyName: '',
  validDate: null,
  remark: '',
  items: [defaultItem()]
})

const quoteTotal = computed(() => {
  const total = quoteForm.items.reduce((sum, item) => {
    return sum + (item.quantity || 0) * (item.unitPrice || 0)
  }, 0)
  return total.toFixed(2)
})

const stats = computed(() => ({
  total: quotes.value.length,
  sent: quotes.value.filter(q => q.status === 'sent').length,
  accepted: quotes.value.filter(q => q.status === 'accepted').length,
  rejected: quotes.value.filter(q => q.status === 'rejected').length
}))

onMounted(() => {
  loadQuotes()
  loadCompanies()
})

async function loadQuotes() {
  loading.value = true
  try {
    const res = await getQuotes({
      page: currentPage.value,
      size: pageSize.value,
      companyName: searchForm.companyName,
      status: searchForm.status
    })
    quotes.value = res.data?.records || res.data || []
    total.value = res.data?.total || quotes.value.length
  } catch (e) {
    console.error(e)
    ElMessage.error('加载报价失败')
  } finally {
    loading.value = false
  }
}

async function loadCompanies() {
  try {
    const res = await getCompanies()
    companies.value = res.data?.records || res.data || []
  } catch (e) {
    console.error(e)
  }
}

function handleSearch() {
  currentPage.value = 1
  loadQuotes()
}

function handleReset() {
  searchForm.companyName = ''
  searchForm.status = ''
  searchForm.dateRange = null
  currentPage.value = 1
  loadQuotes()
}

function handleSizeChange(size) {
  pageSize.value = size
  currentPage.value = 1
  loadQuotes()
}

function handlePageChange(page) {
  currentPage.value = page
  loadQuotes()
}

function openCreateDialog() {
  isEdit.value = false
  resetForm()
  createDialogVisible.value = true
}

function addItem() {
  quoteForm.items.push(defaultItem())
}

function removeItem(index) {
  if (quoteForm.items.length <= 1) {
    ElMessage.warning('至少需要保留一个产品')
    return
  }
  quoteForm.items.splice(index, 1)
}

async function viewQuote(row) {
  try {
    const res = await getQuote(row.id)
    viewQuoteData.value = res.data
    viewDialogVisible.value = true
  } catch (e) {
    console.error(e)
    ElMessage.error('加载详情失败')
  }
}

async function editQuote(row) {
  isEdit.value = true
  try {
    const res = await getQuote(row.id)
    const data = res.data
    Object.assign(quoteForm, {
      id: data.id,
      quoteNo: data.quoteNo,
      companyId: data.companyId,
      companyName: data.companyName,
      validDate: data.validDate,
      remark: data.remark
    })
    if (data.items && data.items.length) {
      quoteForm.items = data.items.map(item => ({
        productName: item.productName || '',
        productModel: item.productModel || '',
        quantity: item.quantity || 1,
        unitPrice: item.unitPrice || 0
      }))
    } else {
      // 兼容旧数据
      quoteForm.items = [{
        productName: data.productName || '',
        productModel: data.productModel || '',
        quantity: data.quantity || 1,
        unitPrice: data.unitPrice || 0
      }]
    }
    createDialogVisible.value = true
  } catch (e) {
    console.error(e)
    ElMessage.error('加载报价失败')
  }
}

async function saveQuote() {
  if (!quoteForm.companyId) {
    ElMessage.warning('请选择客户')
    return
  }
  if (!quoteForm.items || quoteForm.items.length === 0) {
    ElMessage.warning('请至少添加一个产品')
    return
  }
  for (let i = 0; i < quoteForm.items.length; i++) {
    const item = quoteForm.items[i]
    if (!item.productName) {
      ElMessage.warning(`第${i + 1}行产品名称不能为空`)
      return
    }
    if (!item.quantity || item.quantity < 1) {
      ElMessage.warning(`第${i + 1}行数量无效`)
      return
    }
    if (item.unitPrice == null || item.unitPrice < 0) {
      ElMessage.warning(`第${i + 1}行单价无效`)
      return
    }
  }

  const payload = {
    id: quoteForm.id,
    quoteNo: quoteForm.quoteNo,
    companyId: quoteForm.companyId,
    validUntil: quoteForm.validDate,
    notes: quoteForm.remark,
    items: quoteForm.items.map(item => ({
      productName: item.productName,
      productModel: item.productModel,
      quantity: item.quantity,
      unitPrice: item.unitPrice
    }))
  }

  try {
    if (isEdit.value) {
      await updateQuote(quoteForm.id, payload)
      ElMessage.success('报价已更新')
    } else {
      await createQuote(payload)
      ElMessage.success('报价已创建')
    }
    createDialogVisible.value = false
    loadQuotes()
    resetForm()
  } catch (e) {
    console.error(e)
    ElMessage.error('保存失败')
  }
}

async function sendQuote(row) {
  try {
    await updateQuote(row.id, { status: 'sent' })
    ElMessage.success('报价已发送')
    loadQuotes()
  } catch (e) {
    console.error(e)
    ElMessage.error('发送失败')
  }
}

async function deleteQuote(row) {
  await ElMessageBox.confirm('确定要删除该报价吗？', '确认删除', { type: 'warning' })
  try {
    await deleteQuoteApi(row.id)
    ElMessage.success('已删除')
    loadQuotes()
  } catch (e) {
    console.error(e)
    ElMessage.error('删除失败')
  }
}

function resetForm() {
  isEdit.value = false
  Object.assign(quoteForm, {
    id: null,
    quoteNo: '',
    companyId: null,
    companyName: '',
    validDate: null,
    remark: ''
  })
  quoteForm.items = [defaultItem()]
}

function getStatusType(status) {
  switch (status) {
    case 'draft': return 'info'
    case 'sent': return 'warning'
    case 'accepted': return 'success'
    case 'rejected': return 'danger'
    case 'expired': return 'default'
    default: return 'info'
  }
}

function getStatusLabel(status) {
  switch (status) {
    case 'draft': return '草稿'
    case 'sent': return '已发送'
    case 'accepted': return '已接受'
    case 'rejected': return '已拒绝'
    case 'expired': return '过期'
    default: return '未知'
  }
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`
}

function formatDateTime(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

async function exportQuotes() {
  try {
    const res = await request.get('/quotes/export', { responseType: 'blob' })
    const blob = new Blob([res], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = '报价单列表.xlsx'
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
    const res = await request.post('/quotes/import-preview', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
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
    await request.post('/quotes/import-confirm', null, { params: { tempId: importTempId.value } })
    ElMessage.success('导入成功')
    importPreviewVisible.value = false
    loadQuotes()
  } catch (e) {
    ElMessage.error('导入失败')
  } finally {
    importLoading.value = false
  }
}

async function cancelImport() {
  if (importTempId.value) {
    try {
      await request.post('/quotes/import-cancel', null, { params: { tempId: importTempId.value } })
    } catch (e) {}
  }
  importPreviewVisible.value = false
  importTempId.value = ''
  importPreviewList.value = []
  importPreviewTotal.value = 0
}
</script>

<style scoped>
.search-form {
  margin-bottom: 20px;
}
.stats-row {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}
.stat-card {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 16px;
}
.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  color: white;
}
.bg-blue { background: #3b82f6; }
.bg-green { background: #10b981; }
.bg-orange { background: #f59e0b; }
.bg-red { background: #ef4444; }
.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #1f2937;
}
.stat-label {
  font-size: 14px;
  color: #6b7280;
  margin-top: 4px;
}
.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
.quote-detail {
  padding: 10px;
}
.detail-section-title {
  font-size: 16px;
  font-weight: bold;
  margin: 20px 0 10px;
  padding-left: 8px;
  border-left: 4px solid #409eff;
}
.product-line {
  font-size: 13px;
  line-height: 1.6;
}
.product-line.more {
  color: #909399;
}
</style>
