<template>
  <div class="admin-test">
    <h1>后台管理测试页面</h1>
    <p>当前用户: {{ currentUser?.username || '未登录' }}</p>
    <el-button @click="logout">退出登录</el-button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

const currentUser = computed(() => {
  const userStr = localStorage.getItem('user')
  return userStr ? JSON.parse(userStr) : null
})

function logout() {
  localStorage.removeItem('user')
  localStorage.removeItem('token')
  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>

<style scoped>
.admin-test {
  padding: 20px;
  text-align: center;
}
</style> 