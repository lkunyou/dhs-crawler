<template>
  <div class="analytics-page">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header><span>邮件营销效果</span></template>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="metric">
                <div class="metric-value">{{ emailStats.openRate }}%</div>
                <div class="metric-label">打开率</div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="metric">
                <div class="metric-value">{{ emailStats.replyRate }}%</div>
                <div class="metric-label">回复率</div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="metric">
                <div class="metric-value">{{ emailStats.replied }}</div>
                <div class="metric-label">回复数</div>
              </div>
            </el-col>
          </el-row>
          <div ref="emailChartRef" style="height: 250px; margin-top: 20px"></div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card>
          <template #header><span>WhatsApp效果</span></template>
          <el-row :gutter="20">
            <el-col :span="8">
              <div class="metric">
                <div class="metric-value">{{ whatsappStats.readRate }}%</div>
                <div class="metric-label">已读率</div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="metric">
                <div class="metric-value">{{ whatsappStats.replyRate }}%</div>
                <div class="metric-label">回复率</div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="metric">
                <div class="metric-value">{{ whatsappStats.replied }}</div>
                <div class="metric-label">回复数</div>
              </div>
            </el-col>
          </el-row>
          <div ref="whatsappChartRef" style="height: 250px; margin-top: 20px"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header><span>转化漏斗</span></template>
          <div ref="funnelChartRef" style="height: 350px"></div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card>
          <template #header><span>渠道质量分析</span></template>
          <BaseTable :data="sourceQuality" :columns="sourceQualityColumns" :show-pagination="false" />
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <template #header><span>30天趋势</span></template>
          <div ref="trendChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import * as echarts from 'echarts'
import { BaseTable } from '@/components'

const emailStats = reactive({ openRate: 35.2, replyRate: 8.5, replied: 42 })
const whatsappStats = reactive({ readRate: 72.3, replyRate: 25.6, replied: 68 })

const emailChartRef = ref(null)
const whatsappChartRef = ref(null)
const funnelChartRef = ref(null)
const trendChartRef = ref(null)

const sourceQuality = ref([
  { source: 'Google', total: 250, highQuality: 45, qualityRate: '18.00' },
  { source: 'LinkedIn', total: 120, highQuality: 38, qualityRate: '31.67' },
  { source: 'B2B平台', total: 80, highQuality: 15, qualityRate: '18.75' },
  { source: '行业目录', total: 50, highQuality: 12, qualityRate: '24.00' }
])

const sourceQualityColumns = [
  { prop: 'source', label: '渠道', width: 120 },
  { prop: 'total', label: '客户数', width: 100 },
  { prop: 'highQuality', label: 'S/A级', width: 100 },
  { prop: 'qualityRate', label: '质量率', width: 150 }
]

onMounted(() => {
  initCharts()
})

function initCharts() {
  // 邮件效果柱状图
  const emailChart = echarts.init(emailChartRef.value)
  emailChart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['发送', '送达', '打开', '回复'] },
    yAxis: { type: 'value' },
    series: [{ data: [500, 485, 176, 42], type: 'bar', itemStyle: { color: '#409EFF' } }]
  })

  // WhatsApp效果
  const waChart = echarts.init(whatsappChartRef.value)
  waChart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['发送', '送达', '已读', '回复'] },
    yAxis: { type: 'value' },
    series: [{ data: [265, 258, 186, 68], type: 'bar', itemStyle: { color: '#67C23A' } }]
  })

  // 转化漏斗
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

  // 30天趋势
  const trendChart = echarts.init(trendChartRef.value)
  const dates = Array.from({ length: 30 }, (_, i) => {
    const d = new Date();
    d.setDate(d.getDate() - 29 + i);
    return `${d.getMonth() + 1}/${d.getDate()}`;
  })
  trendChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['新增客户', '邮件发送', '客户回复'] },
    xAxis: { type: 'category', data: dates },
    yAxis: { type: 'value' },
    series: [
      { name: '新增客户', type: 'line', data: Array.from({ length: 30 }, () => Math.floor(Math.random() * 20 + 5)), smooth: true },
      { name: '邮件发送', type: 'line', data: Array.from({ length: 30 }, () => Math.floor(Math.random() * 30 + 10)), smooth: true },
      { name: '客户回复', type: 'line', data: Array.from({ length: 30 }, () => Math.floor(Math.random() * 5 + 1)), smooth: true }
    ]
  })
}
</script>

<style scoped>
.analytics-page { padding: 20px; }
.metric { text-align: center; padding: 10px; }
.metric-value { font-size: 28px; font-weight: bold; color: #303133; }
.metric-label { font-size: 14px; color: #909399; margin-top: 5px; }
</style>
