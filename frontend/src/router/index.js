import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录', requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/layout/MainLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: 'dashboard'
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '数据看板' }
      },
      {
        path: 'companies',
        name: 'Companies',
        component: () => import('@/views/CompanyList.vue'),
        meta: { title: '客户管理' }
      },
      {
        path: 'companies/:id',
        name: 'CompanyDetail',
        component: () => import('@/views/CompanyDetail.vue'),
        meta: { title: '客户详情' }
      },
      {
        path: 'quotes',
        name: 'Quotes',
        component: () => import('@/views/QuoteManagement.vue'),
        meta: { title: '报价管理' }
      },
      {
        path: 'products',
        name: 'Products',
        component: () => import('@/views/ProductManagement.vue'),
        meta: { title: '产品管理' }
      },
      {
        path: 'customer-search',
        name: 'CustomerSearch',
        component: () => import('@/views/CustomerSearch.vue'),
        meta: { title: '客户搜索' }
      },
      {
        path: 'inbox',
        name: 'Inbox',
        component: () => import('@/views/Inbox.vue'),
        meta: { title: '收件箱' }
      },
      {
        path: 'email-campaign',
        name: 'EmailCampaign',
        component: () => import('@/views/EmailCampaign.vue'),
        meta: { title: '发送邮件' }
      },
      {
        path: 'email-marketing',
        name: 'EmailMarketing',
        component: () => import('@/views/EmailMarketing.vue'),
        meta: { title: '邮件营销' }
      },
      {
        path: 'email-templates',
        name: 'EmailTemplates',
        component: () => import('@/views/EmailTemplates.vue'),
        meta: { title: '邮件模板' }
      },
      {
        path: 'whatsapp',
        name: 'WhatsApp',
        component: () => import('@/views/WhatsAppManager.vue'),
        meta: { title: 'WhatsApp管理' }
      },
      {
        path: 'crawler',
        name: 'Crawler',
        component: () => import('@/views/CrawlerManager.vue'),
        meta: { title: '爬虫管理' }
      },
      {
        path: 'analytics',
        name: 'Analytics',
        component: () => import('@/views/Analytics.vue'),
        meta: { title: '数据分析' }
      },
      {
        path: 'user-management',
        name: 'UserManagement',
        component: () => import('@/views/UserManagement.vue'),
        meta: { title: '用户管理' }
      },
      {
        path: 'system-config',
        name: 'SystemConfig',
        component: () => import('@/views/SystemConfig.vue'),
        meta: { title: '配置参数' }
      },
      {
        path: 'cmdt-query',
        name: 'CmdtQuery',
        component: () => import('@/views/CmdtQuery.vue'),
        meta: { title: 'CMDT编码查询' }
      },
      {
        path: 'ai-chat',
        name: 'AiChat',
        component: () => import('@/views/AiChat.vue'),
        meta: { title: 'AI 对话' }
      },
      {
        path: 'agent-management',
        name: 'AgentManagement',
        component: () => import('@/views/AgentManagement.vue'),
        meta: { title: 'Agent 管理' }
      },
      {
        path: 'mcp-management',
        name: 'McpManagement',
        component: () => import('@/views/McpManagement.vue'),
        meta: { title: 'MCP 管理' }
      },
      {
        path: 'ai-model-management',
        name: 'AiModelManagement',
        component: () => import('@/views/AiModelManagement.vue'),
        meta: { title: 'AI 模型配置' }
      },
      {
        path: 'ai-workflow-management',
        name: 'AiWorkflowManagement',
        component: () => import('@/views/AiWorkflowManagement.vue'),
        meta: { title: 'Agent 工作流' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const isLoggedIn = userStore.isLoggedIn()

  if (to.meta.requiresAuth !== false && !isLoggedIn) {
    next('/login')
    return
  }

  if (to.path === '/login' && isLoggedIn) {
    next('/dashboard')
    return
  }

  next()
})

router.afterEach((to) => {
  if (to.meta.title) {
    document.title = to.meta.title + ' - 泰国汽配CRM'
  }
})

export default router