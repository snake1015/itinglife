<template>
  <div class="admin-container">
    <div class="admin-header">
      <h1>itinglife 后台管理</h1>
    </div>
    <div class="admin-content">
      <p>后台管理页面正在开发中...</p>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

// 检查登录状态
const currentUser = localStorage.getItem('user')
if (!currentUser) {
  router.push('/login')
}
</script>

<style scoped>
.admin-container {
  min-height: 100vh;
  background: #f5f7fa;
}

.admin-header {
  background: white;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.admin-content {
  padding: 20px;
}
</style> 