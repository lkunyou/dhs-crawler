import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/utils/request'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const username = ref(localStorage.getItem('username') || '')
  const role = ref(localStorage.getItem('role') || '')

  function isLoggedIn() {
    return !!token.value
  }

  async function login(user, pass) {
    try {
      localStorage.removeItem('token')
      const response = await api.post('/auth/login', {
        username: user,
        password: pass
      })
      token.value = response.data.token
      username.value = response.data.username
      role.value = response.data.role || 'user'
      localStorage.setItem('token', token.value)
      localStorage.setItem('username', username.value)
      localStorage.setItem('role', role.value)
      return response.data
    } catch (error) {
      if (error.response?.status === 401) {
        throw new Error('用户名或密码错误')
      }
      throw error
    }
  }

  function logout() {
    token.value = ''
    username.value = ''
    role.value = ''
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('role')
  }

  return {
    token,
    username,
    role,
    isLoggedIn,
    login,
    logout
  }
})