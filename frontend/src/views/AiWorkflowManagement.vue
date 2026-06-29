<template>
  <div class="workflow-management">
    <el-card>
      <template #header>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>Agent 开发工作流</span>
          <el-button type="primary" @click="showDialog = true">
            <el-icon><Plus /></el-icon> 创建工作流
          </el-button>
        </div>
      </template>
      
      <el-tabs v-model="activeTab">
        <el-tab-pane label="工作流列表" name="list">
          <el-row :gutter="16" v-loading="loading">
            <el-col :span="6" v-for="row in workflows" :key="row.id" style="margin-bottom: 16px;">
              <el-card shadow="hover" class="workflow-card" @click="handleEdit(row)">
                <template #header>
                  <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-weight: bold; font-size: 14px;">{{ row.name }}</span>
                    <el-dropdown trigger="click" @command="(cmd) => handleCardAction(cmd, row)" @click.stop>
                      <el-icon style="cursor: pointer; font-size: 18px; color: #909399;"><MoreFilled /></el-icon>
                      <template #dropdown>
                        <el-dropdown-menu>
                          <el-dropdown-item command="edit">编辑</el-dropdown-item>
                          <el-dropdown-item command="execute">执行</el-dropdown-item>
                          <el-dropdown-item command="toggle">
                            {{ row.enabled ? '停用' : '启用' }}
                          </el-dropdown-item>
                          <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                        </el-dropdown-menu>
                      </template>
                    </el-dropdown>
                  </div>
                </template>
                <div class="card-body">
                  <p class="card-desc">{{ row.description || '暂无描述' }}</p>
                  <div class="card-info">
                    <el-tag size="small" type="primary">{{ row.agentType || '-' }}</el-tag>
                    <span class="card-steps">{{ row.steps?.length || 0 }} 个节点</span>
                    <el-tag :type="row.enabled ? 'success' : 'info'" size="small">
                      {{ row.enabled ? '启用' : '停用' }}
                    </el-tag>
                  </div>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6" v-if="workflows.length === 0 && !loading">
              <el-card class="workflow-card empty-card">
                <div style="text-align: center; padding: 40px 0; color: #909399;">
                  <el-icon style="font-size: 48px;"><Plus /></el-icon>
                  <p style="margin-top: 8px;">暂无工作流，点击右上角创建</p>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </el-tab-pane>
        
        <el-tab-pane label="执行记录" name="executions">
          <el-table :data="executions" v-loading="execLoading" style="margin-top: 16px;">
            <el-table-column prop="workflowName" label="工作流" width="180" />
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag 
                  :type="getStatusType(row.status)" 
                  size="small"
                >
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="currentStep" label="当前步骤" width="100" />
            <el-table-column prop="startedAt" label="开始时间" width="160">
              <template #default="{ row }">
                {{ formatTime(row.startedAt) }}
              </template>
            </el-table-column>
            <el-table-column prop="completedAt" label="完成时间" width="160">
              <template #default="{ row }">
                {{ formatTime(row.completedAt) }}
              </template>
            </el-table-column>
            <el-table-column prop="errorMessage" label="错误信息" min-width="150" show-overflow-tooltip />
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="{ row }">
                <el-button type="info" size="small" @click="handleViewOutput(row)">查看</el-button>
                <el-button 
                  v-if="row.status === 'running'" 
                  type="warning" 
                  size="small" 
                  @click="handleStop(row)"
                >
                  停止
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 设计工作流对话框 -->
    <el-dialog v-model="showDialog" :title="isEdit ? '设计' : '创建工作流'" width="1100px" top="5vh" @opened="handleDialogOpened">
      <div style="margin-bottom: 12px;">
        <el-button size="small" :type="showFormFields ? 'primary' : 'default'" @click="showFormFields = !showFormFields">
          <el-icon><Edit /></el-icon> {{ showFormFields ? '隐藏编辑' : '编辑' }}
        </el-button>
      </div>
      <el-form :model="form" label-width="100px" v-show="showFormFields">
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="工作流名称" required>
              <el-input v-model="form.name" placeholder="输入工作流名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="Agent类型">
              <el-select v-model="form.agentType" placeholder="选择关联Agent" style="width: 100%">
                <el-option label="通用" value="general" />
                <el-option label="代码助手" value="code_assistant" />
                <el-option label="数据分析" value="data_analyst" />
                <el-option label="客服助手" value="customer_service" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="16">
            <el-form-item label="描述">
              <el-input v-model="form.description" placeholder="工作流描述" />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="超时(秒)">
              <el-input-number v-model="form.timeout" :min="30" :max="3600" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="启用">
              <el-switch v-model="form.enabled" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div style="width: 100%; height: 500px;">
        <WorkflowCanvas ref="workflowCanvasRef" :model-value="canvasData" @update:model-value="onCanvasDataUpdate" />
      </div>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="saving">保存</el-button>
      </template>
    </el-dialog>

    <!-- 执行工作流对话框 -->
    <el-dialog v-model="showExecuteDialog" title="执行工作流" width="500px">
      <el-form :model="executeForm" label-width="100px">
        <el-form-item label="工作流">
          <el-input v-model="executeForm.workflowName" disabled />
        </el-form-item>
        <el-form-item label="输入参数">
          <el-input v-model="executeForm.inputJson" type="textarea" :rows="4" placeholder='{"key": "value"}' />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showExecuteDialog = false">取消</el-button>
        <el-button type="success" @click="handleDoExecute" :loading="executing">执行</el-button>
      </template>
    </el-dialog>

    <!-- 执行结果对话框 -->
    <el-dialog v-model="showOutputDialog" title="执行结果" width="600px">
      <div v-if="currentExecution">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="工作流">{{ currentExecution.workflowName }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <el-tag :type="getStatusType(currentExecution.status)" size="small">
              {{ getStatusText(currentExecution.status) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="当前步骤">{{ currentExecution.currentStep }}</el-descriptions-item>
          <el-descriptions-item label="开始时间">{{ formatTime(currentExecution.startedAt) }}</el-descriptions-item>
        </el-descriptions>
        <div v-if="currentExecution.errorMessage" style="margin-top: 16px;">
          <el-alert type="error" :title="currentExecution.errorMessage" :closable="false" />
        </div>
        <div v-if="currentExecution.output" style="margin-top: 16px;">
          <h4>输出结果:</h4>
          <pre class="output-pre">{{ formatJson(currentExecution.output) }}</pre>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Delete, MoreFilled, Edit } from '@element-plus/icons-vue'
import WorkflowCanvas from '@/components/WorkflowCanvas.vue'
import { 
  getWorkflows, createWorkflow, updateWorkflow, 
  deleteWorkflow, toggleWorkflow, 
  getAllExecutions, executeWorkflow, stopExecution, getExecution 
} from '@/api/aiWorkflow'

const workflowCanvasRef = ref(null)

const loading = ref(false)
const execLoading = ref(false)
const saving = ref(false)
const executing = ref(false)
const workflows = ref([])
const executions = ref([])
const showDialog = ref(false)
const showExecuteDialog = ref(false)
const showOutputDialog = ref(false)
const isEdit = ref(false)
const currentExecution = ref(null)
const activeTab = ref('list')
const showFormFields = ref(false)

const form = reactive({
  id: null,
  name: '',
  description: '',
  agentType: 'general',
  timeout: 300,
  enabled: true,
  steps: [],
  edges: []
})

// 画布数据：组合 steps 和 edges 传给 WorkflowCanvas
const canvasData = computed(() => ({
  steps: form.steps,
  edges: form.edges
}))

// 画布更新时同步回 form
function onCanvasDataUpdate(data) {
  if (data && typeof data === 'object') {
    if (Array.isArray(data)) {
      form.steps = data
    } else {
      form.steps = data.steps || []
      form.edges = data.edges || []
    }
  }
}

const executeForm = reactive({
  workflowId: null,
  workflowName: '',
  inputJson: '{}'
})

onMounted(() => {
  loadWorkflows()
  loadExecutions()
})

async function loadWorkflows() {
  loading.value = true
  try {
    const res = await getWorkflows()
    workflows.value = res.data || []
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

async function loadExecutions() {
  execLoading.value = true
  try {
    const res = await getAllExecutions()
    executions.value = res.data || []
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    execLoading.value = false
  }
}

function handleEdit(row) {
  isEdit.value = true
  Object.assign(form, {
    id: row.id,
    name: row.name,
    description: row.description,
    agentType: row.agentType,
    timeout: row.timeout,
    enabled: row.enabled,
    steps: row.steps || [],
    edges: row.edges || []
  })
  showDialog.value = true
}

// 对话框打开后触发画布刷新
function handleDialogOpened() {
  console.log('[AiWorkflowManagement] Dialog opened, refreshing canvas...')
  setTimeout(() => {
    if (workflowCanvasRef.value) {
      workflowCanvasRef.value.refresh()
    }
  }, 100)
}

async function handleSave() {
  if (!form.name) {
    ElMessage.warning('请输入工作流名称')
    return
  }
  
  // 同步画布数据到表单
  if (workflowCanvasRef.value) {
    const canvasData = workflowCanvasRef.value.syncSteps()
    // canvasData 是 {steps, edges} 对象
    if (canvasData && typeof canvasData === 'object' && !Array.isArray(canvasData)) {
      form.steps = canvasData.steps || []
      form.edges = canvasData.edges || []
    } else if (Array.isArray(canvasData)) {
      form.steps = canvasData
      form.edges = []
    }
  }
  
  saving.value = true
  try {
    if (isEdit.value) {
      await updateWorkflow(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await createWorkflow(form)
      ElMessage.success('创建成功')
    }
    showDialog.value = false
    loadWorkflows()
  } catch (e) {
    ElMessage.error('保存失败: ' + (e.message || e))
  } finally {
    saving.value = false
  }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm('确定删除该工作流?', '提示', { type: 'warning' })
    await deleteWorkflow(row.id)
    ElMessage.success('删除成功')
    loadWorkflows()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

async function handleToggle(row) {
  try {
    await toggleWorkflow(row.id, !row.enabled)
    ElMessage.success('更新成功')
    loadWorkflows()
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

function handleExecute(row) {
  executeForm.workflowId = row.id
  executeForm.workflowName = row.name
  executeForm.inputJson = '{}'
  showExecuteDialog.value = true
}

async function handleDoExecute() {
  executing.value = true
  try {
    let input = {}
    try {
      input = JSON.parse(executeForm.inputJson)
    } catch (e) {
      ElMessage.warning('输入参数JSON格式错误')
      return
    }
    await executeWorkflow(executeForm.workflowId, input)
    ElMessage.success('工作流已启动')
    showExecuteDialog.value = false
    activeTab.value = 'executions'
    loadExecutions()
  } catch (e) {
    ElMessage.error('执行失败')
  } finally {
    executing.value = false
  }
}

async function handleViewOutput(row) {
  try {
    const res = await getExecution(row.id)
    currentExecution.value = res.data
    showOutputDialog.value = true
  } catch (e) {
    ElMessage.error('加载失败')
  }
}

async function handleStop(row) {
  try {
    await stopExecution(row.id)
    ElMessage.success('已停止')
    loadExecutions()
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

function handleCardAction(command, row) {
  switch (command) {
    case 'edit':
      handleEdit(row)
      break
    case 'execute':
      handleExecute(row)
      break
    case 'toggle':
      handleToggle(row)
      break
    case 'delete':
      handleDelete(row)
      break
  }
}

function getStatusType(status) {
  const types = {
    'pending': 'info',
    'running': 'primary',
    'completed': 'success',
    'failed': 'danger',
    'stopped': 'warning'
  }
  return types[status] || 'info'
}

function getStatusText(status) {
  const texts = {
    'pending': '等待中',
    'running': '执行中',
    'completed': '已完成',
    'failed': '失败',
    'stopped': '已停止'
  }
  return texts[status] || status
}

function formatTime(time) {
  if (!time) return '-'
  return new Date(time).toLocaleString('zh-CN')
}

function formatJson(obj) {
  if (typeof obj === 'string') {
    try {
      return JSON.stringify(JSON.parse(obj), null, 2)
    } catch {
      return obj
    }
  }
  return JSON.stringify(obj, null, 2)
}
</script>

<style scoped>
.workflow-management {
  padding: 20px;
}

.steps-editor {
  max-height: 400px;
  overflow-y: auto;
}

.step-item {
  margin-bottom: 12px;
}

.output-pre {
  background: #f5f7fa;
  padding: 12px;
  border-radius: 4px;
  overflow-x: auto;
  font-size: 12px;
}

.workflow-card {
  height: 200px;
  display: flex;
  flex-direction: column;
  cursor: pointer;
}

.workflow-card :deep(.el-card__body) {
  flex: 1;
  overflow: hidden;
}

.card-body {
  height: 100%;
}

.card-desc {
  margin: 0 0 12px 0;
  font-size: 12px;
  color: #606266;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.5;
}

.card-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}

.card-steps {
  font-size: 12px;
  color: #909399;
}

.empty-card {
  height: 200px;
}
</style>
