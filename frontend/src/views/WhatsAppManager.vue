<template>
  <div class="whatsapp-manager">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>WhatsApp 自动开发</span>
          <el-button type="primary" @click="showSendDialog = true">
            <el-icon><ChatDotRound /></el-icon> 发送消息
          </el-button>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="8">
          <el-card>
            <template #header><span>快捷话术模板</span></template>
            <el-collapse v-model="activeTemplate">
              <el-collapse-item title="第一条：公司介绍" name="1">
                <div class="template-content">
                  <p>Sawadee ka! 🙏</p>
                  <p>I'm [Name] from [Company], a professional auto parts manufacturer in China.</p>
                  <p>We specialize in:</p>
                  <ul>
                    <li>Mirror Covers (Toyota/Isuzu)</li>
                    <li>Front Grilles</li>
                    <li>Bumper Assemblies</li>
                  </ul>
                  <p>Can I send you our catalog?</p>
                </div>
                <el-button size="small" type="primary" @click="useTemplate(1)">使用此模板</el-button>
              </el-collapse-item>
              <el-collapse-item title="第二条：产品图片" name="2">
                <div class="template-content">
                  <p>Here are our best-selling products for Thai market:</p>
                  <p>[发送产品图片]</p>
                  <p>These are very popular among Thai distributors. High quality with competitive price!</p>
                </div>
                <el-button size="small" type="primary" @click="useTemplate(2)">使用此模板</el-button>
              </el-collapse-item>
              <el-collapse-item title="第三条：问需求" name="3">
                <div class="template-content">
                  <p>May I know what products you are currently sourcing?</p>
                  <p>We can provide:</p>
                  <ul>
                    <li>Free samples</li>
                    <li>Competitive pricing</li>
                    <li>Fast delivery (15-20 days)</li>
                  </ul>
                </div>
                <el-button size="small" type="primary" @click="useTemplate(3)">使用此模板</el-button>
              </el-collapse-item>
              <el-collapse-item title="第四条：报价引导" name="4">
                <div class="template-content">
                  <p>We have a special promotion this month:</p>
                  <ul>
                    <li>10% discount on first order</li>
                    <li>Free samples (freight collect)</li>
                    <li>MOQ from 50 pcs</li>
                  </ul>
                  <p>Would you like me to prepare a quotation for you?</p>
                </div>
                <el-button size="small" type="primary" @click="useTemplate(4)">使用此模板</el-button>
              </el-collapse-item>
            </el-collapse>
          </el-card>
        </el-col>

        <el-col :span="16">
          <el-card>
            <template #header><span>发送记录</span></template>
            <el-table :data="messageRecords" style="width: 100%">
              <el-table-column prop="phoneNumber" label="号码" width="150" />
              <el-table-column prop="content" label="内容" min-width="200" show-overflow-tooltip />
              <el-table-column prop="status" label="状态" width="100">
                <template #default="{ row }">
                  <el-tag :type="getStatusType(row.status)" size="small">{{ getStatusLabel(row.status) }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="sentAt" label="发送时间" width="180">
                <template #default="{ row }">
                  {{ formatDateTime(row.sentAt) }}
                </template>
              </el-table-column>
              <el-table-column prop="readAt" label="已读时间" width="180">
                <template #default="{ row }">
                  {{ formatDateTime(row.readAt) }}
                </template>
              </el-table-column>
              <el-table-column prop="repliedAt" label="回复时间" width="180">
                <template #default="{ row }">
                  {{ formatDateTime(row.repliedAt) }}
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
    </el-card>

    <!-- 发送对话框 -->
    <el-dialog v-model="showSendDialog" title="发送WhatsApp消息" width="560px">
      <el-form :model="sendForm" label-width="90px">
        <el-form-item label="目标客户">
          <el-select
            v-model="sendForm.companyId"
            filterable
            remote
            reserve-keyword
            placeholder="输入客户名称搜索"
            :remote-method="searchCompanies"
            :loading="companyLoading"
            clearable
            style="width: 100%"
          >
            <el-option
              v-for="item in companyOptions"
              :key="item.id"
              :label="item.companyName"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="选择模板">
          <el-select v-model="sendForm.templateId" placeholder="选择话术模板" clearable style="width: 100%" @change="handleTemplateChange">
            <el-option label="公司介绍" :value="1" />
            <el-option label="产品图片" :value="2" />
            <el-option label="问需求" :value="3" />
            <el-option label="报价引导" :value="4" />
          </el-select>
        </el-form-item>
        <el-form-item label="消息内容">
          <el-input v-model="sendForm.content" type="textarea" :rows="6" placeholder="输入消息内容..." />
        </el-form-item>
        <el-form-item label="发送图片">
          <el-upload action="/api/upload" :limit="1" list-type="picture">
            <el-button type="primary">上传图片</el-button>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSendDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSend" :loading="sending">发送</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getCompanies } from '@/api/company'
import { sendWhatsappText, getAllWhatsappRecords } from '@/api/whatsapp'

const showSendDialog = ref(false)
const activeTemplate = ref('1')
const companyOptions = ref([])
const companyLoading = ref(false)
const sending = ref(false)

const sendForm = reactive({
  companyId: null,
  content: '',
  imageUrl: '',
  templateId: null
})

const messageRecords = ref([])

async function loadMessageRecords() {
  try {
    const res = await getAllWhatsappRecords()
    messageRecords.value = res.data || []
  } catch (e) {
    console.error('加载发送记录失败:', e)
    messageRecords.value = []
  }
}

onMounted(() => {
  loadMessageRecords()
})

const templates = {
  1: `Sawadee ka! 🙏\n\nI'm [Name] from [Company], a professional auto parts manufacturer in China.\n\nWe specialize in:\n• Mirror Covers (Toyota/Isuzu)\n• Front Grilles\n• Bumper Assemblies\n\nCan I send you our catalog?`,
  2: `Here are our best-selling products for Thai market:\n\n[发送产品图片]\n\nThese are very popular among Thai distributors. High quality with competitive price!`,
  3: `May I know what products you are currently sourcing?\n\nWe can provide:\n• Free samples\n• Competitive pricing\n• Fast delivery (15-20 days)`,
  4: `We have a special promotion this month:\n\n• 10% discount on first order\n• Free samples (freight collect)\n• MOQ from 50 pcs\n\nWould you like me to prepare a quotation for you?`
}

async function searchCompanies(query) {
  if (!query || query.length < 1) {
    companyOptions.value = []
    return
  }
  companyLoading.value = true
  try {
    const res = await getCompanies({ companyName: query, page: 1, size: 20 })
    companyOptions.value = res.data?.records || res.data?.list || res.data || []
  } catch (e) {
    companyOptions.value = []
  } finally {
    companyLoading.value = false
  }
}

function handleTemplateChange(val) {
  if (val && templates[val]) {
    sendForm.content = templates[val]
  }
}

function useTemplate(id) {
  sendForm.content = templates[id]
  sendForm.templateId = id
  ElMessage.success('已加载话术模板')
}

async function handleSend() {
  if (!sendForm.content) {
    ElMessage.warning('请输入消息内容')
    return
  }
  if (!sendForm.companyId) {
    ElMessage.warning('请选择目标客户')
    return
  }
  
  sending.value = true
  try {
    const company = companyOptions.value.find(c => c.id === sendForm.companyId)
    await sendWhatsappText({
      companyId: sendForm.companyId,
      phoneNumber: company?.phone || '',
      content: sendForm.content
    })
    ElMessage.success('WhatsApp消息发送任务已创建')
    showSendDialog.value = false
    sendForm.content = ''
    sendForm.templateId = null
    await loadMessageRecords()
  } catch (e) {
    ElMessage.error('发送失败')
    console.error(e)
  } finally {
    sending.value = false
  }
}

function getStatusType(status) {
  const types = { Pending: 'info', Sent: '', Delivered: 'success', Read: 'warning', Replied: 'success', Failed: 'danger' }
  return types[status] || ''
}

function getStatusLabel(status) {
  const labels = { Pending: '待发送', Sent: '已发送', Delivered: '已送达', Read: '已读', Replied: '已回复', Failed: '发送失败' }
  return labels[status] || status
}

function formatDateTime(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}
</script>

<style scoped>
.whatsapp-manager { padding: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; font-weight: bold; }
.template-content { font-size: 14px; line-height: 1.6; margin-bottom: 10px; }
.template-content ul { padding-left: 20px; }
</style>
