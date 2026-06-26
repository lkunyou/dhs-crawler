<template>
  <el-container class="layout-container">
    <el-header class="main-header">
      <div class="header-left">
        <el-button class="mobile-menu-btn" text @click="mobileMenuVisible = true">
          <el-icon :size="20"><Menu /></el-icon>
        </el-button>
        <div class="logo">
          <el-icon :size="20"><DataBoard /></el-icon>
          <span>泰国汽配CRM</span>
        </div>
        <nav class="top-nav">
          <template v-for="item in menuItems" :key="item.path">
            <router-link 
              v-if="!item.children"
              :to="item.path"
              :class="['nav-item', { active: activeMenu === item.path }]"
            >
              <el-icon :size="16"><component :is="item.icon" /></el-icon>
              <span>{{ item.label }}</span>
            </router-link>
            <el-dropdown v-else @command="handleMenuCommand">
              <span :class="['nav-item', { active: isActiveParent(item) }]">
                <el-icon :size="16"><component :is="item.icon" /></el-icon>
                <span>{{ item.label }}</span>
                <el-icon :size="12"><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item 
                    v-for="child in item.children" 
                    :key="child.path" 
                    :command="child.path"
                    :class="{ active: activeMenu === child.path }"
                  >
                    <el-icon :size="14"><component :is="child.icon" /></el-icon>
                    <span>{{ child.label }}</span>
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
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

    <el-drawer v-model="mobileMenuVisible" title="菜单" direction="ltr" size="260px" :with-header="false">
      <div class="mobile-drawer-header">
        <div class="logo">
          <el-icon :size="20"><DataBoard /></el-icon>
          <span>泰国汽配CRM</span>
        </div>
      </div>
      <div class="mobile-menu">
        <template v-for="item in menuItems" :key="item.path">
          <div v-if="!item.children" 
               :class="['mobile-menu-item', { active: activeMenu === item.path }]"
               @click="handleMobileMenuClick(item.path)">
            <el-icon :size="18"><component :is="item.icon" /></el-icon>
            <span>{{ item.label }}</span>
          </div>
          <div v-else class="mobile-menu-group">
            <div class="mobile-menu-group-title" @click="toggleGroup(item.path)">
              <div class="mobile-menu-group-left">
                <el-icon :size="18"><component :is="item.icon" /></el-icon>
                <span>{{ item.label }}</span>
              </div>
              <el-icon :size="14" :class="['mobile-menu-arrow', { expanded: isGroupExpanded(item.path) }]"><ArrowDown /></el-icon>
            </div>
            <div v-show="isGroupExpanded(item.path)" class="mobile-menu-children">
              <div v-for="child in item.children" 
                   :key="child.path"
                   :class="['mobile-menu-item mobile-menu-subitem', { active: activeMenu === child.path }]"
                   @click="handleMobileMenuClick(child.path)">
                <el-icon :size="16"><component :is="child.icon" /></el-icon>
                <span>{{ child.label }}</span>
              </div>
            </div>
          </div>
        </template>
      </div>
    </el-drawer>
  </el-container>
</template>

<script setup>
import { computed, markRaw, ref } from 'vue'
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
  User,
  ArrowDown,
  Setting,
  Menu
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const mobileMenuVisible = ref(false)
const expandedGroups = ref(new Set())

const activeMenu = computed(() => route.path)

function handleMobileMenuClick(path) {
  mobileMenuVisible.value = false
  router.push(path)
}

function toggleGroup(path) {
  if (expandedGroups.value.has(path)) {
    expandedGroups.value.delete(path)
  } else {
    expandedGroups.value.add(path)
  }
}

function isGroupExpanded(path) {
  return expandedGroups.value.has(path)
}

