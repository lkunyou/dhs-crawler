<template>
  <div class="dashboard">
    <el-row :gutter="16" class="stats-row">
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon">
            <el-icon :size="24"><UserFilled /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalCompanies }}</div>
            <div class="stat-label">总客户数</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon">
            <el-icon :size="24"><Message /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.emailsSent }}</div>
            <div class="stat-label">邮件已发送</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon">
            <el-icon :size="24"><ChatDotRound /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.whatsappSent }}</div>
            <div class="stat-label">WhatsApp发送</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-icon">
            <el-icon :size="24"><SuccessFilled /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.replies }}</div>
            <div class="stat-label">客户回复</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="chart-row">
      <el-col :span="12">
        <div class="chart-card">
          <div class="card-header">客户等级分布</div>
          <div ref="gradeChartRef" class="chart-content"></div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="chart-card">
          <div class="card-header">客户来源分布</div>
          <div ref="sourceChartRef" class="chart-content"></div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="16">
      <el-col :span="24">
        <div class="chart-card">
          <div class="card-header">客户转化漏斗</div>
          <div ref="funnelChartRef" class="chart-content"></div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { getDashboardStats, getGradeDistribution, getSourceDistribution, getFunnelData } from '@/api/dashboard'

const stats = ref({
  totalCompanies: 0,
  emailsSent: 0,
  whatsappSent: 0,
  replies: 0
})

const gradeChartRef = ref(null)
const sourceChartRef = ref(null)
const funnelChartRef = ref(null)

let gradeChart = null
let sourceChart = null
let funnelChart = null

onMounted(async () => {
  await loadStats()
  initCharts()
  window.addEventListener('resize', handleResize)
})

function handleResize() {
  gradeChart?.resize()
  sourceChart?.resize()
  funnelChart?.resize()
}

async function loadStats() {
  try {
    const [statsRes, gradeRes, sourceRes, funnelRes] = await Promise.all([
      getDashboardStats(),
      getGradeDistribution(),
      getSourceDistribution(),
      getFunnelData()
    ])
    
    // 更新统计数据
    if (statsRes.data) {
      stats.value = {
        totalCompanies: statsRes.data.totalCompanies || 0,
        emailsSent: statsRes.data.emailsSent || 0,
        whatsappSent: statsRes.data.whatsappSent || 0,
        replies: statsRes.data.replies || 0
      }
    }
    
    // 更新图表数据
    if (gradeChart) {
      gradeChart.setOption({
        series: [{
          data: (gradeRes.data || []).map(item => ({
            value: item.count,
            name: item.leadGrade || '未分类'
          }))
        }]
      })
    }
    
    if (sourceChart) {
      sourceChart.setOption({
        xAxis: {
          data: (sourceRes.data || []).map(item => item.source || '未知')
        },
        series: [{
          data: (sourceRes.data || []).map(item => item.count)
        }]
      })
    }
    
    if (funnelChart) {
      funnelChart.setOption({
        series: [{
          data: (funnelRes.data || []).map(item => ({
            value: item.count,
            name: item.status || '未知'
          }))
        }]
      })
    }
  } catch (e) {
    console.error('Failed to load dashboard stats:', e)
  }
}

function initCharts() {
  // 客户等级饼图
  gradeChart = echarts.init(gradeChartRef.value)
  gradeChart.setOption({
    tooltip: { trigger: 'item', backgroundColor: '#fff', borderColor: '#e0f2ce', textStyle: { color: '#1e293b' } },
    legend: { bottom: '5%', textStyle: { color: '#64748b', fontSize: 12 } },
    series: [{
      name: '客户等级',
      type: 'pie',
      radius: ['45%', '70%'],
      data: [],
      itemStyle: { borderRadius: 4, borderColor: '#fff', borderWidth: 2 },
      label: { color: '#1e293b', fontSize: 11 },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  })

  // 客户来源柱状图
  sourceChart = echarts.init(sourceChartRef.value)
  sourceChart.setOption({
    tooltip: { trigger: 'axis', backgroundColor: '#fff', borderColor: '#e0f2ce', textStyle: { color: '#1e293b' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: [],
      axisLine: { lineStyle: { color: '#e2e8f0' } },
      axisLabel: { color: '#64748b', fontSize: 11 }
    },
    yAxis: { 
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#f1f5f9' } },
      axisLabel: { color: '#64748b', fontSize: 11 }
    },
    series: [{
      data: [],
      type: 'bar',
      itemStyle: { color: '#3b82f6', borderRadius: [4, 4, 0, 0] }
    }]
  })

  // 转化漏斗图
  funnelChart = echarts.init(funnelChartRef.value)
  funnelChart.setOption({
    tooltip: { trigger: 'item', backgroundColor: '#fff', borderColor: '#e0f2ce', textStyle: { color: '#1e293b' } },
    series: [{
      name: '转化漏斗',
      type: 'funnel',
      left: '15%',
      top: 30,
      bottom: 30,
      width: '70%',
      min: 0,
      max: 100,
      minSize: '0%',
      maxSize: '100%',
      sort: 'descending',
      gap: 1,
      label: { show: true, position: 'inside', color: '#fff', fontSize: 11 },
      itemStyle: { borderColor: '#fff', borderWidth: 1 },
      data: []
    }]
  })
}
</script>

<style scoped>
.dashboard {
  padding: 24px;
  background-color: #f8fafc;
  min-height: 100%;
}

.stats-row {
  margin-bottom: 24px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.stat-card:hover {
  border-color: #bfdbfe;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2563eb;
  background-color: #eff6ff;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #1e293b;
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
  margin-top: 4px;
}

.chart-row {
  margin-bottom: 24px;
}

.chart-card {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}

.card-header {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f1f5f9;
}

.chart-content {
  height: 280px;
}
</style>
