<template>
  <div class="ai-chat-container">
    <el-container style="height: 100%">
      <el-aside width="280px" class="sidebar">
        <div class="sidebar-header">
          <h3>AI 对话助手</h3>
          <el-button type="primary" size="small" @click="handleNewChat" style="width: 100%; margin-top: 10px;">
            <el-icon><Plus /></el-icon> 新建对话
          </el-button>
        </div>
        
        <div class="conversation-list">
          <div v-for="conv in conversations" :key="conv.id" 
               class="conversation-item"
               :class="{ active: currentConversationId === conv.id }"
               @click="selectConversation(conv)">
            <span class="conversation-title">{{ conv.title || '新对话' }}</span>
            <el-icon class="delete-icon" @click.stop="handleDeleteConversation(conv.id)"><Delete /></el-icon>
          </div>
        </div>
        
        <div class="sidebar-footer">
          <el-tabs v-model="activeTab">
            <el-tab-pane label="Agent" name="agent">
              <div class="agent-list">
                <el-select v-model="selectedAgent" placeholder="选择 Agent" style="width: 100%; margin-bottom: 10px;">
                  <el-option label="代码助手" value="code_assistant" />
                  <el-option label="数据分析" value="data_analyst" />
                  <el-option label="客服" value="customer_service" />
                  <el-option label="通用助手" value="general" />
                </el-select>
                <el-input v-model="agentInput" placeholder="输入 Agent 任务" type="textarea" :rows="2" />
                <el-button type="warning" size="small" @click="handleExecuteAgent" :loading="agentLoading" style="width: 100%; margin-top: 10px;">
                  执行 Agent
                </el-button>
              </div>
            </el-tab-pane>
            <el-tab-pane label="Skill" name="skill">
              <div class="skill-list">
                <el-button type="success" size="small" @click="showSkillDialog = true" style="width: 100%; margin-bottom: 10px;">
                  <el-icon><Plus /></el-icon> 添加 Skill
                </el-button>
                <div v-for="skill in skills" :key="skill.id" class="skill-item">
                  <span>{{ skill.name }}</span>
                  <el-switch v-model="skill.enabled" @change="handleToggleSkill(skill)" />
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </el-aside>
      
      <el-main class="chat-area">
        <div class="chat-header">
          <h4>{{ currentConversationTitle }}</h4>
          <el-select v-model="selectedModel" placeholder="选择模型" style="width: 150px;">
            <el-option label="GPT-3.5" value="gpt-3.5-turbo" />
            <el-option label="GPT-4" value="gpt-4" />
            <el-option label="Claude" value="claude-3" />
          </el-select>
        </div>
        
        <div class="message-list" ref="messageListRef">
          <div v-if="messages.length === 0" class="empty-state">
            <el-empty description="开始对话吧">
              <template #image>
                <el-icon size="64" color="#409eff"><ChatDotRound /></el-icon>
              </template>
            </el-empty>
          </div>
          
          <div v-for="msg in messages" :key="msg.id" class="message" :class="msg.role">
            <div class="message-avatar">
              <el-icon v-if="msg.role === 'user'" size="24"><User /></el-icon>
              <el-icon v-else size="24"><ChatDotRound /></el-icon>
            </div>
            <div class="message-content">
              <div class="message-text" v-html="formatMessage(msg.content)"></div>
              <div class="message-time">{{ formatTime(msg.createdAt) }}</div>
            </div>
          </div>
          
          <div v-if="loading" class="message assistant">
            <div class="message-avatar">
              <el-icon size="24"><ChatDotRound /></el-icon>
            </div>
            <div class="message-content">
              <div class="message-text">
                <el-icon class="is-loading"><Loading /></el-icon> AI 正在思考...
              </div>
            </div>
          </div>
        </div>
        
        <div class="input-area">
          <el-input
            v-model="inputMessage"
            type="textarea"
            :rows="3"
            placeholder="输入消息..."
            @keydown.enter.ctrl="handleSend"
            resize="none"
          />
          <div class="input-actions">
            <span class="hint">Ctrl + Enter 发送</span>
            <el-button type="primary" @click="handleSend" :loading="loading" :disabled="!inputMessage.trim()">
              <el-icon><Promotion /></el-icon> 发送
            </el-button>
          </div>
        </div>
      </el-main>
    </el-container>
    
    <el-dialog v-model="showSkillDialog" title="添加 Skill" width="500px">
      <el-form :model="skillForm" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="skillForm.name" placeholder="Skill 名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="skillForm.description" type="textarea" :rows="3" placeholder="Skill 描述" />
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="skillForm.type" placeholder="选择类型">
            <el-option label="对话" value="chat" />
            <el-option label="工具" value="tool" />
            <el-option label="自动化" value="automation" />
          </el-select>
        </el-form-item>
        <el-form-item label="配置">
          <el-input v-model="skillForm.config" type="textarea" :rows="3" placeholder="JSON 配置" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSkillDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreateSkill">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Delete, ChatDotRound, User, Promotion, Loading } from '@element-plus/icons-vue'
import { 
  getConversations, getMessages, createConversation, deleteConversation,
  chat, executeAgent, getSkills, createSkill, updateSkill
} from '@/api/ai'

const messageListRef = ref(null)
const loading = ref(false)
const inputMessage = ref('')
const conversations = ref([])
const currentConversationId = ref(null)
const messages = ref([])
const selectedModel = ref('gpt-3.5-turbo')
const activeTab = ref('agent')
const selectedAgent = ref('')
const agentInput = ref('')
const agentLoading = ref(false)
const skills = ref([])
const showSkillDialog = ref(false)
const skillForm = reactive({
  name: '',
  description: '',
  type: 'chat',
  config: ''
})

