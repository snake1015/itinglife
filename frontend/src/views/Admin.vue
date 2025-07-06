<template>
  <div class="admin-container">
    <!-- 顶部导航栏 -->
    <div class="admin-header">
      <div class="header-left">
        <h1 class="admin-title">itinglife 后台管理</h1>
      </div>
      <div class="header-right">
        <el-dropdown @command="handleCommand">
          <span class="user-info">
            <el-avatar :size="32">
              {{ currentUser?.username?.charAt(0)?.toUpperCase() }}
            </el-avatar>
            <span class="username">{{ currentUser?.username }}</span>
            <span>▼</span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="admin-content">
      <el-tabs v-model="activeTab" class="admin-tabs">
        <!-- 文章管理 -->
        <el-tab-pane label="文章管理" name="article">
          <el-button type="primary" @click="showEditor = true">新建文章</el-button>
          <el-table :data="articles" style="width: 100%" class="mt">
            <el-table-column prop="title" label="标题" />
            <el-table-column prop="category_id" label="分类" />
            <el-table-column prop="is_featured" label="精华" />
            <el-table-column label="操作">
              <template #default="scope">
                <el-button size="small" @click="editArticle(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" @click="deleteArticle(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <el-dialog v-model="showEditor" width="70%">
            <template #header>{{ editId ? '编辑文章' : '新建文章' }}</template>
            <el-input v-model="form.title" placeholder="标题" class="mb" />
            <el-select v-model="form.category_id" placeholder="分类" class="mb">
              <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
            </el-select>
            <el-checkbox v-model="form.is_featured">精华</el-checkbox>
            <MdEditor v-model="form.content" :height="400" :toolbars="toolbars" />
            <el-input v-model="form.tags" placeholder="标签（逗号分隔）" class="mb" />
            <el-button type="primary" @click="submitArticle">保存</el-button>
          </el-dialog>
        </el-tab-pane>
        
        <!-- 分类管理 -->
        <el-tab-pane label="分类管理" name="category">
          <el-input v-model="newCategory" placeholder="新分类名" class="mb" />
          <el-button type="primary" @click="addCategory">添加</el-button>
          <el-table :data="categories" style="width: 100%" class="mt">
            <el-table-column prop="name" label="分类名" />
            <el-table-column label="操作">
              <template #default="scope">
                <el-button size="small" type="danger" @click="deleteCategory(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        
        <!-- 用户管理 -->
        <el-tab-pane label="用户管理" name="user">
          <el-table :data="users" style="width: 100%" class="mt">
            <el-table-column prop="username" label="用户名" />
            <el-table-column prop="email" label="邮箱" />
          </el-table>
        </el-tab-pane>
        
        <!-- 统计分析 -->
        <el-tab-pane label="统计分析" name="stat">
          <div class="stat-cards">
            <el-card class="stat-card">
              <template #header>文章总数</template>
              <div class="stat-number">{{ articles.length }}</div>
            </el-card>
            <el-card class="stat-card">
              <template #header>分类总数</template>
              <div class="stat-number">{{ categories.length }}</div>
            </el-card>
            <el-card class="stat-card">
              <template #header>用户总数</template>
              <div class="stat-number">{{ users.length }}</div>
            </el-card>
            <el-card class="stat-card">
              <template #header>留言总数</template>
              <div class="stat-number">{{ messages.length }}</div>
            </el-card>
          </div>
        </el-tab-pane>
        
        <!-- 留言管理 -->
        <el-tab-pane label="留言管理" name="message">
          <el-table :data="messages" style="width: 100%" class="mt">
            <el-table-column prop="content" label="留言内容" />
            <el-table-column prop="user_id" label="用户ID" />
            <el-table-column prop="created_at" label="时间" />
            <el-table-column label="操作">
              <template #default="scope">
                <el-button size="small" type="danger" @click="deleteMessage(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        
        <!-- FAQ管理 -->
        <el-tab-pane label="FAQ管理" name="faq">
          <MdEditor v-model="faqContent" :height="300" :toolbars="toolbars" />
          <el-button type="primary" class="mt" @click="saveFAQ">保存FAQ</el-button>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { getApiUrl } from '../config.js'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const activeTab = ref('article')
const articles = ref([])
const categories = ref([])
const users = ref([])
const messages = ref([])
const showEditor = ref(false)
const editId = ref(null)
const newCategory = ref('')
const faqContent = ref('')

const form = ref({
  title: '',
  content: '',
  category_id: '',
  tags: '',
  is_featured: false,
})

const toolbars = [
  'bold', 'italic', 'strikethrough', '|',
  'title', 'quote', 'code', '|',
  'ul', 'ol', 'task', '|',
  'link', 'image', 'table', '|',
  'preview', 'fullscreen'
]

const currentUser = computed(() => {
  const userStr = localStorage.getItem('user')
  return userStr ? JSON.parse(userStr) : null
})

// 数据获取函数
function fetchArticles() {
  axios.get(getApiUrl('/api/articles')).then(res => {
    articles.value = res.data
  }).catch(err => {
    console.error('获取文章失败:', err)
    ElMessage.error('获取文章失败')
  })
}

