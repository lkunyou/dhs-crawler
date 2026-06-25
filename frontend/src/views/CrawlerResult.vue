<template>
  <div class="crawler-result-page">
    <!-- 统计卡片 -->
    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value">{{ stats.pending || 0 }}</div>
            <div class="stat-label">待确认</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value" style="color: #67C23A">{{ stats.confirmed || 0 }}</div>
            <div class="stat-label">已确认</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value" style="color: #409EFF">{{ stats.synced || 0 }}</div>
            <div class="stat-label">已同步</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value" style="color: #F56C6C">{{ stats.rejected || 0 }}</div>
            <div class="stat-label">已拒绝</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 筛选栏 -->
    <el-card style="margin-bottom: 20px">
      <el-form :inline="true">
        <el-form-item label="任务">
          <el-select v-model="filters.taskId" placeholder="选择任务" clearable style="width: 200px">
            <el-option v-for="t in taskList" :key="t.id" :label="t.taskName" :value="t.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="filters.status" placeholder="全部" clearable style="width: 120px">
            <el-option label="待确认" value="Pending" />
            <el-option label="已确认" value="Confirmed" />
            <el-option label="已同步" value="Synced" />
            <el-option label="已拒绝" value="Rejected" />
            <el-option label="重复" value="Duplicate" />
          </el-select>
        </el-form-item>
        <el-form-item label="来源">
          <el-select v-model="filters.sourceType" placeholder="全部" clearable style="width: 150px">
            <el-option label="Google搜索" value="Google_Search" />
            <el-option label="Google Maps" value="Google_Maps" />
            <el-option label="LinkedIn" value="LinkedIn" />
            <el-option label="B2B平台" value="B2B_Platform" />
            <el-option label="行业目录" value="Industry_Directory" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadResults">查询</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 批量操作 -->
    <el-card style="margin-bottom: 20px">
      <el-button type="success" :disabled="selectedIds.length === 0" @click="handleBatchSync">
        批量同步到客户管理 ({{ selectedIds.length }})
      </el-button>
      <el-button type="danger" :disabled="selectedIds.length === 0" @click="showBatchRejectDialog">
        批量拒绝 ({{ selectedIds.length }})
      </el-button>
    </el-card>

    <!-- 结果表格 -->
    <el-card>
      <el-table
        :data="results"
        style="width: 100%"
        @selection-change="handleSelectionChange"
        v-loading="loading"
      >
        <el-table-column type="selection" width="50" />
        <el-table-column prop="companyName" label="公司名称" min-width="180" show-overflow-tooltip />
        <el-table-column prop="sourceType" label="来源" width="120">
          <template #default="{ row }">
            <el-tag size="small">{{ getSourceLabel(row.sourceType) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="website" label="网站" width="180" show-overflow-tooltip />
        <el-table-column prop="phone" label="电话" width="130" />
        <el-table-column prop="email" label="邮箱" width="180" show-overflow-tooltip />
        <el-table-column prop="leadGrade" label="等级" width="80">
          <template #default="{ row }">
            <el-tag :type="getGradeType(row.leadGrade)" size="small">{{ row.leadGrade }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">{{ getStatusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="showDetail(row)">详情</el-button>
            <template v-if="row.status === 'Pending'">
              <el-button size="small" type="success" @click="handleConfirm(row)">确认</el-button>
              <el-button size="small" type="primary" @click="handleSync(row)">同步</el-button>
              <el-button size="small" type="danger" @click="handleReject(row)">拒绝</el-button>
            </template>
            <el-button v-if="row.status === 'Synced'" size="small" type="info" disabled>已同步</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        style="margin-top: 20px; justify-content: flex-end"
        :current-page="pagination.page"
        :page-size="pagination.size"
        :total="pagination.total"
        layout="total, prev, pager, next"
        @current-change="handlePageChange"
      />
    </el-card>

    <!-- 详情对话框 -->
    <el-dialog v-model="showDetailDialog" title="抓取详情" width="800px">
      <el-descriptions :column="2" border v-if="detailResult">
        <el-descriptions-item label="公司名称">{{ detailResult.companyName }}</el-descriptions-item>
        <el-descriptions-item label="泰文名称">{{ detailResult.companyNameTh || '-' }}</el-descriptions-item>
        <el-descriptions-item label="英文名称">{{ detailResult.companyNameEn || '-' }}</el-descriptions-item>
        <el-descriptions-item label="公司类型">{{ detailResult.companyType || '-' }}</el-descriptions-item>
        <el-descriptions-item label="网站" :span="2">
          <a :href="detailResult.website" target="_blank">{{ detailResult.website || '-' }}</a>
        </el-descriptions-item>
        <el-descriptions-item label="地址" :span="2">{{ detailResult.address || '-' }}</el-descriptions-item>
        <el-descriptions-item label="城市">{{ detailResult.city || '-' }}</el-descriptions-item>
        <el-descriptions-item label="省份">{{ detailResult.province || '-' }}</el-descriptions-item>
        <el-descriptions-item label="电话">{{ detailResult.phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="WhatsApp">{{ detailResult.whatsapp || '-' }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ detailResult.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="员工规模">{{ detailResult.employeeCount || '-' }}</el-descriptions-item>
        <el-descriptions-item label="汽配核心业务">
          {{ detailResult.isAutoPartsCore ? '是' : '否' }}
        </el-descriptions-item>
        <el-descriptions-item label="进口/分销商">
          {{ detailResult.isImporterDistributor ? '是' : '否' }}
        </el-descriptions-item>
        <el-descriptions-item label="客户评分">{{ detailResult.leadScore }}分</el-descriptions-item>
        <el-descriptions-item label="客户等级">
          <el-tag :type="getGradeType(detailResult.leadGrade)">{{ detailResult.leadGrade }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="来源URL" :span="2">
          <a :href="detailResult.sourceUrl" target="_blank">{{ detailResult.sourceUrl || '-' }}</a>
        </el-descriptions-item>
        <el-descriptions-item label="搜索关键词">{{ detailResult.searchKeyword || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">{{ getStatusLabel(detailResult.status) }}</el-descriptions-item>
      </el-descriptions>
      <div v-if="detailResult && detailResult.rawData" style="margin-top: 15px">
        <h4>原始数据</h4>
        <pre style="background: #f5f7fa; padding: 10px; border-radius: 4px; max-height: 200px; overflow: auto">{{ formatJson(detailResult.rawData) }}</pre>
      </div>
    </el-dialog>

    <!-- 拒绝对话框 -->
    <el-dialog v-model="showRejectDialog" title="拒绝原因" width="400px">
      <el-input v-model="rejectReason" type="textarea" :rows="3" placeholder="请输入拒绝原因..." />
      <template #footer>
        <el-button @click="showRejectDialog = false">取消</el-button>
        <el-button type="danger" @click="confirmReject">确认拒绝</el-button>
      </template>
    </el-dialog>

    <!-- 批量拒绝对话框 -->
    <el-dialog v-model="showBatchRejectDialogFlag" title="批量拒绝" width="400px">
      <el-input v-model="batchRejectReason" type="textarea" :rows="3" placeholder="请输入拒绝原因..." />
      <template #footer>
        <el-button @click="showBatchRejectDialogFlag = false">取消</el-button>
        <el-button type="danger" @click="confirmBatchReject">确认拒绝</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const loading = ref(false)
const results = ref([])
const selectedIds = ref([])
const stats = reactive({ pending: 0, confirmed: 0, synced: 0, rejected: 0 })
const taskList = ref([])

const filters = reactive({
  taskId: null,
  status: 'Pending',
  sourceType: ''
})

const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

const showDetailDialog = ref(false)
const showRejectDialog = ref(false)
const showBatchRejectDialogFlag = ref(false)
const detailResult = ref(null)
const rejectReason = ref('')
const batchRejectReason = ref('')
const currentRejectId = ref(null)

onMounted(() => {
  loadResults()
  loadTaskList()
})

async function loadResults() {
  loading.value = true
  try {
    const params = new URLSearchParams({
      page: pagination.page,
      size: pagination.size
    })
    if (filters.taskId) params.append('taskId', filters.taskId)
    if (filters.status) params.append('status', filters.status)
    if (filters.sourceType) params.append('sourceType', filters.sourceType)

    const res = await fetch(`/api/crawler-result/list?${params}`)
    const data = await res.json()
    if (data.code === 200) {
      results.value = data.data.records
      pagination.total = data.data.total
      updateStats(data.data.records)
    }
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

async function loadTaskList() {
  try {
    const res = await fetch('/api/crawler/tasks')
    const data = await res.json()
    if (data.code === 200) {
      taskList.value = data.data
    }
  } catch (e) {}
}

function updateStats(records) {
  stats.pending = records.filter(r => r.status === 'Pending').length
  stats.confirmed = records.filter(r => r.status === 'Confirmed').length
  stats.synced = records.filter(r => r.status === 'Synced').length
  stats.rejected = records.filter(r => r.status === 'Rejected').length
}

function handleSelectionChange(selection) {
  selectedIds.value = selection.map(s => s.id)
}

function handlePageChange(page) {
  pagination.page = page
  loadResults()
}

function showDetail(row) {
  detailResult.value = row
  showDetailDialog.value = true
}

async function handleConfirm(row) {
  try {
    const res = await fetch(`/api/crawler-result/${row.id}/confirm`, { method: 'POST' })
    const data = await res.json()
    if (data.code === 200) {
      ElMessage.success('已确认')
      loadResults()
    }
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

async function handleSync(row) {
  try {
    const res = await fetch(`/api/crawler-result/${row.id}/sync`, { method: 'POST' })
    const data = await res.json()
    if (data.code === 200) {
      ElMessage.success('已同步到客户管理')
      loadResults()
    } else {
      ElMessage.warning(data.message || '同步失败')
    }
  } catch (e) {
    ElMessage.error('同步失败')
  }
}

function handleReject(row) {
  currentRejectId.value = row.id
  rejectReason.value = ''
  showRejectDialog.value = true
}

async function confirmReject() {
  try {
    const res = await fetch(`/api/crawler-result/${currentRejectId.value}/reject`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason: rejectReason.value })
    })
    const data = await res.json()
    if (data.code === 200) {
      ElMessage.success('已拒绝')
      showRejectDialog.value = false
      loadResults()
    }
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

async function handleBatchSync() {
  try {
    const res = await fetch('/api/crawler-result/batch-sync', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ids: selectedIds.value })
    })
    const data = await res.json()
    if (data.code === 200) {
      ElMessage.success(`已同步 ${data.data.synced} 条`)
      selectedIds.value = []
      loadResults()
    }
  } catch (e) {
    ElMessage.error('批量同步失败')
  }
}

function showBatchRejectDialog() {
  batchRejectReason.value = ''
  showBatchRejectDialogFlag.value = true
}

async function confirmBatchReject() {
  try {
    const res = await fetch('/api/crawler-result/batch-reject', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ids: selectedIds.value, reason: batchRejectReason.value })
    })
    const data = await res.json()
    if (data.code === 200) {
      ElMessage.success(`已拒绝 ${data.data.rejected} 条`)
      showBatchRejectDialogFlag.value = false
      selectedIds.value = []
      loadResults()
    }
  } catch (e) {
    ElMessage.error('批量拒绝失败')
  }
}

function getSourceLabel(source) {
  const labels = {
    Google_Search: 'Google搜索',
    Google_Maps: 'Google Maps',
    LinkedIn: 'LinkedIn',
    B2B_Platform: 'B2B平台',
    Industry_Directory: '行业目录'
  }
  return labels[source] || source
}

function getStatusLabel(status) {
  const labels = {
    Pending: '待确认',
    Confirmed: '已确认',
    Synced: '已同步',
    Rejected: '已拒绝',
    Duplicate: '重复'
  }
  return labels[status] || status
}

function getStatusType(status) {
  const types = { Pending: 'warning', Confirmed: 'success', Synced: '', Rejected: 'danger', Duplicate: 'info' }
  return types[status] || ''
}

function getGradeType(grade) {
  const types = { S: 'danger', A: 'warning', B: '', C: 'info' }
  return types[grade] || ''
}

function formatJson(str) {
  try {
    return JSON.stringify(JSON.parse(str), null, 2)
  } catch {
    return str
  }
}
</script>

<style scoped>
.crawler-result-page { padding: 20px; }
.stat-card { text-align: center; }
.stat-value { font-size: 32px; font-weight: bold; color: #303133; }
.stat-label { font-size: 14px; color: #909399; margin-top: 5px; }
</style>
