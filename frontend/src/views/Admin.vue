<template>
  <div>
    <el-tabs v-model="activeTab">
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
          <v-md-editor
            v-model="form.content"
            height="400px"
            :autofocus="true"
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
        <v-md-editor v-model="faqContent" height="300px" />
        <el-button type="primary" class="mt" @click="saveFAQ"
          >保存FAQ</el-button
        >
      </el-tab-pane>
      <el-tab-pane label="轮播图管理" name="banner">
        <el-upload
          action="http://localhost:8000/api/upload"
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
import { ref, onMounted } from 'vue'
import axios from 'axios'
import VMdEditor from '@kangc/v-md-editor'
import githubTheme from '@kangc/v-md-editor-theme-github'
import '@kangc/v-md-editor/lib/style/base-editor.css'
import '@kangc/v-md-editor-theme-github/lib/theme.css'
VMdEditor.use(githubTheme)

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

function fetchArticles() {
  axios.get('http://localhost:8000/api/articles').then(res => {
    articles.value = res.data
  })
}
function fetchCategories() {
  axios.get('http://localhost:8000/api/categories').then(res => {
    categories.value = res.data
  })
}
function fetchUsers() {
  axios.get('http://localhost:8000/api/users').then(res => {
    users.value = res.data
  })
}
function fetchMessages() {
  axios.get('http://localhost:8000/api/messages').then(res => {
    messages.value = res.data
  })
}
function fetchBanners() {
  axios.get('http://localhost:8000/api/banners').then(res => {
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
      .put(`http://localhost:8000/api/articles/${editId.value}`, form.value)
      .then(() => {
        showEditor.value = false
        fetchArticles()
      })
  } else {
    axios.post('http://localhost:8000/api/articles', form.value).then(() => {
      showEditor.value = false
      fetchArticles()
    })
  }
}
function deleteArticle(id) {
  axios.delete(`http://localhost:8000/api/articles/${id}`).then(() => {
    fetchArticles()
  })
}
function addCategory() {
  axios
    .post('http://localhost:8000/api/categories', { name: newCategory.value })
    .then(() => {
      newCategory.value = ''
      fetchCategories()
    })
}
function deleteCategory(id) {
  axios.delete(`http://localhost:8000/api/categories/${id}`).then(() => {
    fetchCategories()
  })
}
function deleteMessage(id) {
  axios.delete(`http://localhost:8000/api/messages/${id}`).then(() => {
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
        `http://localhost:8000/api/banners/${bannerForm.value.id}`,
        bannerForm.value
      )
      .then(() => {
        showBannerEditor.value = false
        bannerForm.value = { id: null, img: '', link: '' }
        fetchBanners()
      })
  } else {
    axios
      .post('http://localhost:8000/api/banners', bannerForm.value)
      .then(() => {
        showBannerEditor.value = false
        bannerForm.value = { id: null, img: '', link: '' }
        fetchBanners()
      })
  }
}
function deleteBanner(id) {
  axios.delete(`http://localhost:8000/api/banners/${id}`).then(() => {
    fetchBanners()
  })
}
onMounted(() => {
  fetchArticles()
  fetchCategories()
  fetchUsers()
  fetchMessages()
  fetchFAQ()
  fetchBanners()
})
</script>
<style scoped>
.mt {
  margin-top: 20px;
}
.mb {
  margin-bottom: 16px;
}
</style>
