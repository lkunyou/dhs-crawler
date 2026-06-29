<template>
  <div class="model-management">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>AI 模型配置</span>
          <el-button type="primary" @click="showDialog = true">
            <el-icon><Plus /></el-icon> 添加模型
          </el-button>
        </div>
      </template>
      
      <div class="provider-grid">
        <div v-for="provider in providerList" :key="provider.key" class="provider-card">
          <div class="provider-header">
            <span class="provider-name">{{ provider.name }}</span>
            <el-tag size="small" :type="provider.verified ? 'success' : 'info'">
              {{ provider.verified ? '已配置' : '未配置' }}
            </el-tag>
          </div>
          <div class="provider-desc">{{ provider.description }}</div>
          <div class="provider-status">
            <span>状态: </span>
            <el-switch 
              :model-value="provider.enabled" 
              @change="handleToggleProvider(provider)"
              size="small"
            />
          </div>
          <div class="provider-actions">
            <el-button size="small" type="primary" @click="editModel(provider)">配置</el-button>
          </div>
        </div>
      </div>
      
      <el-divider />
      
      <el-table :data="models" v-loading="loading">
        <el-table-column prop="provider" label="提供商" width="120">
          <template #default="{ row }">
            <el-tag size="small" type="primary">{{ row.provider }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="modelName" label="模型名称" width="150" />
        <el-table-column prop="baseUrl" label="API 地址" min-width="200" show-overflow-tooltip />
        <el-table-column prop="apiEndpoint" label="端点" width="150" show-overflow-tooltip />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.enabled ? 'success' : 'info'" size="small">
              {{ row.enabled ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="showDialog" :title="isEdit ? '编辑模型' : '添加模型'" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="提供商" required>
          <el-select v-model="form.provider" placeholder="选择提供商" style="width: 100%" :disabled="isEdit">
            <el-option label="DeepSeek" value="deepseek" />
            <el-option label="Kimi (月之暗面)" value="kimi" />
            <el-option label="智谱 GLM" value="glm" />
            <el-option label="豆包 Doubao" value="doubao" />
            <el-option label="通义千问 Qwen" value="qwen" />
            <el-option label="MiniMax" value="minimax" />
            <el-option label="OpenAI" value="openai" />
            <el-option label="Claude" value="claude" />
          </el-select>
        </el-form-item>
        <el-form-item label="模型名称" required>
          <el-input v-model="form.modelName" placeholder="如: deepseek-chat, gpt-4" />
        </el-form-item>
        <el-form-item label="API 地址" required>
          <el-input v-model="form.baseUrl" placeholder="如: https://api.deepseek.com" />
        </el-form-item>
        <el-form-item label="端点">
          <el-input v-model="form.apiEndpoint" placeholder="如: /chat/completions" />
        </el-form-item>
        <el-form-item label="API 密钥" required>
          <el-input v-model="form.apiKey" type="password" show-password placeholder="API Key" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="2" placeholder="模型描述" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sortOrder" :min="0" :max="100" />
        </el-form-item>
        <el-form-item label="启用">
          <el-switch v-model="form.enabled" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { 
  getAiModels, createAiModel, updateAiModel, 
  deleteAiModel, toggleAiModel 
} from '@/api/aiModel'

const loading = ref(false)
const saving = ref(false)
const models = ref([])
const showDialog = ref(false)
const isEdit = ref(false)

const providerList = ref([
  { key: 'deepseek', name: 'DeepSeek', description: '深度求索 AI 助手', verified: false, enabled: false },
  { key: 'kimi', name: 'Kimi', description: '月之暗面 AI 助手，支持长文本', verified: false, enabled: false },
  { key: 'glm', name: '智谱 GLM', description: '智谱 AI 大模型', verified: false, enabled: false },
  { key: 'doubao', name: '豆包', description: '字节跳动 AI 助手', verified: false, enabled: false },
  { key: 'qwen', name: '通义千问', description: '阿里云 AI 大模型', verified: false, enabled: false },
  { key: 'minimax', name: 'MiniMax', description: '稀宇科技 AI 助手', verified: false, enabled: false },
  { key: 'openai', name: 'OpenAI', description: 'GPT 系列模型', verified: false, enabled: false },
  { key: 'claude', name: 'Claude', description: 'Anthropic AI 助手', verified: false, enabled: false }
])

const form = reactive({
  id: null,
  provider: '',
  modelName: '',
  baseUrl: '',
  apiEndpoint: '/chat/completions',
  apiKey: '',
  description: '',
  sortOrder: 0,
  enabled: true
})

onMounted(() => {
  loadModels()
})

async function loadModels() {
  loading.value = true
  try {
    const res = await getAiModels()
    models.value = res.data || []
    updateProviderStatus()
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

function updateProviderStatus() {
  providerList.value.forEach(p => {
    const model = models.value.find(m => m.provider === p.key)
    if (model) {
      p.verified = !!(model.apiKey && model.apiKey.trim() !== '')
      p.enabled = model.enabled
    } else {
      p.verified = false
      p.enabled = false
    }
  })
}

async function handleToggleProvider(provider) {
  const model = models.value.find(m => m.provider === provider.key)
  if (model) {
    try {
      await toggleAiModel(model.id, !model.enabled)
      ElMessage.success('更新成功')
      loadModels()
    } catch (e) {
      ElMessage.error('操作失败')
    }
  }
}

function editModel(provider) {
  const model = models.value.find(m => m.provider === provider.key)
  if (model) {
    handleEdit(model)
  } else {
    isEdit.value = false
    Object.assign(form, {
      id: null,
      provider: provider.key,
      modelName: getDefaultModelName(provider.key),
      baseUrl: getDefaultBaseUrl(provider.key),
      apiEndpoint: '/chat/completions',
      apiKey: '',
      description: provider.description,
      sortOrder: providerList.value.indexOf(provider),
      enabled: true
    })
    showDialog.value = true
  }
}

function handleEdit(row) {
  isEdit.value = true
  Object.assign(form, {
    id: row.id,
    provider: row.provider,
    modelName: row.modelName,
    baseUrl: row.baseUrl,
    apiEndpoint: row.apiEndpoint,
    apiKey: row.apiKey,
    description: row.description,
    sortOrder: row.sortOrder,
    enabled: row.enabled
  })
  showDialog.value = true
}

async function handleSave() {
  if (!form.provider || !form.modelName || !form.baseUrl) {
    ElMessage.warning('请填写必填项')
    return
  }
  
  saving.value = true
  try {
    if (isEdit.value) {
      await updateAiModel(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await createAiModel(form)
      ElMessage.success('添加成功')
    }
    showDialog.value = false
    loadModels()
  } catch (e) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm('确定删除该模型配置?', '提示', { type: 'warning' })
    await deleteAiModel(row.id)
    ElMessage.success('删除成功')
    loadModels()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

function getDefaultBaseUrl(provider) {
  const urls = {
    'deepseek': 'https://api.deepseek.com',
    'kimi': 'https://api.moonshot.cn/v1',
    'glm': 'https://open.bigmodel.cn/api/paas/v4',
    'doubao': 'https://ark.cn-beijing.volces.com/api/v3',
    'qwen': 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    'minimax': 'https://api.minimax.chat/v1',
    'openai': 'https://api.openai.com/v1',
    'claude': 'https://api.anthropic.com/v1'
  }
  return urls[provider] || ''
}

function getDefaultModelName(provider) {
  const models = {
    'deepseek': 'deepseek-chat',
    'kimi': 'moonshot-v1-8k',
    'glm': 'glm-4',
    'doubao': 'doubao-pro-32k',
    'qwen': 'qwen-plus',
    'minimax': 'abab6-chat',
    'openai': 'gpt-4',
    'claude': 'claude-3-sonnet-20240229'
  }
  return models[provider] || ''
}
</script>

<style scoped>
.model-management {
  padding: 20px;
}

.provider-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.provider-card {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 16px;
  background: #fafafa;
  transition: all 0.3s;
}

.provider-card:hover {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.provider-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.provider-name {
  font-weight: bold;
  font-size: 16px;
  color: #303133;
}

.provider-desc {
  font-size: 12px;
  color: #909399;
  margin-bottom: 12px;
}

.provider-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #606266;
  margin-bottom: 12px;
}

.provider-actions {
  display: flex;
  gap: 8px;
}
</style>
