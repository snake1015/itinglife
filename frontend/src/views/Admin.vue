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
            <el-avatar :size="32" :src="userAvatar">
              {{ currentUser?.username?.charAt(0)?.toUpperCase() }}
            </el-avatar>
            <span class="username">{{ currentUser?.username }}</span>
            <el-icon><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人资料</el-dropdown-item>
              <el-dropdown-item command="settings">设置</el-dropdown-item>
              <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="admin-content">
      <el-tabs v-model="activeTab" class="admin-tabs">
      <el-tab-pane label="文章管理" name="article">
        <el-button type="primary" @click="showEditor = true"
          >新建文章</el-button
        >
        <el-table :data="articles" style="width: 100%" class="mt">
          <el-table-column prop="title" label="标题" />
          <el-table-column prop="category_id" label="分类" />
          <el-table-column prop="is_featured" label="精华" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button size="small" @click="editArticle(scope.row)"
                >编辑</el-button
              >
              <el-button
                size="small"
                type="danger"
                @click="deleteArticle(scope.row.id)"
                >删除</el-button
              >
            </template>
          </el-table-column>
        </el-table>
        <el-dialog v-model="showEditor" width="70%">
          <template #header>{{ editId ? '编辑文章' : '新建文章' }}</template>
          <el-input v-model="form.title" placeholder="标题" class="mb" />
          <el-select v-model="form.category_id" placeholder="分类" class="mb">
            <el-option
              v-for="cat in categories"
              :key="cat.id"
              :label="cat.name"
              :value="cat.id"
            />
          </el-select>
          <el-checkbox v-model="form.is_featured">精华</el-checkbox>
          <MdEditor
            v-model="form.content"
            :height="400"
            :toolbars="toolbars"
          />
          <el-input
            v-model="form.tags"
            placeholder="标签（逗号分隔）"
            class="mb"
          />
          <el-button type="primary" @click="submitArticle">保存</el-button>
        </el-dialog>
      </el-tab-pane>
      <el-tab-pane label="分类管理" name="category">
        <el-input v-model="newCategory" placeholder="新分类名" class="mb" />
        <el-button type="primary" @click="addCategory">添加</el-button>
        <el-table :data="categories" style="width: 100%" class="mt">
          <el-table-column prop="name" label="分类名" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button
                size="small"
                type="danger"
                @click="deleteCategory(scope.row.id)"
                >删除</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="用户管理" name="user">
        <el-table :data="users" style="width: 100%" class="mt">
          <el-table-column prop="username" label="用户名" />
          <el-table-column prop="email" label="邮箱" />
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="统计分析" name="stat">
        <div>统计分析（占位）</div>
      </el-tab-pane>
      <el-tab-pane label="设置" name="setting">
        <div>设置（占位）</div>
      </el-tab-pane>
      <el-tab-pane label="留言管理" name="message">
        <el-table :data="messages" style="width: 100%" class="mt">
          <el-table-column prop="content" label="留言内容" />
          <el-table-column prop="user_id" label="用户ID" />
          <el-table-column prop="created_at" label="时间" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button
                size="small"
                type="danger"
                @click="deleteMessage(scope.row.id)"
                >删除</el-button
              >
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
      <el-tab-pane label="FAQ管理" name="faq">
        <MdEditor v-model="faqContent" :height="300" :toolbars="toolbars" />
        <el-button type="primary" class="mt" @click="saveFAQ"
          >保存FAQ</el-button
        >
      </el-tab-pane>
      <el-tab-pane label="轮播图管理" name="banner">
        <el-upload
          :action="getApiUrl('/api/upload')"
          :on-success="handleBannerUpload"
          :show-file-list="false"
        >
          <el-button type="primary">上传新图片</el-button>
        </el-upload>
        <el-table :data="banners" style="width: 100%" class="mt">
          <el-table-column prop="img" label="图片">
            <template #default="scope">
              <img
                :src="scope.row.img"
                style="width: 120px; height: 40px; object-fit: cover"
              />
            </template>
          </el-table-column>
          <el-table-column prop="link" label="跳转链接" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button size="small" @click="editBanner(scope.row)"
                >编辑</el-button
              >
              <el-button
                size="small"
                type="danger"
                @click="deleteBanner(scope.row.id)"
                >删除</el-button
              >
            </template>
          </el-table-column>
        </el-table>
        <el-dialog v-model="showBannerEditor" width="400px">
          <template #header>编辑轮播图</template>
          <el-input v-model="bannerForm.img" placeholder="图片URL" class="mb" />
          <el-input
            v-model="bannerForm.link"
            placeholder="跳转链接（可选）"
            class="mb"
          />
          <el-button type="primary" @click="saveBanner">保存</el-button>
        </el-dialog>
      </el-tab-pane>
    </el-tabs>
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
import { ArrowDown } from '@element-plus/icons-vue'

