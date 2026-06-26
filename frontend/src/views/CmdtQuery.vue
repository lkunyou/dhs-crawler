<template>
  <div class="cmdt-query-container">
    <div class="search-header">
      <el-input 
        v-model="searchKeyword" 
        placeholder="搜索CMDT编码、英文描述或中文描述" 
        clearable
        style="width: 400px;"
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button @click="handleSearch" type="primary">搜索</el-button>
        </template>
      </el-input>
      
      <div class="filter-row">
        <el-select v-model="selectedSection" placeholder="选择大类" clearable @change="handleSectionChange">
          <el-option 
            v-for="section in sections" 
            :key="section.sectionCode" 
            :label="section.section" 
            :value="section.sectionCode" 
          />
        </el-select>
        
        <el-select v-model="selectedChapter" placeholder="选择中类" clearable @change="handleChapterChange" :disabled="!selectedSection">
          <el-option 
            v-for="chapter in chapters" 
            :key="chapter.chapterCode" 
            :label="chapter.chapter" 
            :value="chapter.chapterCode" 
          />
        </el-select>
        
        <el-button @click="resetFilters" type="default">重置筛选</el-button>
      </div>
    </div>

    <el-table :data="tableData" border stripe style="width: 100%" :loading="loading">
      <el-table-column prop="cmdtCode" label="CMDT编码" width="120" fixed="left" />
      <el-table-column prop="descriptionEn" label="英文描述" min-width="250" />
      <el-table-column prop="descriptionCn" label="中文描述" min-width="200" />
      <el-table-column prop="chapterCode" label="HS中类" width="80" />
      <el-table-column prop="chapter" label="中类名称" min-width="200" />
      <el-table-column prop="sectionCode" label="HS大类" width="80" />
      <el-table-column prop="section" label="大类名称" min-width="200" />
    </el-table>

    <el-pagination
      v-model:current-page="currentPage"
      v-model:page-size="pageSize"
      :total="total"
      :page-sizes="[20, 50, 100]"
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const searchKeyword = ref('')
const selectedSection = ref('')
const selectedChapter = ref('')
const sections = ref([])
const chapters = ref([])

const tableData = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)

onMounted(() => {
  loadSections()
  fetchData()
})

async function loadSections() {
  try {
    const response = await axios.get('/api/cmdt/sections')
    sections.value = response.data.data
  } catch (error) {
    console.error('加载大类失败:', error)
  }
}

async function handleSectionChange(value) {
  selectedChapter.value = ''
  chapters.value = []
  if (value) {
    try {
      const response = await axios.get(`/api/cmdt/chapters?sectionCode=${value}`)
      chapters.value = response.data.data
    } catch (error) {
      console.error('加载中类失败:', error)
    }
  }
  currentPage.value = 1
  fetchData()
}

function handleChapterChange(value) {
  currentPage.value = 1
  fetchData()
}

function resetFilters() {
  searchKeyword.value = ''
  selectedSection.value = ''
  selectedChapter.value = ''
  chapters.value = []
  currentPage.value = 1
  fetchData()
}

function handleSearch() {
  currentPage.value = 1
  fetchData()
}

function handleSizeChange(size) {
  pageSize.value = size
  currentPage.value = 1
  fetchData()
}

function handleCurrentChange(page) {
  currentPage.value = page
  fetchData()
}

async function fetchData() {
  loading.value = true
  try {
    let url = `/api/cmdt/search?page=${currentPage.value}&size=${pageSize.value}`
    
    if (searchKeyword.value) {
      url += `&keyword=${encodeURIComponent(searchKeyword.value)}`
    } else if (selectedChapter.value) {
      url = `/api/cmdt/chapter/${selectedChapter.value}?page=${currentPage.value}&size=${pageSize.value}`
    } else if (selectedSection.value) {
      url = `/api/cmdt/section/${selectedSection.value}?page=${currentPage.value}&size=${pageSize.value}`
    }
    
    const response = await axios.get(url)
    tableData.value = response.data.data.records
    total.value = response.data.data.total
  } catch (error) {
    console.error('获取数据失败:', error)
    tableData.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.cmdt-query-container {
  padding: 20px;
}

.search-header {
  margin-bottom: 20px;
}

.filter-row {
  display: flex;
  gap: 10px;
  margin-top: 15px;
  align-items: center;
}

.filter-row .el-select {
  width: 250px;
}
</style>