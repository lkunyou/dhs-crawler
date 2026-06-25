<template>
  <el-container class="layout-container">
    <el-header class="main-header">
      <div class="header-left">
        <div class="logo">
          <el-icon :size="20"><DataBoard /></el-icon>
          <span>泰国汽配CRM</span>
        </div>
        <nav class="top-nav">
          <router-link 
            v-for="item in menuItems" 
            :key="item.path" 
            :to="item.path"
            :class="['nav-item', { active: activeMenu === item.path }]"
          >
            <el-icon :size="16"><component :is="item.icon" /></el-icon>
            <span>{{ item.label }}</span>
          </router-link>
        </nav>
      </div>
      <div class="header-right">
        <el-badge :value="12" class="badge">
          <el-icon :size="18"><Bell /></el-icon>
        </el-badge>
        <el-dropdown @command="handleCommand">
          <span class="user-info">
            <el-icon :size="16"><User /></el-icon>
            <span>{{ userStore.username || '管理员' }}</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="settings">个人设置</el-dropdown-item>
              <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>
    
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { computed, markRaw } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'
import { 
  DataBoard, 
  UserFilled, 
  MessageBox,
  Message, 
  Document, 
  ChatDotRound, 
  Search, 
  TrendCharts,
  Bell,
  User
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

const menuItems = [
  { path: '/dashboard', label: '数据看板', icon: markRaw(DataBoard) },
  { path: '/companies', label: '客户管理', icon: markRaw(UserFilled) },
  { path: '/inbox', label: '收件箱', icon: markRaw(MessageBox) },
  { path: '/email-campaign', label: '邮件营销', icon: markRaw(Message) },
  { path: '/email-templates', label: '邮件模板', icon: markRaw(Document) },
  { path: '/whatsapp', label: 'WhatsApp', icon: markRaw(ChatDotRound) },
  { path: '/crawler', label: '爬虫管理', icon: markRaw(Search) },
  { path: '/analytics', label: '数据分析', icon: markRaw(TrendCharts) }
]

function handleCommand(command) {
  if (command === 'logout') {
    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.main-header {
  background-color: #ffffff;
  height: 52px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e8f4f8;
}

.header-left {
  display: flex;
  align-items: center;
  flex: 1;
  gap: 24px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.logo span {
  color: #2563eb;
  font-size: 14px;
  font-weight: 600;
}

.logo :deep(.el-icon) {
  color: #2563eb;
}

.top-nav {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  color: #64748b;
  text-decoration: none;
  font-size: 13px;
  border-radius: 6px;
  transition: all 0.15s ease;
}

.nav-item:hover {
  color: #2563eb;
  background-color: #eff6ff;
}

.nav-item.active {
  color: #2563eb;
  background-color: #eff6ff;
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #64748b;
}

.badge {
  cursor: pointer;
  padding: 6px;
  border-radius: 6px;
  transition: background-color 0.15s ease;
}

.badge:hover {
  background-color: #f1f5f9;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 13px;
  color: #64748b;
  padding: 6px 10px;
  border-radius: 6px;
  transition: all 0.15s ease;
}

.user-info:hover {
  color: #2563eb;
  background-color: #eff6ff;
}

.el-main {
  padding: 0;
  background-color: #f8fafc;
}
</style>
