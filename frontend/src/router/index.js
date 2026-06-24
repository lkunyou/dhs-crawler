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
        path: 'email-campaign',
        name: 'EmailCampaign',
        component: () => import('@/views/EmailCampaign.vue'),
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