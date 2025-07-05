<template>
  <div class="login-container">
    <el-card class="login-card">
      <el-tabs v-model="tab">
        <el-tab-pane label="登录" name="login">
          <el-form :model="loginForm" @submit.prevent="login">
            <el-form-item label="用户名">
              <el-input v-model="loginForm.username" />
            </el-form-item>
            <el-form-item label="密码">
              <el-input v-model="loginForm.password" type="password" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="login">登录</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="注册" name="register">
          <el-form :model="registerForm" @submit.prevent="register">
            <el-form-item label="用户名">
              <el-input v-model="registerForm.username" />
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="registerForm.email" />
            </el-form-item>
            <el-form-item label="密码">
              <el-input v-model="registerForm.password" type="password" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="register">注册</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
const tab = ref('login')
const loginForm = ref({ username: '', password: '' })
const registerForm = ref({ username: '', email: '', password: '' })
const router = useRouter()

function login() {
  if (!loginForm.value.username || !loginForm.value.password) {
    ElMessage.error('请填写用户名和密码')
    return
  }
  axios
    .post('http://localhost:8000/api/users/login', loginForm.value)
    .then(res => {
      localStorage.setItem('user', JSON.stringify(res.data))
      ElMessage.success('登录成功')
      router.push('/')
    })
    .catch(() => {
      ElMessage.error('用户名或密码错误')
    })
}
function register() {
  if (
    !registerForm.value.username ||
    !registerForm.value.email ||
    !registerForm.value.password
  ) {
    ElMessage.error('请填写完整信息')
    return
  }
  axios
    .post('http://localhost:8000/api/users/register', registerForm.value)
    .then(() => {
      ElMessage.success('注册成功，请登录')
      tab.value = 'login'
    })
    .catch(() => {
      ElMessage.error('注册失败，用户名或邮箱已存在')
    })
}
</script>
<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}
.login-card {
  width: 400px;
}
</style>
