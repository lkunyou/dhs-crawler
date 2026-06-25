<template>
  <div class="company-detail" v-loading="loading">
    <el-page-header @back="$router.back()" content="客户详情" style="margin-bottom: 20px" />
    
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>基本信息</span>
              <el-button type="primary" size="small" @click="editMode = !editMode">
                {{ editMode ? '保存' : '编辑' }}
              </el-button>
            </div>
          </template>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="公司名称">{{ company.companyName }}</el-descriptions-item>
            <el-descriptions-item label="公司类型">{{ company.companyType }}</el-descriptions-item>
            <el-descriptions-item label="官网">
              <el-link v-if="company.website" :href="company.website" target="_blank">{{ company.website }}</el-link>
            </el-descriptions-item>
            <el-descriptions-item label="来源">{{ company.source }}</el-descriptions-item>
            <el-descriptions-item label="地址">{{ company.address }}</el-descriptions-item>
            <el-descriptions-item label="城市">{{ company.city }}</el-descriptions-item>
            <el-descriptions-item label="电话">{{ company.phone }}</el-descriptions-item>
            <el-descriptions-item label="WhatsApp">{{ company.whatsapp }}</el-descriptions-item>
            <el-descriptions-item label="邮箱">{{ company.email }}</el-descriptions-item>
            <el-descriptions-item label="员工规模">{{ company.employeeCount }}</el-descriptions-item>
          </el-descriptions>
        </el-card>

        <el-card style="margin-top: 20px">
          <template #header>
            <div class="card-header">
              <span>联系人</span>
              <el-button type="primary" size="small">添加联系人</el-button>
            </div>
          </template>
          <BaseTable :data="company.contacts || []" :columns="contactColumns" :show-pagination="false" />
        </el-card>

        <el-card style="margin-top: 20px">
          <template #header>跟进记录</template>
          <el-timeline>
            <el-timeline-item timestamp="2024-01-15 10:00" placement="top">
              <el-card>
                <h4>发送开发信 - Day1</h4>
                <p>邮件主题: Professional Auto Parts Manufacturer from China</p>
                <el-tag size="small" type="success">已发送</el-tag>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card>
          <template #header>客户评分</template>
          <div class="score-display">
            <div class="score-circle">
              <span class="score-number">{{ company.leadScore || 0 }}</span>
              <span class="score-grade">{{ company.leadGrade || 'C' }}</span>
            </div>
          </div>
        </el-card>

        <el-card style="margin-top: 20px">
          <template #header>快捷操作</template>
          <el-button type="primary" style="width: 100%; margin-bottom: 10px">
            <el-icon><Message /></el-icon> 发送邮件
          </el-button>
          <el-button type="success" style="width: 100%; margin-bottom: 10px">
            <el-icon><ChatDotRound /></el-icon> 发送WhatsApp
          </el-button>
          <el-button type="warning" style="width: 100%; margin-bottom: 10px">
            <el-icon><Document /></el-icon> 创建报价
          </el-button>
          <el-button style="width: 100%">
            <el-icon><Edit /></el-icon> 添加跟进记录
          </el-button>
        </el-card>

        <el-card style="margin-top: 20px">
          <template #header>客户状态</template>
          <el-select v-model="company.status" style="width: 100%">
            <el-option label="New - 新客户" value="New" />
            <el-option label="Contacted - 已联系" value="Contacted" />
            <el-option label="Replied - 有回复" value="Replied" />
            <el-option label="Quoted - 已报价" value="Quoted" />
            <el-option label="Negotiation - 谈判中" value="Negotiation" />
            <el-option label="Sample Sent - 已打样" value="Sample_Sent" />
            <el-option label="Won - 已成交" value="Won" />
            <el-option label="Lost - 已流失" value="Lost" />
          </el-select>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getCompany } from '@/api/company'
import { BaseTable } from '@/components'

const route = useRoute()
const loading = ref(false)
const editMode = ref(false)

const contactColumns = [
  { prop: 'fullName', label: '姓名', width: 150 },
  { prop: 'jobTitle', label: '职位', width: 150 },
  { prop: 'email', label: '邮箱', width: 200 },
  { prop: 'whatsapp', label: 'WhatsApp', width: 150 },
  { prop: 'linkedinUrl', label: 'LinkedIn', width: 200, type: 'link' },
  { label: '操作', width: 100, fixed: 'right', type: 'button', buttons: [
    { label: '发邮件', type: 'primary', size: 'small', handler: () => {} }
  ]}
]

const company = reactive({
  id: null,
  companyName: '',
  companyType: '',
  website: '',
  address: '',
  city: '',
  phone: '',
  whatsapp: '',
  email: '',
  employeeCount: '',
  source: '',
  leadScore: 0,
  leadGrade: 'C',
  status: 'New',
  contacts: []
})

onMounted(async () => {
  const id = route.params.id
  if (id) {
    loading.value = true
    try {
      const res = await getCompany(id)
      Object.assign(company, res.data)
      if (!company.contacts) company.contacts = []
    } catch (e) {
      console.error(e)
    } finally {
      loading.value = false
    }
  }
})
</script>

<style scoped>
.company-detail {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.score-display {
  display: flex;
  justify-content: center;
  padding: 20px;
}

.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: linear-gradient(135deg, #409EFF, #67C23A);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.score-number {
  font-size: 36px;
  font-weight: bold;
}

.score-grade {
  font-size: 24px;
  margin-top: 5px;
}
</style>
