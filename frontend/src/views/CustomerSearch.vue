<template>
  <div class="customer-search">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>客户搜索</span>
          <div class="header-actions">
            <el-tag type="info">支持 SerpAPI / Brave / Bing / DuckDuckGo / LinkedIn / Yellow Pages / URL导入</el-tag>
          </div>
        </div>
      </template>

      <!-- 搜索区域 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="搜索关键词">
          <el-input
            v-model="searchForm.keyword"
            placeholder="例如: auto parts, brake pads, engine parts"
            style="width: 300px"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="数据源">
          <el-select v-model="searchForm.source" style="width: 180px">
            <el-option label="Brave Search (推荐)" value="brave" />
            <el-option label="SerpAPI" value="serpapi" />
            <el-option label="Bing" value="bing" />
            <el-option label="DuckDuckGo" value="duckduckgo" />
            <el-option label="LinkedIn" value="linkedin" />
            <el-option label="Yellow Pages" value="yellowpages" />
          </el-select>
        </el-form-item>
        <el-form-item label="国家">
          <el-select v-model="searchForm.country" style="width: 120px">
            <el-option label="泰国" value="TH" />
            <el-option label="越南" value="VN" />
            <el-option label="马来西亚" value="MY" />
            <el-option label="印尼" value="ID" />
            <el-option label="菲律宾" value="PH" />
            <el-option label="新加坡" value="SG" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch" :loading="searching">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- URL导入区域 -->
      <el-collapse v-model="activeCollapse" style="margin-bottom: 20px">
        <el-collapse-item title="URL导入" name="url">
          <el-form :inline="true">
            <el-form-item label="网站URL">
              <el-input
                v-model="urlInput"
                placeholder="请输入网站URL，例如: https://example.com"
                style="width: 400px"
                clearable
                @keyup.enter="handleFetchUrl"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleFetchUrl" :loading="fetchingUrl">获取内容</el-button>
            </el-form-item>
          </el-form>
        </el-collapse-item>
      </el-collapse>

      <!-- 批量搜索 -->
      <el-collapse v-model="activeCollapse" style="margin-bottom: 20px">
        <el-collapse-item title="批量搜索" name="batch">
          <el-form :inline="true">
            <el-form-item label="关键词列表">
              <el-input
                v-model="batchKeywords"
                type="textarea"
                :rows="3"
                placeholder="每行一个关键词，例如：&#10;brake pads&#10;engine parts&#10;suspension"
                style="width: 500px"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="warning" @click="handleBatchSearch" :loading="searching">批量搜索</el-button>
            </el-form-item>
          </el-form>
        </el-collapse-item>
      </el-collapse>

      <!-- 搜索结果 -->
      <div v-if="searchResults.length > 0" class="results-section">
        <div class="results-header">
          <span>搜索结果 ({{ searchResults.length }} 条)</span>
          <el-button type="success" size="small" @click="handleImportSelected" :disabled="selectedRows.length === 0">
            导入选中 ({{ selectedRows.length }})
          </el-button>
          <el-button type="primary" size="small" @click="handleImportAll">全部导入</el-button>
        </div>

        <el-table
          :data="searchResults"
          border
          @selection-change="handleSelectionChange"
          class="results-table"
        >
          <el-table-column type="selection" width="50" />
          <el-table-column prop="companyName" label="公司名称" min-width="200">
            <template #default="{ row }">
              <span style="font-weight: 500">{{ row.companyName }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="website" label="官网" min-width="180">
            <template #default="{ row }">
              <el-link v-if="row.website" :href="row.website" target="_blank" type="primary">
                {{ row.website }}
              </el-link>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column prop="email" label="邮箱" width="180">
            <template #default="{ row }">
              <span v-if="row.email">{{ row.email }}</span>
              <span v-else style="color: #ccc">-</span>
            </template>
          </el-table-column>
          <el-table-column prop="phone" label="电话" width="140">
            <template #default="{ row }">
              <span v-if="row.phone">{{ row.phone }}</span>
              <span v-else style="color: #ccc">-</span>
            </template>
          </el-table-column>
          <el-table-column prop="source" label="来源" width="120">
            <template #default="{ row }">
              <el-tag size="small" type="info">{{ row.source }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="country" label="国家" width="80" />
          <el-table-column label="操作" width="100" fixed="right">
            <template #default="{ row }">
              <el-button type="primary" size="small" @click="handleImportOne(row)">导入</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 空状态 -->
      <el-empty v-else description="请输入关键词开始搜索" />
    </el-card>

    <!-- 导入确认弹窗 -->
    <el-dialog v-model="importDialogVisible" title="确认导入客户" width="500px">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="公司名称">{{ importForm.companyName }}</el-descriptions-item>
        <el-descriptions-item label="官网">{{ importForm.website || '-' }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ importForm.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="电话">{{ importForm.phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="来源">{{ importForm.source }}</el-descriptions-item>
        <el-descriptions-item label="国家">{{ importForm.country }}</el-descriptions-item>
      </el-descriptions>
      <el-form :model="importForm" style="margin-top: 20px" label-width="80px">
        <el-form-item label="公司类型">
          <el-select v-model="importForm.companyType" style="width: 100%">
            <el-option label="批发商" value="Distributor" />
            <el-option label="进口商" value="Importer" />
            <el-option label="零售商" value="Retailer" />
            <el-option label="维修厂" value="Repair_Shop" />
            <el-option label="制造商" value="Manufacturer" />
            <el-option label="经销商" value="Dealer" />
            <el-option label="其他" value="Other" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="importDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmImport">确认导入</el-button>
      </template>
    </el-dialog>

    <!-- URL预览弹窗 -->
    <el-dialog v-model="urlPreviewVisible" title="URL内容预览" width="600px" destroy-on-close>
      <div v-if="urlPreviewData">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="公司名称">{{ urlPreviewData.companyName || '-' }}</el-descriptions-item>
          <el-descriptions-item label="官网">
            <el-link v-if="urlPreviewData.website" :href="urlPreviewData.website" target="_blank" type="primary">
              {{ urlPreviewData.website }}
            </el-link>
            <span v-else>-</span>
          </el-descriptions-item>
          <el-descriptions-item label="邮箱">{{ urlPreviewData.email || '-' }}</el-descriptions-item>
          <el-descriptions-item label="电话">{{ urlPreviewData.phone || '-' }}</el-descriptions-item>
          <el-descriptions-item label="描述">{{ urlPreviewData.description || '-' }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <template #footer>
        <el-button @click="urlPreviewVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmImportFromUrl">确认导入</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { searchCompanies, batchSearchCompanies, importCompany, fetchUrl } from '@/api/customerSearch'

const searching = ref(false)
const fetchingUrl = ref(false)
const activeCollapse = ref([])
const batchKeywords = ref('')
const urlInput = ref('')
const urlPreviewData = ref(null)
const urlPreviewVisible = ref(false)
const searchResults = ref([])
const selectedRows = ref([])
const importDialogVisible = ref(false)

const searchForm = reactive({
  keyword: '',
  source: 'brave',
  country: 'TH'
})

const importForm = reactive({
  companyName: '',
  website: '',
  email: '',
  phone: '',
  source: '',
  country: 'TH',
  companyType: 'Other',
  description: ''
})

async function handleSearch() {
  if (!searchForm.keyword) {
    ElMessage.warning('请输入搜索关键词')
    return
  }
  searching.value = true
  try {
    const res = await searchCompanies({
      keyword: searchForm.keyword,
      source: searchForm.source,
      country: searchForm.country
    })
    searchResults.value = res.data || []
    if (searchResults.value.length === 0) {
      ElMessage.info('未找到相关结果，请尝试其他关键词或数据源')
    }
  } catch (e) {
    ElMessage.error('搜索失败: ' + (e.message || '请检查API配置'))
    console.error(e)
  } finally {
    searching.value = false
  }
}

async function handleBatchSearch() {
  const keywords = batchKeywords.value.split('\n').map(k => k.trim()).filter(k => k)
  if (keywords.length === 0) {
    ElMessage.warning('请输入关键词')
    return
  }
  searching.value = true
  try {
    const res = await batchSearchCompanies(keywords, searchForm.source, searchForm.country)
    searchResults.value = res.data || []
    ElMessage.success(`批量搜索完成，共找到 ${searchResults.value.length} 条结果`)
  } catch (e) {
    ElMessage.error('批量搜索失败')
    console.error(e)
  } finally {
    searching.value = false
  }
}

function handleReset() {
  searchForm.keyword = ''
  searchForm.source = 'brave'
  searchForm.country = 'TH'
  searchResults.value = []
  selectedRows.value = []
  batchKeywords.value = ''
}

async function handleFetchUrl() {
  const url = urlInput.value.trim()
  if (!url) {
    ElMessage.warning('请输入URL地址')
    return
  }
  fetchingUrl.value = true
  try {
    const res = await fetchUrl(url, searchForm.keyword)
    urlPreviewData.value = res.data
    urlPreviewVisible.value = true
  } catch (e) {
    ElMessage.error('获取URL内容失败: ' + (e.message || '请检查URL是否正确'))
    console.error(e)
  } finally {
    fetchingUrl.value = false
  }
}

function confirmImportFromUrl() {
  if (!urlPreviewData.value) return
  Object.assign(importForm, {
    companyName: urlPreviewData.value.companyName || '',
    website: urlPreviewData.value.website || '',
    email: urlPreviewData.value.email || '',
    phone: urlPreviewData.value.phone || '',
    source: urlPreviewData.value.source || 'URL导入',
    country: urlPreviewData.value.country || 'TH',
    companyType: 'Other',
    description: urlPreviewData.value.description || ''
  })
  urlPreviewVisible.value = false
  importDialogVisible.value = true
}

function handleSelectionChange(rows) {
  selectedRows.value = rows
}

function handleImportOne(row) {
  Object.assign(importForm, {
    companyName: row.companyName || '',
    website: row.website || '',
    email: row.email || '',
    phone: row.phone || '',
    source: row.source || '',
    country: row.country || 'TH',
    companyType: 'Other',
    description: row.description || ''
  })
  importDialogVisible.value = true
}

async function handleImportSelected() {
  if (selectedRows.value.length === 0) {
    ElMessage.warning('请选择要导入的客户')
    return
  }
  await ElMessageBox.confirm(
    `确定要导入选中的 ${selectedRows.value.length} 个客户吗？`,
    '导入确认',
    { type: 'warning' }
  )
  let success = 0
  let fail = 0
  for (const row of selectedRows.value) {
    try {
      await importCompany({
        companyName: row.companyName,
        website: row.website,
        email: row.email,
        phone: row.phone,
        source: row.source,
        country: row.country,
        companyType: 'Other',
        description: row.description || ''
      })
      success++
    } catch (e) {
      fail++
    }
  }
  ElMessage.success(`导入完成：成功 ${success} 个，失败 ${fail} 个`)
}

async function handleImportAll() {
  if (searchResults.value.length === 0) return
  await ElMessageBox.confirm(
    `确定要导入全部 ${searchResults.value.length} 个客户吗？`,
    '导入确认',
    { type: 'warning' }
  )
  let success = 0
  let fail = 0
  for (const row of searchResults.value) {
    try {
      await importCompany({
        companyName: row.companyName,
        website: row.website,
        email: row.email,
        phone: row.phone,
        source: row.source,
        country: row.country,
        companyType: 'Other',
        description: row.description || ''
      })
      success++
    } catch (e) {
      fail++
    }
  }
  ElMessage.success(`导入完成：成功 ${success} 个，失败 ${fail} 个`)
}

async function confirmImport() {
  if (!importForm.companyName) {
    ElMessage.warning('公司名称不能为空')
    return
  }
  try {
    await importCompany({
      companyName: importForm.companyName,
      website: importForm.website,
      email: importForm.email,
      phone: importForm.phone,
      source: importForm.source,
      country: importForm.country,
      companyType: importForm.companyType,
      description: importForm.description
    })
    ElMessage.success('客户导入成功')
    importDialogVisible.value = false
  } catch (e) {
    ElMessage.error('导入失败')
    console.error(e)
  }
}
</script>

<style scoped>
.customer-search {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.search-form {
  margin-bottom: 10px;
}

.results-section {
  margin-top: 20px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  font-weight: bold;
}

.results-table {
  margin-top: 10px;
}
</style>