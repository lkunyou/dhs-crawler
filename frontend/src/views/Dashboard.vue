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
import { getGradeStats, getSourceStats, getStatusStats } from '@/api/company'

const stats = ref({
  totalCompanies: 0,
  emailsSent: 0,
  whatsappSent: 0,
  replies: 0
})

const gradeChartRef = ref(null)
const sourceChartRef = ref(null)
const funnelChartRef = ref(null)

onMounted(async () => {
  await loadStats()
  initCharts()
})

async function loadStats() {
  try {
    const [gradeRes, sourceRes, statusRes] = await Promise.all([
      getGradeStats(),
      getSourceStats(),
      getStatusStats()
    ])
    
    // 计算总数
    stats.value.totalCompanies = gradeRes.data.reduce((sum, item) => sum + item.count, 0)
  } catch (e) {
    console.error('Failed to load stats:', e)
  }
}

function initCharts() {
  // 客户等级饼图
  const gradeChart = echarts.init(gradeChartRef.value)
  gradeChart.setOption({
    tooltip: { trigger: 'item', backgroundColor: '#fff', borderColor: '#e0f2fe', textStyle: { color: '#1e293b' } },
    legend: { bottom: '5%', textStyle: { color: '#64748b', fontSize: 12 } },
    series: [{
      name: '客户等级',
      type: 'pie',
      radius: ['45%', '70%'],
      data: [
        { value: 15, name: 'S级 - 必须开发', itemStyle: { color: '#2563eb' } },
        { value: 35, name: 'A级 - 重点跟进', itemStyle: { color: '#3b82f6' } },
        { value: 80, name: 'B级 - 自动培育', itemStyle: { color: '#60a5fa' } },
        { value: 120, name: 'C级 - 丢弃', itemStyle: { color: '#bfdbfe' } }
      ],
      label: { color: '#1e293b', fontSize: 11 }
    }]
  })

  // 客户来源柱状图
  const sourceChart = echarts.init(sourceChartRef.value)
  sourceChart.setOption({
    tooltip: { trigger: 'axis', backgroundColor: '#fff', borderColor: '#e0f2fe', textStyle: { color: '#1e293b' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: ['Google', 'LinkedIn', 'B2B平台', '行业目录', '手动录入'],
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
      data: [120, 85, 45, 30, 20],
      type: 'bar',
      itemStyle: { color: '#3b82f6', borderRadius: [4, 4, 0, 0] }
    }]
  })

  // 转化漏斗图
  const funnelChart = echarts.init(funnelChartRef.value)
  funnelChart.setOption({
    tooltip: { trigger: 'item', backgroundColor: '#fff', borderColor: '#e0f2fe', textStyle: { color: '#1e293b' } },
    series: [{
      name: '转化漏斗',
      type: 'funnel',
      left: '15%',
      top: 30,
      bottom: 30,
      width: '70%',
      min: 0,
      max: 500,
      minSize: '0%',
      maxSize: '100%',
      sort: 'descending',
      gap: 1,
      label: { show: true, position: 'inside', color: '#fff', fontSize: 11 },
      itemStyle: { borderColor: '#fff', borderWidth: 1 },
      data: [
        { value: 500, name: '新线索', itemStyle: { color: '#1d4ed8' } },
        { value: 350, name: '已联系', itemStyle: { color: '#2563eb' } },
        { value: 120, name: '已回复', itemStyle: { color: '#3b82f6' } },
        { value: 45, name: '已报价', itemStyle: { color: '#60a5fa' } },
        { value: 20, name: '洽谈中', itemStyle: { color: '#93c5fd' } },
        { value: 8, name: '已成交', itemStyle: { color: '#bfdbfe' } }
      ]
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
