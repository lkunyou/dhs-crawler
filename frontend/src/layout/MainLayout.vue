<template>
  <el-container class="layout-container">
    <el-header class="main-header">
      <div class="header-left">
        <div class="logo">
          <h2>🇹🇭 泰国汽配CRM</h2>
        </div>
        <el-menu
          :default-active="activeMenu"
          router
          mode="horizontal"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
          class="top-menu"
        >
          <el-menu-item index="/dashboard">
            <el-icon><DataBoard /></el-icon>
            <span>数据看板</span>
          </el-menu-item>
          <el-menu-item index="/companies">
            <el-icon><UserFilled /></el-icon>
            <span>客户管理</span>
          </el-menu-item>
          <el-menu-item index="/email-campaign">
            <el-icon><Message /></el-icon>
            <span>邮件营销</span>
          </el-menu-item>
          <el-menu-item index="/email-templates">
            <el-icon><Document /></el-icon>
            <span>邮件模板</span>
          </el-menu-item>
          <el-menu-item index="/whatsapp">
            <el-icon><ChatDotRound /></el-icon>
            <span>WhatsApp</span>
          </el-menu-item>
          <el-menu-item index="/crawler">
            <el-icon><Search /></el-icon>
            <span>爬虫管理</span>
          </el-menu-item>
          <el-menu-item index="/analytics">
            <el-icon><TrendCharts /></el-icon>
            <span>数据分析</span>
          </el-menu-item>
        </el-menu>
      </div>
      <div class="header-right">
        <el-badge :value="12" class="item">
          <el-icon :size="18"><Bell /></el-icon>
        </el-badge>
        <el-dropdown @command="handleCommand">
          <span class="user-info">
            <el-icon><User /></el-icon>
            {{ userStore.username || '管理员' }}
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
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)

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
  background-color: #304156;
  height: 40px;
  padding: 0 15px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.header-left {
  display: flex;
  align-items: center;
  flex: 1;
}

.logo {
  display: flex;
  align-items: center;
  margin-right: 15px;
  flex-shrink: 0;
}

.logo h2 {
  color: #fff;
  font-size: 12px;
  margin: 0;
  white-space: nowrap;
}

.top-menu {
  border-bottom: none !important;
  background-color: transparent !important;
}

:deep(.el-menu--horizontal) {
  border-bottom: none !important;
  height: 40px;
}

:deep(.el-menu--horizontal > .el-menu-item) {
  height: 40px !important;
  line-height: 40px !important;
  font-size: 12px;
  border-bottom: none !important;
  display: flex;
  align-items: center;
  margin: 0;
}

:deep(.el-menu--horizontal > .el-menu-item.is-active) {
  border-bottom: 2px solid #409EFF !important;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #bfcbd9;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
  font-size: 10px;
  color: #bfcbd9;
}

.el-main {
  padding: 0;
  background-color: #f0f2f5;
}
</style>
