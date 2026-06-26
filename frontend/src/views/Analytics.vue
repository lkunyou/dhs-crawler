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
import { getEmailStats, getWhatsappStats, getSourceQuality, getTrend, getFunnel } from '@/api/analytics'

const emailStats = reactive({ openRate: 0, replyRate: 0, replied: 0, totalSent: 0, totalOpened: 0 })
const whatsappStats = reactive({ readRate: 0, replyRate: 0, replied: 0, totalSent: 0, totalRead: 0 })

const emailChartRef = ref(null)
const whatsappChartRef = ref(null)
const funnelChartRef = ref(null)
const trendChartRef = ref(null)

const sourceQuality = ref([])
const sourceQualityColumns = [
  { prop: 'source', label: '渠道', width: 120 },
  { prop: 'count', label: '客户数', width: 100 },
  { prop: 'highQuality', label: 'S/A级', width: 100 },
  { prop: 'qualityRate', label: '质量率', width: 150 }
]

let emailChart = null
let whatsappChart = null
let funnelChart = null
let trendChart = null

onMounted(async () => {
  await loadData()
  initCharts()
  window.addEventListener('resize', handleResize)
})

function handleResize() {
  emailChart?.resize()
  whatsappChart?.resize()
  funnelChart?.resize()
  trendChart?.resize()
}

async function loadData() {
  try {
    const [emailRes, whatsappRes, sourceRes, funnelRes, trendRes] = await Promise.all([
      getEmailStats(),
      getWhatsappStats(),
      getSourceQuality(),
      getFunnel(),
      getTrend(30)
    ])
    
    // 更新邮件统计
    if (emailRes.data) {
      Object.assign(emailStats, emailRes.data)
    }
    
    // 更新WhatsApp统计
    if (whatsappRes.data) {
      Object.assign(whatsappStats, whatsappRes.data)
    }
    
    // 更新渠道质量
    if (sourceRes.data) {
      sourceQuality.value = sourceRes.data.map(item => ({
        source: item.source || '未知',
        count: item.count,
        highQuality: item.highQuality || 0,
        qualityRate: item.qualityRate || 0
      }))
    }
    
    // 更新图表数据
    if (emailChart) {
      emailChart.setOption({
        series: [{
          data: [
            emailRes.data?.totalSent || 0,
            emailRes.data?.totalOpened || 0,
            emailRes.data?.totalOpened || 0,
            emailRes.data?.totalReplied || 0
          ]
        }]
      })
    }
    
    if (whatsappChart) {
      whatsappChart.setOption({
        series: [{
          data: [
            whatsappRes.data?.totalSent || 0,
            whatsappRes.data?.totalSent || 0,
            whatsappRes.data?.totalRead || 0,
            whatsappRes.data?.totalReplied || 0
          ]
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
    
    if (trendChart && trendRes.data) {
      trendChart.setOption({
        xAxis: {
          data: trendRes.data.map(item => item.date)
        },
        series: [
          { data: trendRes.data.map(item => item.newCompanies) },
          { data: trendRes.data.map(item => item.emailsSent) },
          { data: trendRes.data.map(item => item.replies) }
        ]
      })
    }
  } catch (e) {
    console.error('Failed to load analytics data:', e)
  }
}

function initCharts() {
  // 邮件效果柱状图
  emailChart = echarts.init(emailChartRef.value)
  emailChart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['发送', '送达', '打开', '回复'] },
    yAxis: { type: 'value' },
    series: [{ data: [], type: 'bar', itemStyle: { color: '#409EFF' } }]
  })

  // WhatsApp效果
  whatsappChart = echarts.init(whatsappChartRef.value)
  whatsappChart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['发送', '送达', '已读', '回复'] },
    yAxis: { type: 'value' },
    series: [{ data: [], type: 'bar', itemStyle: { color: '#67C23A' } }]
  })

  // 转化漏斗
  funnelChart = echarts.init(funnelChartRef.value)
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
      data: []
    }]
  })

  // 30天趋势
  trendChart = echarts.init(trendChartRef.value)
  trendChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['新增客户', '邮件发送', '客户回复'] },
    xAxis: { type: 'category', data: [] },
    yAxis: { type: 'value' },
    series: [
      { name: '新增客户', type: 'line', data: [], smooth: true },
      { name: '邮件发送', type: 'line', data: [], smooth: true },
      { name: '客户回复', type: 'line', data: [], smooth: true }
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
