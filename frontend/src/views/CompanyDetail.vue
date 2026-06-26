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
          <el-form v-if="editMode" :model="company" label-width="120px" style="padding: 20px;">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="公司名称" required>
                  <el-input v-model="company.companyName" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="公司类型">
                  <el-select v-model="company.companyType" style="width: 100%">
                    <el-option label="批发商" value="Distributor" />
                    <el-option label="进口商" value="Importer" />
                    <el-option label="零售商" value="Retailer" />
                    <el-option label="维修厂" value="Repair_Shop" />
                    <el-option label="制造商" value="Manufacturer" />
                    <el-option label="经销商" value="Dealer" />
                    <el-option label="其他" value="Other" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="官网">
                  <el-input v-model="company.website" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="来源">
                  <el-select v-model="company.source" style="width: 100%">
                    <el-option label="Google" value="Google" />
                    <el-option label="LinkedIn" value="LinkedIn" />
                    <el-option label="B2B平台" value="B2B_Platform" />
                    <el-option label="行业目录" value="Industry_Directory" />
                    <el-option label="手动添加" value="Manual" />
                    <el-option label="API导入" value="API" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="地址">
              <el-input v-model="company.address" />
            </el-form-item>
            <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="城市">
                  <el-input v-model="company.city" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="省份">
                  <el-input v-model="company.province" />
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="国家">
                  <el-input v-model="company.country" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="电话">
                  <el-input v-model="company.phone" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="WhatsApp">
                  <el-input v-model="company.whatsapp" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="邮箱">
              <el-input v-model="company.email" />
            </el-form-item>
            <el-form-item label="员工规模">
              <el-input v-model="company.employeeCount" placeholder="例如: 1-10, 11-50" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveCompany">保存</el-button>
              <el-button @click="cancelEdit">取消</el-button>
            </el-form-item>
          </el-form>
          
          <el-descriptions v-else :column="2" border>
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
          <el-timeline v-if="followUpRecords.length > 0">
            <el-timeline-item
              v-for="record in followUpRecords"
              :key="record.id"
              :timestamp="record.createdAt"
              placement="top"
            >
              <el-card>
                <h4>{{ record.summary || record.followUpType + ' - ' + record.outcome }}</h4>
                <p style="color: #666; font-size: 13px; margin: 6px 0;">{{ record.detail || '' }}</p>
                <div style="display: flex; gap: 8px; align-items: center; margin-top: 8px;">
                  <el-tag size="small" :type="record.outcome === 'Sent' ? 'success' : record.outcome === 'Failed' ? 'danger' : 'info'">{{ record.outcome }}</el-tag>
                  <el-tag size="small" type="primary">{{ record.followUpType }}</el-tag>
                  <span v-if="record.createdBy" style="font-size: 12px; color: #999;">操作员: {{ record.createdBy }}</span>
                </div>
              </el-card>
            </el-timeline-item>
          </el-timeline>
          <el-empty v-else description="暂无跟进记录" />
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
          <el-button type="primary" style="width: 100%; margin-bottom: 10px" @click="handleSendEmail">
            <el-icon><Message /></el-icon> 发送邮件
          </el-button>
          <el-button type="success" style="width: 100%; margin-bottom: 10px" @click="handleSendWhatsApp">
            <el-icon><ChatDotRound /></el-icon> 发送WhatsApp
          </el-button>
          <el-button type="warning" style="width: 100%; margin-bottom: 10px" @click="quoteDialogVisible = true">
            <el-icon><Document /></el-icon> 创建报价
          </el-button>
          <el-button style="width: 100%" @click="followupDialogVisible = true">
            <el-icon><Edit /></el-icon> 添加跟进记录
          </el-button>
        </el-card>

        <el-card style="margin-top: 20px">
          <template #header>客户状态</template>
          <el-select v-model="company.status" style="width: 100%" @change="handleStatusChange">
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

    <!-- 创建报价弹窗 -->
    <el-dialog v-model="quoteDialogVisible" title="创建报价单" width="600px">
      <el-form :model="quoteForm" label-width="100px">
        <el-form-item label="客户名称">
          <el-input v-model="company.companyName" disabled />
        </el-form-item>
        <el-form-item label="报价编号">
          <el-input v-model="quoteForm.quoteNo" placeholder="自动生成" disabled />
        </el-form-item>
        <el-form-item label="产品名称" required>
          <el-input v-model="quoteForm.productName" placeholder="请输入产品名称" />
        </el-form-item>
        <el-form-item label="产品型号">
          <el-input v-model="quoteForm.productModel" placeholder="请输入产品型号" />
        </el-form-item>
        <el-form-item label="数量" required>
          <el-input-number v-model="quoteForm.quantity" :min="1" style="width: 100%" />
        </el-form-item>
        <el-form-item label="单价(USD)" required>
          <el-input-number v-model="quoteForm.unitPrice" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        <el-form-item label="总金额">
          <el-input :model-value="quoteTotal" disabled style="width: 100%">
            <template #prefix>USD</template>
          </el-input>
        </el-form-item>
        <el-form-item label="有效期">
          <el-date-picker v-model="quoteForm.validDate" type="date" placeholder="选择有效期" style="width: 100%" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="quoteForm.remark" type="textarea" :rows="3" placeholder="请输入备注" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="quoteDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveQuote">保存报价</el-button>
      </template>
    </el-dialog>

    <!-- 添加跟进记录弹窗 -->
    <el-dialog v-model="followupDialogVisible" title="添加跟进记录" width="500px">
      <el-form :model="followupForm" label-width="100px">
        <el-form-item label="跟进方式" required>
          <el-select v-model="followupForm.type" placeholder="选择跟进方式" style="width: 100%">
            <el-option label="电话" value="phone" />
            <el-option label="邮件" value="email" />
            <el-option label="WhatsApp" value="whatsapp" />
            <el-option label="面谈" value="meeting" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="跟进结果" required>
          <el-select v-model="followupForm.result" placeholder="选择跟进结果" style="width: 100%">
            <el-option label="已联系" value="contacted" />
            <el-option label="有意向" value="interested" />
            <el-option label="已报价" value="quoted" />
            <el-option label="已下单" value="ordered" />
            <el-option label="无回复" value="no_reply" />
            <el-option label="已拒绝" value="rejected" />
          </el-select>
        </el-form-item>
        <el-form-item label="跟进内容" required>
          <el-input v-model="followupForm.content" type="textarea" :rows="4" placeholder="请输入跟进内容" />
        </el-form-item>
        <el-form-item label="下次跟进">
          <el-date-picker v-model="followupForm.nextFollowDate" type="datetime" placeholder="选择下次跟进时间" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="followupDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveFollowup">保存记录</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Message, ChatDotRound, Document, Edit } from '@element-plus/icons-vue'
