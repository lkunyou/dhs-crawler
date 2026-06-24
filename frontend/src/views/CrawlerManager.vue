<template>
  <div class="crawler-manager">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>爬虫管理 - 泰国汽配客户抓取</span>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="Google搜索" name="google">
          <BaseForm :model-value="googleForm" label-width="120px">
            <FormField type="select" label="搜索关键词" prop="keywords" v-model="googleForm.keywords" :options="googleKeywordOptions" :multiple="true" :filterable="true" :allow-create="true" />
            <FormField type="input" label="目标地区" prop="location" v-model="googleForm.location" placeholder="Thailand" />
            <FormField type="number" label="每关键词结果数" prop="maxResults" v-model="googleForm.maxResults" :min="10" :max="100" />
            <el-form-item>
              <el-button type="primary" @click="startGoogleCrawl" :loading="crawling">
                <el-icon><VideoPlay /></el-icon> 开始抓取
              </el-button>
            </el-form-item>
          </BaseForm>
        </el-tab-pane>

        <el-tab-pane label="Google Maps" name="maps">
          <BaseForm :model-value="mapsForm" label-width="120px">
            <FormField type="select" label="搜索关键词" prop="keywords" v-model="mapsForm.keywords" :options="mapsKeywordOptions" :multiple="true" :filterable="true" :allow-create="true" />
            <FormField type="select" label="目标城市" prop="city" v-model="mapsForm.city" :options="cityOptions" />
            <el-form-item>
              <el-button type="primary" @click="startMapsCrawl" :loading="crawling">
                <el-icon><VideoPlay /></el-icon> 开始抓取
              </el-button>
            </el-form-item>
          </BaseForm>
        </el-tab-pane>

        <el-tab-pane label="LinkedIn" name="linkedin">
          <el-alert title="需要配置LinkedIn Session Cookie" type="warning" :closable="false" style="margin-bottom: 20px" />
          <BaseForm :model-value="linkedinForm" label-width="120px">
            <FormField type="select" label="目标职位" prop="titles" v-model="linkedinForm.titles" :options="linkedinTitleOptions" :multiple="true" :filterable="true" :allow-create="true" />
            <FormField type="select" label="公司关键词" prop="companyKeywords" v-model="linkedinForm.companyKeywords" :options="linkedinCompanyOptions" :multiple="true" :filterable="true" :allow-create="true" />
            <el-form-item>
              <el-button type="primary" @click="startLinkedInCrawl" :loading="crawling">
                <el-icon><VideoPlay /></el-icon> 开始抓取
              </el-button>
            </el-form-item>
          </BaseForm>
        </el-tab-pane>

        <el-tab-pane label="任务历史" name="history">
          <BaseTable :data="taskHistory" :columns="taskHistoryColumns" :show-pagination="false" />
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../utils/request'
import { BaseForm, BaseTable, FormField } from '@/components'

const activeTab = ref('google')
const crawling = ref(false)

const googleKeywordOptions = [
  { label: 'auto parts distributor Thailand', value: 'auto parts distributor Thailand' },
  { label: 'car parts importer Bangkok', value: 'car parts importer Bangkok' },
  { label: 'automotive parts wholesale Thailand', value: 'automotive parts wholesale Thailand' },
  { label: 'OEM automotive parts Thailand', value: 'OEM automotive parts Thailand' },
  { label: 'car accessories distributor', value: 'car accessories distributor' },
  { label: 'auto spare parts Thailand', value: 'auto spare parts Thailand' },
  { label: 'truck parts distributor Thailand', value: 'truck parts distributor Thailand' }
]

const mapsKeywordOptions = [
  { label: 'auto parts shop Bangkok', value: 'auto parts shop Bangkok' },
  { label: 'car parts store Chiang Mai', value: 'car parts store Chiang Mai' },
  { label: 'auto accessories Phuket', value: 'auto accessories Phuket' },
  { label: 'truck parts dealer', value: 'truck parts dealer' }
]

const cityOptions = [
  { label: 'Bangkok', value: 'Bangkok' },
  { label: 'Chiang Mai', value: 'Chiang Mai' },
  { label: 'Chonburi', value: 'Chonburi' },
  { label: 'Rayong', value: 'Rayong' },
  { label: 'Samut Prakan', value: 'Samut Prakan' },
  { label: 'Nonthaburi', value: 'Nonthaburi' }
]

const linkedinTitleOptions = [
  { label: 'Purchasing Manager', value: 'Purchasing Manager' },
  { label: 'Procurement Manager', value: 'Procurement Manager' },
  { label: 'Owner', value: 'Owner' },
  { label: 'Import Manager', value: 'Import Manager' },
  { label: 'Director', value: 'Director' }
]

