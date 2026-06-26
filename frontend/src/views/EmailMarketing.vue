<template>
  <div class="email-marketing">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>邮件营销活动</span>
          <el-button type="primary" size="small" @click="createCampaign">新建营销活动</el-button>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-card>
            <template #header>营销活动列表</template>
            <el-table :data="campaigns" border>
              <el-table-column prop="name" label="活动名称" min-width="200" />
              <el-table-column prop="status" label="状态" width="120">
                <template #default="{ row }">
                  <el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="totalEmails" label="邮件总数" width="100" />
              <el-table-column prop="sentCount" label="已发送" width="100" />
              <el-table-column prop="openRate" label="打开率" width="100">
                <template #default="{ row }">
                  {{ row.openRate ? (row.openRate * 100).toFixed(1) + '%' : '-' }}
                </template>
              </el-table-column>
              <el-table-column prop="createTime" label="创建时间" width="180" />
              <el-table-column label="操作" width="180">
                <template #default="{ row }">
                  <el-button size="small" @click="viewCampaign(row)">查看</el-button>
                  <el-button size="small" type="warning" @click="startCampaign(row)" v-if="row.status === 'draft'">启动</el-button>
                  <el-button size="small" type="danger" @click="deleteCampaign(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>

        <el-col :span="12">
          <el-card>
            <template #header>营销统计</template>
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-value">{{ totalCampaigns }}</div>
                <div class="stat-label">总活动数</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ totalSent }}</div>
                <div class="stat-label">总发送量</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ avgOpenRate }}</div>
                <div class="stat-label">平均打开率</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ activeCampaigns }}</div>
                <div class="stat-label">进行中</div>
              </div>
            </div>
          </el-card>

          <el-card style="margin-top: 20px">
            <template #header>最近发送记录</template>
            <el-timeline>
              <el-timeline-item 
                v-for="record in recentRecords" 
                :key="record.id" 
                :timestamp="record.sentAt" 
                placement="top"
              >
                <el-card size="small">
                  <h4>{{ record.subject }}</h4>
                  <p>{{ record.recipientEmail }}</p>
                  <el-tag :type="getStatusType(record.status)" size="small">{{ getStatusLabel(record.status) }}</el-tag>
                </el-card>
              </el-timeline-item>
            </el-timeline>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const campaigns = ref([
  { id: 1, name: '2026年6月产品推广', status: 'active', totalEmails: 500, sentCount: 320, openRate: 0.28, createTime: '2026-06-01 10:30' },
  { id: 2, name: 'OEM合作伙伴招募', status: 'completed', totalEmails: 200, sentCount: 200, openRate: 0.35, createTime: '2026-05-15 09:00' },
  { id: 3, name: '新品发布通知', status: 'draft', totalEmails: 800, sentCount: 0, openRate: null, createTime: '2026-06-20 14:00' }
])

const recentRecords = ref([
  { id: 1, subject: 'Hot Selling Auto Parts', recipientEmail: 'contact@company.com', status: 'Opened', sentAt: '10分钟前' },
  { id: 2, subject: 'OEM Partnership', recipientEmail: 'sales@factory.co.th', status: 'Sent', sentAt: '25分钟前' },
  { id: 3, subject: 'Exclusive Price List', recipientEmail: 'info@autoparts.co', status: 'Delivered', sentAt: '1小时前' }
])

const totalCampaigns = ref(3)
const totalSent = ref(520)
const avgOpenRate = ref('31.5%')
const activeCampaigns = ref(1)

onMounted(() => {
  loadCampaigns()
})

async function loadCampaigns() {
  campaigns.value = campaigns.value
}

function createCampaign() {
  ElMessage.info('新建营销活动功能开发中')
}

function viewCampaign(row) {
  ElMessage.info(`查看活动: ${row.name}`)
}

function startCampaign(row) {
  row.status = 'active'
  ElMessage.success(`已启动活动: ${row.name}`)
}

function deleteCampaign(row) {
  campaigns.value = campaigns.value.filter(c => c.id !== row.id)
  ElMessage.success(`已删除活动: ${row.name}`)
}

function getStatusType(status) {
  const types = { draft: 'info', active: '', completed: 'success', paused: 'warning' }
  return types[status] || ''
}

function getStatusLabel(status) {
  const labels = { draft: '草稿', active: '进行中', completed: '已完成', paused: '已暂停' }
  return labels[status] || status
}
</script>

<style scoped>
.email-marketing {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.stat-item {
  background: linear-gradient(135deg, #eff6ff 0%, #f8fafc 100%);
  padding: 16px;
  border-radius: 8px;
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #2563eb;
}

.stat-label {
  font-size: 12px;
  color: #64748b;
  margin-top: 4px;
}
</style>