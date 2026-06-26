<template>
  <div class="system-config">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>配置参数</span>
          <div>
            <el-button type="success" @click="handleInitDefaults">
              <el-icon><Refresh /></el-icon> 初始化默认配置
            </el-button>
            <el-button type="primary" @click="handleAdd">
              <el-icon><Plus /></el-icon> 新增配置
            </el-button>
          </div>
        </div>
      </template>

      <el-tabs v-model="activeTab" type="border-card">
        <el-tab-pane label="基本配置" name="common">
          <el-table :data="commonConfigs" border style="width: 100%">
            <el-table-column prop="configKey" label="配置键" width="250" />
            <el-table-column prop="configValue" label="配置值" min-width="250">
              <template #default="{ row }">
                <el-tooltip :content="row.configValue" placement="top" :open-delay="300">
                  <span class="config-value">{{ row.configValue }}</span>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column prop="description" label="描述" min-width="300" />
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
                <el-button type="danger" size="small" @click="handleDelete(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="搜索配置" name="search">
          <el-table :data="searchConfigs" border style="width: 100%">
            <el-table-column prop="configKey" label="配置键" width="250" />
            <el-table-column prop="configValue" label="配置值" min-width="250" />
            <el-table-column prop="description" label="描述" min-width="300" />
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
                <el-button type="danger" size="small" @click="handleDelete(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="爬虫配置" name="crawler">
          <el-table :data="crawlerConfigs" border style="width: 100%">
            <el-table-column prop="configKey" label="配置键" width="250" />
            <el-table-column prop="configValue" label="配置值" min-width="250" />
            <el-table-column prop="description" label="描述" min-width="300" />
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
                <el-button type="danger" size="small" @click="handleDelete(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="邮件配置" name="email">
          <el-table :data="emailConfigs" border style="width: 100%">
            <el-table-column prop="configKey" label="配置键" width="250" />
            <el-table-column prop="configValue" label="配置值" min-width="250" />
            <el-table-column prop="description" label="描述" min-width="300" />
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
                <el-button type="danger" size="small" @click="handleDelete(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="WhatsApp配置" name="whatsapp">
          <el-table :data="whatsappConfigs" border style="width: 100%">
            <el-table-column prop="configKey" label="配置键" width="250" />
            <el-table-column prop="configValue" label="配置值" min-width="250" />
            <el-table-column prop="description" label="描述" min-width="300" />
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
                <el-button type="danger" size="small" @click="handleDelete(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="限流配置" name="rate-limit">
          <el-table :data="rateLimitConfigs" border style="width: 100%">
            <el-table-column prop="configKey" label="配置键" width="250" />
            <el-table-column prop="configValue" label="配置值" min-width="250" />
            <el-table-column prop="description" label="描述" min-width="300" />
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="handleEdit(row)">编辑</el-button>
                <el-button type="danger" size="small" @click="handleDelete(row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑配置' : '新增配置'" width="600px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="配置分类" required>
          <el-select v-model="form.configType" placeholder="请选择分类" style="width: 100%">
            <el-option label="基本配置" value="common" />
            <el-option label="搜索配置" value="search" />
            <el-option label="爬虫配置" value="crawler" />
            <el-option label="邮件配置" value="email" />
            <el-option label="WhatsApp配置" value="whatsapp" />
            <el-option label="限流配置" value="rate-limit" />
          </el-select>
        </el-form-item>
        <el-form-item label="配置键" required>
          <el-input v-model="form.configKey" placeholder="请输入配置键" />
        </el-form-item>
        <el-form-item label="配置值" required>
          <el-input v-model="form.configValue" type="textarea" :rows="3" placeholder="请输入配置值" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="2" placeholder="请输入描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh } from '@element-plus/icons-vue'
import { getConfigList, createConfig, updateConfig, deleteConfig, initDefaultConfigs } from '@/api/systemConfig'

const configList = ref([])
const activeTab = ref('common')
const dialogVisible = ref(false)
const isEdit = ref(false)
const form = reactive({
  id: null,
  configKey: '',
  configValue: '',
  configType: 'search',
  description: ''
})

const searchConfigs = computed(() => configList.value.filter(c => c.configType === 'search'))
const crawlerConfigs = computed(() => configList.value.filter(c => c.configType === 'crawler'))
const emailConfigs = computed(() => configList.value.filter(c => c.configType === 'email'))
const whatsappConfigs = computed(() => configList.value.filter(c => c.configType === 'whatsapp'))
const rateLimitConfigs = computed(() => configList.value.filter(c => c.configType === 'rate-limit'))
const commonConfigs = computed(() => configList.value.filter(c => c.configType === 'common'))

function resetForm() {
  form.id = null
  form.configKey = ''
  form.configValue = ''
  form.configType = activeTab.value
  form.description = ''
}

async function loadConfigs() {
  try {
    const res = await getConfigList()
    if (res.code === 200) {
      configList.value = res.data || []
    }
  } catch (e) {
    console.error('加载配置失败', e)
  }
}

function handleAdd() {
  resetForm()
  isEdit.value = false
  dialogVisible.value = true
}

function handleEdit(row) {
  Object.assign(form, row)
  isEdit.value = true
  dialogVisible.value = true
}

async function handleSubmit() {
  if (!form.configKey || !form.configValue || !form.configType) {
    ElMessage.warning('请填写完整信息')
    return
  }
  try {
    if (isEdit.value) {
      await updateConfig(form.id, form)
      ElMessage.success('配置已更新')
    } else {
      await createConfig(form)
      ElMessage.success('配置已创建')
    }
    dialogVisible.value = false
    loadConfigs()
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

async function handleDelete(id) {
  try {
    await ElMessageBox.confirm('确定删除该配置吗?', '提示', { type: 'warning' })
    await deleteConfig(id)
    ElMessage.success('删除成功')
    loadConfigs()
  } catch (e) {}
}

async function handleInitDefaults() {
  try {
    await ElMessageBox.confirm('确定要初始化默认配置吗? 已存在的配置不会被覆盖', '提示', { type: 'warning' })
    await initDefaultConfigs()
    ElMessage.success('默认配置已初始化')
    loadConfigs()
  } catch (e) {}
}

onMounted(loadConfigs)
</script>

<style scoped>
.system-config {
  padding: 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.config-value {
  display: inline-block;
  max-width: 400px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  vertical-align: bottom;
}
</style>