import { getCompany, updateCompany } from '@/api/company'
import { getFollowUpRecords, addFollowUpRecord } from '@/api/followUp'
import { BaseTable } from '@/components'

const route = useRoute()
const router = useRouter()
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
  companyNameTh: '',
  companyNameEn: '',
  country: '',
  companyType: '',
  website: '',
  address: '',
  city: '',
  province: '',
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

const originalCompany = ref({})
const followUpRecords = ref([])

onMounted(async () => {
  const id = route.params.id
  if (id) {
    loading.value = true
    try {
      const res = await getCompany(id)
      Object.assign(company, res.data)
      if (!company.contacts) company.contacts = []
      originalCompany.value = JSON.parse(JSON.stringify(res.data))
      await loadFollowUpRecords(id)
    } catch (e) {
      console.error(e)
    } finally {
      loading.value = false
    }
  }
})

async function loadFollowUpRecords(companyId) {
  try {
    const res = await getFollowUpRecords(companyId)
    followUpRecords.value = res.data || []
  } catch (e) {
    followUpRecords.value = []
  }
}

async function saveCompany() {
  if (!company.companyName) {
    ElMessage.warning('请输入公司名称')
    return
  }
  
  loading.value = true
  try {
    await updateCompany(company.id, company)
    ElMessage.success('保存成功')
    editMode.value = false
    originalCompany.value = JSON.parse(JSON.stringify(company))
  } catch (e) {
    ElMessage.error('保存失败')
    console.error(e)
  } finally {
    loading.value = false
  }
}

function cancelEdit() {
  Object.assign(company, originalCompany.value)
  editMode.value = false
}

// 发送邮件
function handleSendEmail() {
  if (!company.email) {
    ElMessage.warning('该客户没有邮箱地址')
    return
  }
  router.push({ path: '/email-campaign', query: { companyId: company.id } })
}

// 发送WhatsApp
function handleSendWhatsApp() {
  if (!company.whatsapp) {
    ElMessage.warning('该客户没有WhatsApp号码')
    return
  }
  const phone = company.whatsapp.replace(/\D/g, '')
  window.open(`https://web.whatsapp.com/send?phone=${phone}`, '_blank')
}

// 报价弹窗
const quoteDialogVisible = ref(false)
const quoteForm = reactive({
  quoteNo: '',
  productName: '',
  productModel: '',
  quantity: 1,
  unitPrice: 0,
  validDate: null,
  remark: ''
})

const quoteTotal = computed(() => {
  return (quoteForm.quantity * quoteForm.unitPrice).toFixed(2)
})

function saveQuote() {
  if (!quoteForm.productName) {
    ElMessage.warning('请输入产品名称')
    return
  }
  if (!quoteForm.quantity || quoteForm.quantity < 1) {
    ElMessage.warning('请输入有效数量')
    return
  }
  if (!quoteForm.unitPrice || quoteForm.unitPrice < 0) {
    ElMessage.warning('请输入有效单价')
    return
  }
  
  // 模拟保存报价
  ElMessage.success(`报价单已创建，总金额: USD ${quoteTotal}`)
  quoteDialogVisible.value = false
  
  // 重置表单
  quoteForm.productName = ''
  quoteForm.productModel = ''
  quoteForm.quantity = 1
  quoteForm.unitPrice = 0
  quoteForm.validDate = null
  quoteForm.remark = ''
}

// 跟进记录弹窗
const followupDialogVisible = ref(false)
const followupForm = reactive({
  type: '',
  result: '',
  content: '',
  nextFollowDate: null
})

async function saveFollowup() {
  if (!followupForm.type) {
    ElMessage.warning('请选择跟进方式')
    return
  }
  if (!followupForm.result) {
    ElMessage.warning('请选择跟进结果')
    return
  }
  if (!followupForm.content) {
    ElMessage.warning('请输入跟进内容')
    return
  }

  try {
    await addFollowUpRecord({
      companyId: company.id,
      followUpType: followupForm.type,
      outcome: followupForm.result,
      summary: followupForm.type + ' - ' + followupForm.result,
      detail: followupForm.content,
      nextActionDate: followupForm.nextFollowDate
    })
    ElMessage.success('跟进记录已保存')
    followupDialogVisible.value = false
    await loadFollowUpRecords(company.id)

    // 重置表单
    followupForm.type = ''
    followupForm.result = ''
    followupForm.content = ''
    followupForm.nextFollowDate = null
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

// 客户状态变更
async function handleStatusChange(status) {
  try {
    await updateCompany(company.id, { status })
    ElMessage.success('状态已更新')
  } catch (e) {
    ElMessage.error('状态更新失败')
    console.error(e)
  }
}
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
