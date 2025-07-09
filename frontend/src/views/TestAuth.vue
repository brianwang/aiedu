<template>
  <div class="test-auth">
    <h1>认证测试页面</h1>
    <div class="auth-status">
      <p>认证状态: {{ isAuthenticated ? '已登录' : '未登录' }}</p>
      <p>用户信息: {{ user ? JSON.stringify(user, null, 2) : '无' }}</p>
    </div>
    
    <div class="actions">
      <button @click="testLogin" v-if="!isAuthenticated">测试登录</button>
      <button @click="testLogout" v-if="isAuthenticated">测试登出</button>
      <button @click="goHome">前往首页</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const user = computed(() => authStore.user)

const testLogin = () => {
  // 模拟登录
  authStore.setToken('test_token')
  authStore.setUser({ id: 1, username: 'test_user', role: 'student' })
}

const testLogout = () => {
  authStore.logoutUser()
}

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.test-auth {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
}

.auth-status {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
  margin: 20px 0;
}

.actions {
  display: flex;
  gap: 10px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  background: #007bff;
  color: white;
  cursor: pointer;
}

button:hover {
  background: #0056b3;
}
</style> 