const activeTab = ref('article')
const articles = ref([])
const categories = ref([])
const users = ref([])
const showEditor = ref(false)
const editId = ref(null)
const form = ref({
  title: '',
  content: '',
  category_id: '',
  tags: '',
  is_featured: false,
})
const newCategory = ref('')
const messages = ref([])
const faqContent = ref('')
const banners = ref([])
const showBannerEditor = ref(false)
const bannerForm = ref({ id: null, img: '', link: '' })
const router = useRouter()

// 用户信息
const currentUser = computed(() => {
  const userStr = localStorage.getItem('user')
  return userStr ? JSON.parse(userStr) : null
})

const userAvatar = ref('')

// md-editor-v3 工具栏配置
const toolbars = [
  'bold',
  'underline',
  'italic',
  'strikethrough',
  'title',
  'sub',
  'sup',
  'quote',
  'unordered-list',
  'ordered-list',
  'task-list',
  '-',
  'code',
  'code-block',
  'link',
  'image',
  'table',
  'mermaid',
  'katex',
  '-',
  'preview',
  'fullscreen',
  'page-break',
  'catalog'
]

function fetchArticles() {
  axios.get(getApiUrl('/api/articles')).then(res => {
    articles.value = res.data
  })
}
function fetchCategories() {
  axios.get(getApiUrl('/api/categories')).then(res => {
    categories.value = res.data
  })
}
function fetchUsers() {
  axios.get(getApiUrl('/api/users')).then(res => {
    users.value = res.data
  })
}
function fetchMessages() {
  axios.get(getApiUrl('/api/messages')).then(res => {
    messages.value = res.data
  })
}
function fetchBanners() {
  axios.get(getApiUrl('/api/banners')).then(res => {
    banners.value = res.data
  })
}
function editArticle(row) {
  editId.value = row.id
  form.value = { ...row }
  showEditor.value = true
}
function submitArticle() {
  if (editId.value) {
    axios
      .put(getApiUrl(`/api/articles/${editId.value}`), form.value)
      .then(() => {
        showEditor.value = false
        fetchArticles()
      })
  } else {
    axios.post(getApiUrl('/api/articles'), form.value).then(() => {
      showEditor.value = false
      fetchArticles()
    })
  }
}
function deleteArticle(id) {
  axios.delete(getApiUrl(`/api/articles/${id}`)).then(() => {
    fetchArticles()
  })
}
function addCategory() {
  axios
    .post(getApiUrl('/api/categories'), { name: newCategory.value })
    .then(() => {
      newCategory.value = ''
      fetchCategories()
    })
}
function deleteCategory(id) {
  axios.delete(getApiUrl(`/api/categories/${id}`)).then(() => {
    fetchCategories()
  })
}
function deleteMessage(id) {
  axios.delete(getApiUrl(`/api/messages/${id}`)).then(() => {
    fetchMessages()
  })
}
function fetchFAQ() {
  // 示例：可从后端获取FAQ markdown
  faqContent.value = `
## 常见问题
- **Q:** 如何注册？
- **A:** 点击右上角注册按钮。
`
}
function saveFAQ() {
  // 示例：可用axios.post('/api/faq', { content: faqContent.value })
  alert('FAQ已保存（模拟）')
}
function handleBannerUpload(res) {
  bannerForm.value.img = res.url
  showBannerEditor.value = true
}
function editBanner(row) {
  bannerForm.value = { ...row }
  showBannerEditor.value = true
}
function saveBanner() {
  if (bannerForm.value.id) {
    axios
      .put(
        getApiUrl(`/api/banners/${bannerForm.value.id}`),
        bannerForm.value
      )
      .then(() => {
        showBannerEditor.value = false
        bannerForm.value = { id: null, img: '', link: '' }
        fetchBanners()
      })
  } else {
    axios
      .post(getApiUrl('/api/banners'), bannerForm.value)
      .then(() => {
        showBannerEditor.value = false
        bannerForm.value = { id: null, img: '', link: '' }
        fetchBanners()
      })
  }
}
function deleteBanner(id) {
  axios.delete(getApiUrl(`/api/banners/${id}`)).then(() => {
    fetchBanners()
  })
}

// 用户相关功能
function handleCommand(command) {
  switch (command) {
    case 'profile':
      ElMessage.info('个人资料功能开发中...')
      break
    case 'settings':
      ElMessage.info('设置功能开发中...')
      break
    case 'logout':
      logout()
      break
  }
}

function logout() {
  ElMessageBox.confirm(
    '确定要退出登录吗？',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
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
  fetchBanners()
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
}
</style>
