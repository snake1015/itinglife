<template>
  <div class="login-container">
    <div class="login-background">
      <div class="login-card">
        <div class="login-header">
          <h1 class="login-title">itinglife</h1>
          <p class="login-subtitle">后台管理系统</p>
        </div>
        
        <el-tabs v-model="tab" class="login-tabs">
          <el-tab-pane label="登录" name="login">
            <el-form 
              :model="loginForm" 
              :rules="loginRules"
              ref="loginFormRef"
              @submit.prevent="login"
              class="login-form"
            >
              <el-form-item prop="username">
                <el-input 
                  v-model="loginForm.username" 
                  placeholder="请输入用户名"
                  prefix-icon="User"
                  size="large"
                />
              </el-form-item>
              <el-form-item prop="password">
                <el-input 
                  v-model="loginForm.password" 
                  type="password" 
                  placeholder="请输入密码"
                  prefix-icon="Lock"
                  size="large"
                  show-password
                />
              </el-form-item>
              <el-form-item>
                <el-button 
                  type="primary" 
                  @click="login" 
                  :loading="loginLoading"
                  size="large"
                  class="login-button"
                >
                  {{ loginLoading ? '登录中...' : '登录' }}
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          
          <el-tab-pane label="注册" name="register">
            <el-form 
              :model="registerForm" 
              :rules="registerRules"
              ref="registerFormRef"
              @submit.prevent="register"
              class="login-form"
            >
              <el-form-item prop="username">
                <el-input 
                  v-model="registerForm.username" 
                  placeholder="请输入用户名"
                  prefix-icon="User"
                  size="large"
                />
              </el-form-item>
              <el-form-item prop="email">
                <el-input 
                  v-model="registerForm.email" 
                  placeholder="请输入邮箱"
                  prefix-icon="Message"
                  size="large"
                />
              </el-form-item>
              <el-form-item prop="password">
                <el-input 
                  v-model="registerForm.password" 
                  type="password" 
                  placeholder="请输入密码"
                  prefix-icon="Lock"
                  size="large"
                  show-password
                />
              </el-form-item>
              <el-form-item prop="confirmPassword">
                <el-input 
                  v-model="registerForm.confirmPassword" 
                  type="password" 
                  placeholder="请确认密码"
                  prefix-icon="Lock"
                  size="large"
                  show-password
                />
              </el-form-item>
              <el-form-item>
                <el-button 
                  type="primary" 
                  @click="register" 
                  :loading="registerLoading"
                  size="large"
                  class="login-button"
                >
                  {{ registerLoading ? '注册中...' : '注册' }}
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>
        
        <div class="login-footer">
          <p class="footer-text">© 2024 itinglife. All rights reserved.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { getApiUrl } from '../config.js'

const tab = ref('login')
const loginFormRef = ref()
const registerFormRef = ref()
const loginLoading = ref(false)
const registerLoading = ref(false)

const loginForm = reactive({ 
  username: '', 
  password: '' 
})

const registerForm = reactive({ 
  username: '', 
  email: '', 
  password: '', 
  confirmPassword: '' 
})

const router = useRouter()

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
  ]
}

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

async function login() {
  try {
    await loginFormRef.value.validate()
    loginLoading.value = true
    
    const response = await axios.post(getApiUrl('/api/users/login'), {
      username: loginForm.username,
      password: loginForm.password
    })
    
    localStorage.setItem('user', JSON.stringify(response.data))
    localStorage.setItem('token', response.data.token || '')
    
    ElMessage.success('登录成功')
    router.push('/admin')
  } catch (error) {
    if (error.response) {
      ElMessage.error(error.response.data.detail || '用户名或密码错误')
    } else if (error.message) {
      ElMessage.error(error.message)
    } else {
      ElMessage.error('登录失败，请稍后重试')
    }
  } finally {
    loginLoading.value = false
  }
}

async function register() {
  try {
    await registerFormRef.value.validate()
    registerLoading.value = true
    
    await axios.post(getApiUrl('/api/users/register'), {
      username: registerForm.username,
      email: registerForm.email,
      password: registerForm.password
    })
    
    ElMessage.success('注册成功，请登录')
    tab.value = 'login'
    
    // 清空注册表单
    Object.assign(registerForm, {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })
  } catch (error) {
    if (error.response) {
      ElMessage.error(error.response.data.detail || '注册失败')
    } else {
      ElMessage.error('注册失败，请稍后重试')
    }
  } finally {
    registerLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-background {
  width: 100%;
  max-width: 450px;
}

.login-card {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #2c3e50;
  margin: 0 0 10px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.login-subtitle {
  color: #6c757d;
  font-size: 1.1rem;
  margin: 0;
}

.login-tabs {
  margin-bottom: 20px;
}

.login-tabs :deep(.el-tabs__header) {
  margin-bottom: 30px;
}

.login-tabs :deep(.el-tabs__item) {
  font-size: 1.1rem;
  font-weight: 500;
}

.login-form {
  margin-bottom: 20px;
}

.login-form :deep(.el-form-item) {
  margin-bottom: 20px;
}

.login-form :deep(.el-input__wrapper) {
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.login-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.login-button {
  width: 100%;
  border-radius: 10px;
  height: 50px;
  font-size: 1.1rem;
  font-weight: 500;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.login-footer {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #e9ecef;
}

.footer-text {
  color: #6c757d;
  font-size: 0.9rem;
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .login-card {
    padding: 30px 20px;
  }
  
  .login-title {
    font-size: 2rem;
  }
  
  .login-subtitle {
    font-size: 1rem;
  }
}
</style>
