<template>
  <div class="dashboard">
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background: #409EFF">
              <el-icon :size="30"><UserFilled /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.totalCompanies }}</div>
              <div class="stat-label">总客户数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background: #67C23A">
              <el-icon :size="30"><Message /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.emailsSent }}</div>
              <div class="stat-label">邮件已发送</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background: #E6A23C">
              <el-icon :size="30"><ChatDotRound /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.whatsappSent }}</div>
              <div class="stat-label">WhatsApp发送</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-icon" style="background: #F56C6C">
              <el-icon :size="30"><SuccessFilled /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.replies }}</div>
              <div class="stat-label">客户回复</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="chart-row">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>客户等级分布</span>
            </div>
          </template>
          <div ref="gradeChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>客户来源分布</span>
            </div>
          </template>
          <div ref="sourceChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>客户转化漏斗</span>
            </div>
          </template>
          <div ref="funnelChartRef" style="height: 300px"></div>
        </el-card>
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
    tooltip: { trigger: 'item' },
    legend: { bottom: '5%' },
    series: [{
      name: '客户等级',
      type: 'pie',
      radius: ['40%', '70%'],
      data: [
        { value: 15, name: 'S级 - 必须开发', itemStyle: { color: '#F56C6C' } },
        { value: 35, name: 'A级 - 重点跟进', itemStyle: { color: '#E6A23C' } },
        { value: 80, name: 'B级 - 自动培育', itemStyle: { color: '#409EFF' } },
        { value: 120, name: 'C级 - 丢弃', itemStyle: { color: '#909399' } }
      ]
    }]
  })

  // 客户来源柱状图
  const sourceChart = echarts.init(sourceChartRef.value)
  sourceChart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: ['Google', 'LinkedIn', 'B2B平台', '行业目录', '手动录入']
    },
    yAxis: { type: 'value' },
    series: [{
      data: [120, 85, 45, 30, 20],
      type: 'bar',
      itemStyle: { color: '#409EFF' }
    }]
  })

  // 转化漏斗图
  const funnelChart = echarts.init(funnelChartRef.value)
  funnelChart.setOption({
    tooltip: { trigger: 'item' },
    series: [{
      name: '转化漏斗',
      type: 'funnel',
      left: '10%',
      top: 20,
      bottom: 20,
      width: '80%',
      min: 0,
      max: 500,
      minSize: '0%',
      maxSize: '100%',
      sort: 'descending',
      gap: 2,
      label: { show: true, position: 'inside' },
      data: [
        { value: 500, name: 'New Lead' },
        { value: 350, name: 'Contacted' },
        { value: 120, name: 'Replied' },
        { value: 45, name: 'Quoted' },
        { value: 20, name: 'Negotiation' },
        { value: 8, name: 'Won' }
      ]
    }]
  })
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}
</style>