const linkedinCompanyOptions = [
  { label: 'automotive parts Thailand', value: 'automotive parts Thailand' },
  { label: 'auto parts distributor', value: 'auto parts distributor' },
  { label: 'aftermarket Thailand', value: 'aftermarket Thailand' }
]

const taskHistoryColumns = [
  { prop: 'taskName', label: '任务名称', minWidth: 150 },
  { prop: 'sourceType', label: '数据源', width: 120 },
  { prop: 'status', label: '状态', width: 100, type: 'tag', tagType: (row) => getTaskStatusType(row.status), tagLabel: (row) => getTaskStatusLabel(row.status) },
  { prop: 'totalFound', label: '发现总数', width: 100 },
  { prop: 'newCompanies', label: '新增公司', width: 100 },
  { prop: 'duplicates', label: '重复数', width: 100 },
  { prop: 'progress', label: '进度', width: 150, type: 'custom', render: (row) => `<el-progress :percentage="${row.progress}" :stroke-width="8" />` },
  { prop: 'startedAt', label: '开始时间', width: 180 },
  { prop: 'completedAt', label: '完成时间', width: 180 }
]

const googleForm = reactive({
  keywords: ['auto parts distributor Thailand', 'car parts importer Bangkok'],
  location: 'Thailand',
  maxResults: 50
})

const mapsForm = reactive({
  keywords: ['auto parts shop Bangkok'],
  city: 'Bangkok'
})

const linkedinForm = reactive({
  titles: ['Purchasing Manager', 'Procurement Manager'],
  companyKeywords: ['automotive parts Thailand']
})

const taskHistory = ref([])

async function loadTaskHistory() {
  try {
    const response = await api.get('/crawler/tasks')
    taskHistory.value = response.data || []
  } catch (e) {
    console.error('加载任务历史失败:', e)
  }
}

async function startGoogleCrawl() {
  crawling.value = true
  try {
    const task = {
      taskName: `Google搜索-${googleForm.keywords.join(',')}`,
      sourceType: 'Google_Search',
      keywords: JSON.stringify(googleForm.keywords),
      targetCountry: googleForm.location,
      filters: JSON.stringify({ maxResults: googleForm.maxResults })
    }
    
    const createResponse = await api.post('/crawler/task', task)
    const taskId = createResponse.data.id
    
    await api.post(`/crawler/task/${taskId}/start`)
    ElMessage.success('Google搜索爬虫已启动')
    
    loadTaskHistory()
  } catch (e) {
    ElMessage.error('启动失败: ' + (e.response?.data?.message || e.message))
  } finally {
    crawling.value = false
  }
}

async function startMapsCrawl() {
  crawling.value = true
  try {
    const task = {
      taskName: `Google Maps-${mapsForm.keywords.join(',')}-${mapsForm.city}`,
      sourceType: 'Google_Maps',
      keywords: JSON.stringify(mapsForm.keywords),
      targetCity: mapsForm.city,
      targetCountry: 'Thailand'
    }
    
    const createResponse = await api.post('/crawler/task', task)
    const taskId = createResponse.data.id
    
    await api.post(`/crawler/task/${taskId}/start`)
    ElMessage.success('Google Maps爬虫已启动')
    
    loadTaskHistory()
  } catch (e) {
    ElMessage.error('启动失败: ' + (e.response?.data?.message || e.message))
  } finally {
    crawling.value = false
  }
}

async function startLinkedInCrawl() {
  crawling.value = true
  try {
    const task = {
      taskName: `LinkedIn-${linkedinForm.titles.join(',')}`,
      sourceType: 'LinkedIn',
      keywords: JSON.stringify(linkedinForm.titles),
      filters: JSON.stringify({ companyKeywords: linkedinForm.companyKeywords }),
      targetCountry: 'Thailand'
    }
    
    const createResponse = await api.post('/crawler/task', task)
    const taskId = createResponse.data.id
    
    await api.post(`/crawler/task/${taskId}/start`)
    ElMessage.success('LinkedIn爬虫已启动')
    
    loadTaskHistory()
  } catch (e) {
    ElMessage.error('启动失败: ' + (e.response?.data?.message || e.message))
  } finally {
    crawling.value = false
  }
}

onMounted(() => {
  loadTaskHistory()
})

function getTaskStatusType(status) {
  const types = { Pending: 'info', Running: '', Completed: 'success', Failed: 'danger', Paused: 'warning' }
  return types[status] || ''
}

function getTaskStatusLabel(status) {
  const labels = { Pending: '待执行', Running: '执行中', Completed: '已完成', Failed: '失败', Paused: '已暂停' }
  return labels[status] || status
}
</script>

<style scoped>
.crawler-manager {
  padding: 20px;
}

.card-header {
  font-weight: bold;
}
</style>