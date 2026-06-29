<template>
  <div class="mcp-management">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>MCP 工具管理</span>
          <el-button type="primary" @click="showDialog = true">
            <el-icon><Plus /></el-icon> 添加 MCP 工具
          </el-button>
        </div>
      </template>
      
      <el-table :data="tools" v-loading="loading">
        <el-table-column prop="name" label="工具名称" width="150" />
        <el-table-column prop="toolType" label="类型" width="120">
          <template #default="{ row }">
            <el-tag size="small">{{ row.toolType || '-' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="200" />
        <el-table-column prop="endpoint" label="端点" min-width="150" show-overflow-tooltip />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.enabled ? 'success' : 'info'" size="small">
              {{ row.enabled ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button type="success" size="small" @click="handleExecute(row)">执行</el-button>
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

    <el-dialog v-model="showDialog" :title="isEdit ? '编辑 MCP 工具' : '添加 MCP 工具'" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="工具名称" required>
          <el-input v-model="form.name" placeholder="工具唯一名称" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="form.toolType" placeholder="选择类型" style="width: 100%">
            <el-option label="HTTP API" value="http" />
            <el-option label="数据库" value="database" />
            <el-option label="文件操作" value="file" />
            <el-option label="命令执行" value="command" />
            <el-option label="自定义" value="custom" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="2" placeholder="工具描述" />
        </el-form-item>
        <el-form-item label="端点">
          <el-input v-model="form.endpoint" placeholder="API 端点或命令" />
        </el-form-item>
        <el-form-item label="能力">
          <el-input v-model="form.capabilities" type="textarea" :rows="2" placeholder="工具能力列表" />
        </el-form-item>
        <el-form-item label="配置">
          <el-input v-model="form.config" type="textarea" :rows="3" placeholder="JSON 配置" />
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

    <el-dialog v-model="showExecuteDialog" title="执行 MCP 工具" width="500px">
      <el-form :model="executeForm" label-width="100px">
        <el-form-item label="工具名称">
          <el-input v-model="executeForm.toolName" disabled />
        </el-form-item>
        <el-form-item label="参数">
          <el-input v-model="executeForm.parameters" type="textarea" :rows="4" placeholder='{"key": "value"}' />
        </el-form-item>
      </el-form>
      <div v-if="executeResult" class="execute-result">
        <h4>执行结果:</h4>
        <pre>{{ executeResult }}</pre>
      </div>
      <template #footer>
        <el-button @click="showExecuteDialog = false">关闭</el-button>
        <el-button type="success" @click="handleDoExecute" :loading="executing">执行</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { 
  getMcpTools, createMcpTool, updateMcpTool, deleteMcpTool, 
  toggleMcpTool, executeMcpTool 
} from '@/api/aiManagement'

const loading = ref(false)
const saving = ref(false)
const executing = ref(false)
const tools = ref([])
const showDialog = ref(false)
const showExecuteDialog = ref(false)
const isEdit = ref(false)
const executeResult = ref('')

const form = reactive({
  id: null,
  name: '',
  toolType: '',
  description: '',
  endpoint: '',
  capabilities: '',
  config: '',
  enabled: true
})

const executeForm = reactive({
  toolId: null,
  toolName: '',
  parameters: '{}'
})

onMounted(() => {
  loadTools()
})

async function loadTools() {
  loading.value = true
  try {
    const res = await getMcpTools()
    tools.value = res.data || []
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
    name: row.name,
    toolType: row.toolType,
    description: row.description,
    endpoint: row.endpoint,
    capabilities: row.capabilities,
    config: row.config,
    enabled: row.enabled
  })
  showDialog.value = true
}

async function handleSave() {
  if (!form.name) {
    ElMessage.warning('请填写工具名称')
    return
  }
  
  saving.value = true
  try {
    if (isEdit.value) {
      await updateMcpTool(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await createMcpTool(form)
      ElMessage.success('添加成功')
    }
    showDialog.value = false
    loadTools()
  } catch (e) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

function handleExecute(row) {
  executeForm.toolId = row.id
  executeForm.toolName = row.name
  executeForm.parameters = '{}'
  executeResult.value = ''
  showExecuteDialog.value = true
}

async function handleDoExecute() {
  executing.value = true
  try {
    const res = await executeMcpTool({
      toolId: executeForm.toolId,
      toolName: executeForm.toolName,
      parameters: executeForm.parameters
    })
    if (res.data.error) {
      executeResult.value = '错误: ' + res.data.error
    } else {
      executeResult.value = res.data.result
    }
  } catch (e) {
    executeResult.value = '执行失败: ' + e.message
  } finally {
    executing.value = false
  }
}

async function handleToggle(row) {
  try {
    await toggleMcpTool(row.id, !row.enabled)
    ElMessage.success('更新成功')
    loadTools()
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm('确定删除该工具?', '提示', { type: 'warning' })
    await deleteMcpTool(row.id)
    ElMessage.success('删除成功')
    loadTools()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}
</script>

<style scoped>
.mcp-management {
  padding: 20px;
}

.execute-result {
  margin-top: 15px;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 4px;
}

.execute-result h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
}

.execute-result pre {
  margin: 0;
  white-space: pre-wrap;
  word-break: break-all;
  font-size: 12px;
}
</style>
