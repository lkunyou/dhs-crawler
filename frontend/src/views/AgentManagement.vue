<template>
  <div class="agent-management">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>Agent 管理</span>
          <el-button type="primary" @click="showDialog = true">
            <el-icon><Plus /></el-icon> 添加 Agent
          </el-button>
        </div>
      </template>
      
      <el-table :data="agents" v-loading="loading">
        <el-table-column prop="agentType" label="类型" width="150" />
        <el-table-column prop="name" label="名称" width="150" />
        <el-table-column prop="description" label="描述" min-width="200" />
        <el-table-column prop="prompt" label="提示词" min-width="200" show-overflow-tooltip />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.enabled ? 'success' : 'info'" size="small">
              {{ row.enabled ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button 
              :type="row.enabled ? 'warning' : 'success'" 
              size="small" 
              @click="handleToggle(row)"
            >
              {{ row.enabled ? '禁用' : '启用' }}
            </el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="showDialog" :title="isEdit ? '编辑 Agent' : '添加 Agent'" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="类型标识" required>
          <el-input v-model="form.agentType" placeholder="如: code_assistant" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="名称" required>
          <el-input v-model="form.name" placeholder="Agent 名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="2" placeholder="描述" />
        </el-form-item>
        <el-form-item label="提示词">
          <el-input v-model="form.prompt" type="textarea" :rows="4" placeholder="系统提示词配置" />
        </el-form-item>
        <el-form-item label="配置">
          <el-input v-model="form.config" type="textarea" :rows="2" placeholder="JSON 配置" />
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
import { getAgents, createAgent, updateAgent, deleteAgent, toggleAgent } from '@/api/aiManagement'

const loading = ref(false)
const saving = ref(false)
const agents = ref([])
const showDialog = ref(false)
const isEdit = ref(false)

const form = reactive({
  id: null,
  agentType: '',
  name: '',
  description: '',
  prompt: '',
  config: '',
  enabled: true
})

onMounted(() => {
  loadAgents()
})

async function loadAgents() {
  loading.value = true
  try {
    const res = await getAgents()
    agents.value = res.data || []
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

function handleEdit(row) {
  isEdit.value = true
  Object.assign(form, {
    id: row.id,
    agentType: row.agentType,
    name: row.name,
    description: row.description,
    prompt: row.prompt,
    config: row.config,
    enabled: row.enabled
  })
  showDialog.value = true
}

async function handleSave() {
  if (!form.agentType || !form.name) {
    ElMessage.warning('请填写必填项')
    return
  }
  
  saving.value = true
  try {
    if (isEdit.value) {
      await updateAgent(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await createAgent(form)
      ElMessage.success('添加成功')
    }
    showDialog.value = false
    loadAgents()
  } catch (e) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

async function handleToggle(row) {
  try {
    await toggleAgent(row.id, !row.enabled)
    ElMessage.success('更新成功')
    loadAgents()
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm('确定删除该 Agent?', '提示', { type: 'warning' })
    await deleteAgent(row.id)
    ElMessage.success('删除成功')
    loadAgents()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}
</script>

<style scoped>
.agent-management {
  padding: 20px;
}
</style>