function fetchCategories() {
  axios.get(getApiUrl('/api/categories')).then(res => {
    categories.value = res.data
  }).catch(err => {
    console.error('获取分类失败:', err)
    ElMessage.error('获取分类失败')
  })
}

function fetchUsers() {
  axios.get(getApiUrl('/api/users')).then(res => {
    users.value = res.data
  }).catch(err => {
    console.error('获取用户失败:', err)
    ElMessage.error('获取用户失败')
  })
}

function fetchMessages() {
  axios.get(getApiUrl('/api/messages')).then(res => {
    messages.value = res.data
  }).catch(err => {
    console.error('获取留言失败:', err)
    ElMessage.error('获取留言失败')
  })
}

// 文章相关功能
function editArticle(row) {
  editId.value = row.id
  form.value = { ...row }
  showEditor.value = true
}

function submitArticle() {
  if (editId.value) {
    axios.put(getApiUrl(`/api/articles/${editId.value}`), form.value).then(() => {
      showEditor.value = false
      editId.value = null
      form.value = { title: '', content: '', category_id: '', tags: '', is_featured: false }
      fetchArticles()
      ElMessage.success('文章更新成功')
    }).catch(err => {
      ElMessage.error('更新文章失败')
    })
  } else {
    axios.post(getApiUrl('/api/articles'), form.value).then(() => {
      showEditor.value = false
      form.value = { title: '', content: '', category_id: '', tags: '', is_featured: false }
      fetchArticles()
      ElMessage.success('文章创建成功')
    }).catch(err => {
      ElMessage.error('创建文章失败')
    })
  }
}

function deleteArticle(id) {
  ElMessageBox.confirm('确定要删除这篇文章吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    axios.delete(getApiUrl(`/api/articles/${id}`)).then(() => {
      fetchArticles()
      ElMessage.success('删除成功')
    }).catch(err => {
      ElMessage.error('删除失败')
    })
  })
}

// 分类相关功能
function addCategory() {
  if (!newCategory.value.trim()) {
    ElMessage.warning('请输入分类名')
    return
  }
  axios.post(getApiUrl('/api/categories'), { name: newCategory.value }).then(() => {
    newCategory.value = ''
    fetchCategories()
    ElMessage.success('分类添加成功')
  }).catch(err => {
    ElMessage.error('添加分类失败')
  })
}

function deleteCategory(id) {
  ElMessageBox.confirm('确定要删除这个分类吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    axios.delete(getApiUrl(`/api/categories/${id}`)).then(() => {
      fetchCategories()
      ElMessage.success('删除成功')
    }).catch(err => {
      ElMessage.error('删除失败')
    })
  })
}

// 留言相关功能
function deleteMessage(id) {
  ElMessageBox.confirm('确定要删除这条留言吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    axios.delete(getApiUrl(`/api/messages/${id}`)).then(() => {
      fetchMessages()
      ElMessage.success('删除成功')
    }).catch(err => {
      ElMessage.error('删除失败')
    })
  })
}

// FAQ相关功能
function fetchFAQ() {
  faqContent.value = `## 常见问题
- **Q:** 如何注册？
- **A:** 点击右上角注册按钮。

- **Q:** 如何发布文章？
- **A:** 登录后台管理，在文章管理模块中创建新文章。

- **Q:** 如何联系管理员？
- **A:** 可以通过留言板或联系页面与我们联系。
`
}

function saveFAQ() {
  ElMessage.success('FAQ已保存（模拟）')
}

// 用户相关功能
function handleCommand(command) {
  if (command === 'logout') {
    logout()
  }
}

function logout() {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    localStorage.removeItem('user')
    localStorage.removeItem('token')
    ElMessage.success('已退出登录')
    router.push('/login')
  }).catch(() => {
    // 用户取消
  })
}

onMounted(() => {
  // 检查登录状态
  if (!currentUser.value) {
    router.push('/login')
    return
  }
  
  fetchArticles()
  fetchCategories()
  fetchUsers()
  fetchMessages()
  fetchFAQ()
})
</script>

<style scoped>
.admin-container {
  min-height: 100vh;
  background: #f5f7fa;
}

.admin-header {
  background: white;
  padding: 0 24px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-left {
  display: flex;
  align-items: center;
}

.admin-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.user-info:hover {
  background-color: #f5f7fa;
}

.username {
  font-weight: 500;
  color: #2c3e50;
}

.admin-content {
  padding: 24px;
}

.admin-tabs {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.admin-tabs :deep(.el-tabs__header) {
  margin-bottom: 24px;
}

.admin-tabs :deep(.el-tabs__item) {
  font-weight: 500;
}

.mt {
  margin-top: 20px;
}

.mb {
  margin-bottom: 16px;
}

.stat-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #409eff;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .admin-header {
    padding: 0 16px;
  }
  
  .admin-title {
    font-size: 1.2rem;
  }
  
  .admin-content {
    padding: 16px;
  }
  
  .admin-tabs {
    padding: 16px;
  }
  
  .stat-cards {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style> 