const currentConversationTitle = computed(() => {
  const conv = conversations.value.find(c => c.id === currentConversationId.value)
  return conv ? conv.title || '新对话' : '新对话'
})

onMounted(async () => {
  await loadConversations()
  await loadSkills()
})

async function loadConversations() {
  try {
    const res = await getConversations()
    conversations.value = res.data || []
  } catch (e) {
    console.error(e)
  }
}

async function loadSkills() {
  try {
    const res = await getSkills()
    skills.value = res.data || []
  } catch (e) {
    console.error(e)
  }
}

async function handleNewChat() {
  try {
    const res = await createConversation('新对话')
    await loadConversations()
    selectConversation(res.data)
    ElMessage.success('新对话已创建')
  } catch (e) {
    ElMessage.error('创建失败')
  }
}

async function selectConversation(conv) {
  currentConversationId.value = conv.id
  try {
    const res = await getMessages(conv.id)
    messages.value = res.data || []
    scrollToBottom()
  } catch (e) {
    console.error(e)
  }
}

async function handleDeleteConversation(id) {
  try {
    await deleteConversation(id)
    await loadConversations()
    if (currentConversationId.value === id) {
      currentConversationId.value = null
      messages.value = []
    }
    ElMessage.success('已删除')
  } catch (e) {
    ElMessage.error('删除失败')
  }
}

async function handleSend() {
  if (!inputMessage.value.trim()) return
  
  if (!currentConversationId.value) {
    await handleNewChat()
  }
  
  const userMessage = inputMessage.value
  inputMessage.value = ''
  
  messages.value.push({
    id: Date.now(),
    role: 'user',
    content: userMessage,
    createdAt: new Date().toISOString()
  })
  scrollToBottom()
  
  loading.value = true
  try {
    const res = await chat({
      conversationId: currentConversationId.value,
      message: userMessage,
      model: selectedModel.value
    })
    
    if (res.data) {
      messages.value.push({
        id: res.data.messageId,
        role: 'assistant',
        content: res.data.content,
        createdAt: new Date().toISOString()
      })
      await loadConversations()
    }
    scrollToBottom()
  } catch (e) {
    ElMessage.error('发送失败')
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function handleExecuteAgent() {
  if (!selectedAgent.value || !agentInput.value.trim()) {
    ElMessage.warning('请选择 Agent 并输入任务')
    return
  }
  
  agentLoading.value = true
  try {
    const res = await executeAgent({
      agentType: selectedAgent.value,
      input: agentInput.value
    })
    
    messages.value.push({
      id: Date.now(),
      role: 'assistant',
      content: `[Agent: ${selectedAgent.value}]\n\n${res.data.result}`,
      createdAt: new Date().toISOString()
    })
    
    agentInput.value = ''
    scrollToBottom()
    ElMessage.success('Agent 执行完成')
  } catch (e) {
    ElMessage.error('执行失败')
  } finally {
    agentLoading.value = false
  }
}

async function handleCreateSkill() {
  try {
    await createSkill(skillForm)
    await loadSkills()
    showSkillDialog.value = false
    Object.assign(skillForm, { name: '', description: '', type: 'chat', config: '' })
    ElMessage.success('Skill 创建成功')
  } catch (e) {
    ElMessage.error('创建失败')
  }
}

async function handleToggleSkill(skill) {
  try {
    await updateSkill(skill.id, { enabled: skill.enabled })
  } catch (e) {
    ElMessage.error('更新失败')
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (messageListRef.value) {
      messageListRef.value.scrollTop = messageListRef.value.scrollHeight
    }
  })
}

function formatTime(time) {
  if (!time) return ''
  return new Date(time).toLocaleString('zh-CN')
}

function formatMessage(content) {
  if (!content) return ''
  return content.replace(/\n/g, '<br>')
}
</script>

<style scoped>
.ai-chat-container {
  height: calc(100vh - 60px);
  background: #f5f7fa;
}

.sidebar {
  background: #fff;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #e4e7ed;
}

.sidebar-header h3 {
  margin: 0;
  color: #303133;
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.conversation-item {
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
  transition: all 0.3s;
}

.conversation-item:hover {
  background: #f5f7fa;
}

.conversation-item.active {
  background: #ecf5ff;
  color: #409eff;
}

.conversation-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.delete-icon {
  opacity: 0;
  transition: opacity 0.3s;
}

.conversation-item:hover .delete-icon {
  opacity: 1;
}

.sidebar-footer {
  border-top: 1px solid #e4e7ed;
  padding: 15px;
  max-height: 250px;
}

.agent-list, .skill-list {
  padding: 10px 0;
}

.skill-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.chat-area {
  display: flex;
  flex-direction: column;
  padding: 0;
}

.chat-header {
  padding: 15px 20px;
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h4 {
  margin: 0;
  color: #303133;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.empty-state {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.message {
  display: flex;
  margin-bottom: 20px;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.message.user .message-avatar {
  background: #409eff;
  color: #fff;
}

.message.assistant .message-avatar {
  background: #67c23a;
  color: #fff;
}

.message-content {
  max-width: 70%;
  margin: 0 12px;
}

.message.user .message-content {
  align-items: flex-end;
}

.message-text {
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.6;
  word-break: break-word;
}

.message.user .message-text {
  background: #409eff;
  color: #fff;
}

.message.assistant .message-text {
  background: #fff;
  color: #303133;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.input-area {
  padding: 20px;
  background: #fff;
  border-top: 1px solid #e4e7ed;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.hint {
  font-size: 12px;
  color: #999;
}
</style>