const allMenuItems = [
  { 
    path: '/dashboard', 
    label: '数据看板', 
    icon: markRaw(DataBoard), 
    roles: ['admin', 'user', 'sales', 'operator'],
    children: [
      { path: '/dashboard', label: '数据看板', icon: markRaw(DataBoard), roles: ['admin', 'user', 'sales', 'operator'] },
      { path: '/analytics', label: '数据分析', icon: markRaw(TrendCharts), roles: ['admin', 'user', 'sales'] }
    ]
  },
  { 
    path: '/companies', 
    label: '客户管理', 
    icon: markRaw(UserFilled),
    roles: ['admin', 'user', 'sales'],
    children: [
      { path: '/companies', label: '客户列表', icon: markRaw(UserFilled), roles: ['admin', 'user', 'sales'] },
      { path: '/quotes', label: '报价管理', icon: markRaw(Document), roles: ['admin', 'user', 'sales'] },
      { path: '/products', label: '产品管理', icon: markRaw(Search), roles: ['admin', 'user', 'sales'] }
    ]
  },
  { 
    path: '/customer-search', 
    label: '客户搜索', 
    icon: markRaw(Search),
    roles: ['admin', 'operator'],
    children: [
      { path: '/customer-search', label: '搜索客户', icon: markRaw(Search), roles: ['admin', 'operator'] },
      { path: '/crawler', label: '爬虫管理', icon: markRaw(Search), roles: ['admin', 'operator'] }
    ]
  },
  { 
    path: '/email', 
    label: '邮件管理', 
    icon: markRaw(Message),
    roles: ['admin', 'user', 'sales'],
    children: [
      { path: '/inbox', label: '收件箱', icon: markRaw(MessageBox), roles: ['admin', 'user', 'sales'] },
      { path: '/email-campaign', label: '发送邮件', icon: markRaw(Document), roles: ['admin', 'user', 'sales'] },
      { path: '/email-marketing', label: '邮件营销', icon: markRaw(Message), roles: ['admin', 'user', 'sales'] },
      { path: '/email-templates', label: '邮件模板', icon: markRaw(Document), roles: ['admin', 'user', 'sales'] },
      { path: '/whatsapp', label: 'WhatsApp', icon: markRaw(ChatDotRound), roles: ['admin', 'user', 'sales'] }
    ]
  },
  { 
    path: '/system-config', 
    label: '系统配置', 
    icon: markRaw(Setting),
    roles: ['admin'],
    children: [
      { path: '/user-management', label: '用户管理', icon: markRaw(User), roles: ['admin'] },
      { path: '/system-config', label: '配置参数', icon: markRaw(Setting), roles: ['admin'] }
    ]
  }
]

// 根据用户角色过滤菜单
const menuItems = computed(() => {
  const userRole = userStore.role || 'user'
  
  const filterMenu = (items) => {
    return items
      .filter(item => item.roles.includes(userRole))
      .map(item => {
        if (item.children) {
          const filteredChildren = item.children.filter(child => child.roles.includes(userRole))
          if (filteredChildren.length === 0) return null
          return { ...item, children: filteredChildren }
        }
        return item
      })
      .filter(item => item !== null)
  }
  
  return filterMenu(allMenuItems)
})

function handleCommand(command) {
  if (command === 'logout') {
    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  }
}

function handleMenuCommand(command) {
  router.push(command)
}

function isActiveParent(item) {
  return item.children?.some(child => activeMenu.value === child.path)
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

.mobile-menu-btn {
  display: none;
  color: #64748b;
  padding: 6px;
}

.mobile-drawer-header {
  padding: 16px;
  border-bottom: 1px solid #e8f4f8;
  margin-bottom: 8px;
}

.mobile-menu {
  padding: 0 12px;
}

.mobile-menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 14px;
  color: #64748b;
  font-size: 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.mobile-menu-item:hover {
  color: #2563eb;
  background-color: #eff6ff;
}

.mobile-menu-item.active {
  color: #2563eb;
  background-color: #eff6ff;
  font-weight: 500;
}

.mobile-menu-group {
  margin-bottom: 8px;
}

.mobile-menu-group-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  color: #64748b;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.15s ease;
}

.mobile-menu-group-title:hover {
  background-color: #f8fafc;
}

.mobile-menu-group-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.mobile-menu-arrow {
  transition: transform 0.2s ease;
  color: #94a3b8;
}

.mobile-menu-arrow.expanded {
  transform: rotate(180deg);
}

.mobile-menu-children {
  overflow: hidden;
}

.mobile-menu-subitem {
  padding-left: 36px;
  font-size: 13px;
}

@media (max-width: 768px) {
  .mobile-menu-btn {
    display: inline-flex;
  }
  .top-nav {
    display: none;
  }
  .main-header {
    padding: 0 12px;
  }
  .header-left {
    gap: 12px;
  }
  .logo span {
    font-size: 13px;
  }
  .user-info span {
    display: none;
  }
}
</style>
