<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="18">
        <div class="life-logs-section">
          <div class="flex-between">
            <el-date-picker
              v-model="selectedDate"
              type="date"
              placeholder="选择日期"
              @change="fetchLogs"
            />
            <el-button type="primary" @click="showEditor = true">新建日志</el-button>
          </div>
          <el-divider>生活日志</el-divider>
          <div class="posts-grid">
            <div
              class="post-card life-card"
              v-for="log in logs"
              :key="log.id"
              @click="viewLog(log)"
            >
              <div class="life-card-img-wrapper" v-if="getFirstImage(log.content)">
                <img :src="getFirstImage(log.content)" class="life-card-img" alt="封面" />
              </div>
              <div class="life-card-img-wrapper" v-else>
                <img src="https://placehold.co/600x300?text=No+Image" class="life-card-img" alt="无图" />
              </div>
              <div class="life-card-content">
                <div class="post-header">
                  <span class="post-date">{{ formatDate(log.created_at) }}</span>
                </div>
                <h3 class="post-title">{{ log.title }}</h3>
                <p class="post-excerpt">{{ log.summary }}</p>
              </div>
            </div>
          </div>
        </div>
        <el-dialog v-model="showEditor" width="70%">
          <template #header>{{ editId ? '编辑日志' : '新建日志' }}</template>
          <el-input v-model="form.title" placeholder="标题" class="mb" />
          <MdEditor
            v-model="form.content"
            :height="300"
            :toolbars="toolbars"
            @onUploadImg="handleUploadImage"
            @onPaste="handlePasteImage"
          />
          <el-input v-model="form.summary" placeholder="摘要" class="mb" />
          <el-progress v-if="uploading" :percentage="uploadPercent" status="success" class="mb" />
          <el-button type="primary" @click="submitLog">保存</el-button>
        </el-dialog>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div>多媒体展示：</div>
          <el-image
            v-for="img in mediaImages"
            :key="img"
            :src="img"
            style="width: 100px; height: 100px; margin: 4px"
            fit="cover"
          />
          <video
            v-for="vid in mediaVideos"
            :key="vid"
            :src="vid"
            style="width: 100px; height: 100px; margin: 4px"
            controls
          />
        </el-card>
        <el-card class="mt">
          <div>互动式地图（占位）</div>
        </el-card>
        <el-card class="mt">
          <div>互动形式（如故事投票/点赞/评论等占位）</div>
        </el-card>
      </el-col>
    </el-row>
    <el-dialog v-model="showDetail" width="60%">
      <template #header> {{ detail.title }} </template>
      <MdPreview :modelValue="detail.content || ''" />
      <el-divider>评论区</el-divider>
      <div v-for="c in comments" :key="c.id" class="comment">
        {{ c.content }}
      </div>
      <el-input v-model="newComment" placeholder="写下你的评论..." />
      <el-button type="primary" @click="submitComment">提交评论</el-button>
    </el-dialog>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { MdEditor, MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { getApiUrl } from '../config.js'

const logs = ref([])
const selectedDate = ref()
const showDetail = ref(false)
const showEditor = ref(false)
const editId = ref(null)
const detail = ref({})
const comments = ref([])
const newComment = ref('')
const form = ref({ title: '', content: '', summary: '' })
const mediaImages = ref([
  'https://placehold.co/100x100?text=Pic1',
  'https://placehold.co/100x100?text=Pic2',
])
const mediaVideos = ref(['https://www.w3schools.com/html/mov_bbb.mp4'])
const uploading = ref(false)
const uploadPercent = ref(0)

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
  'catalog',
]

function fetchLogs() {
  // 示例：可按日期筛选，实际应调用后端API
  axios
    .get(getApiUrl('/api/articles'), { params: { category_id: 2 } })
    .then(res => {
      logs.value = res.data
    })
}
function viewLog(log) {
  detail.value = log
  showDetail.value = true
  fetchComments(log.id)
}
function fetchComments(article_id) {
  axios
    .get(getApiUrl('/api/comments'), { params: { article_id } })
    .then(res => {
      comments.value = res.data
    })
}
function submitComment() {
  axios
    .post(getApiUrl('/api/comments'), {
      content: newComment.value,
      article_id: detail.value.id,
      user_id: 1, // TODO: 替换为当前登录用户
    })
    .then(() => {
      newComment.value = ''
      fetchComments(detail.value.id)
    })
}
function submitLog() {
  // category_id: 2 代表生活日志
  axios
    .post(getApiUrl('/api/articles'), {
      ...form.value,
      category_id: 2,
    })
    .then(() => {
      showEditor.value = false
      fetchLogs()
    })
}
function handleUploadImage(files, callback) {
  const file = files[0]
  const formData = new FormData()
  formData.append('file', file)
  uploading.value = true
  uploadPercent.value = 0
  axios
    .post(getApiUrl('/api/upload'), formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: e => {
        if (e.total) uploadPercent.value = Math.round((e.loaded / e.total) * 100)
      },
    })
    .then(res => {
      callback([res.data.url])
      uploading.value = false
      uploadPercent.value = 100
    })
    .catch(() => {
      uploading.value = false
      uploadPercent.value = 0
      window.$message?.error?.('图片上传失败')
    })
}
// 粘贴/拖拽图片上传
function handlePasteImage(e) {
  const items = (e.clipboardData || e.dataTransfer)?.items
  if (!items) return
  for (let i = 0; i < items.length; i++) {
    const item = items[i]
    if (item.kind === 'file' && item.type.startsWith('image/')) {
      const file = item.getAsFile()
      handleUploadImage([file], urls => {
        // 自动插入Markdown图片
        form.value.content += `\n![](${urls[0]})\n`
      })
      e.preventDefault()
      break
    }
  }
}
// 提取首张图片（支持markdown图片语法和html img标签）
function getFirstImage(content) {
  if (!content) return ''
  // markdown ![alt](url)
  const mdImg = content.match(/!\[[^\]]*\]\(([^)]+)\)/)
  if (mdImg) return mdImg[1]
  // html <img src="...">
  const htmlImg = content.match(/<img[^>]+src=["']([^"']+)["']/)
  if (htmlImg) return htmlImg[1]
  return ''
}
function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('zh-CN')
}
onMounted(() => {
  fetchLogs()
})
</script>
<style scoped>
.life-logs-section {
  margin-bottom: 32px;
}
.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
}
.post-card.life-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: transform 0.3s ease;
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 320px;
}
.post-card.life-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 32px rgba(102,126,234,0.10);
}
.life-card-img-wrapper {
  width: 100%;
  height: 180px;
  overflow: hidden;
  background: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
}
.life-card-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.life-card-content {
  padding: 22px 24px 18px 24px;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.post-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 10px;
}
.post-date {
  color: #6c757d;
  font-size: 0.9rem;
}
.post-title {
  font-size: 1.3rem;
  margin-bottom: 12px;
  color: #2c3e50;
  line-height: 1.4;
}
.post-excerpt {
  color: #6c757d;
  line-height: 1.6;
  margin-bottom: 0;
  flex: 1;
}
.mt {
  margin-top: 20px;
}
.mb {
  margin-bottom: 16px;
}
.flex-between {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.comment {
  margin: 8px 0;
  padding: 8px;
  background: #f5f5f5;
  border-radius: 4px;
}
@media (max-width: 768px) {
  .posts-grid {
    grid-template-columns: 1fr;
    gap: 18px;
  }
  .life-card-img-wrapper {
    height: 140px;
  }
  .life-card-content {
    padding: 14px 10px 10px 10px;
  }
  .post-title {
    font-size: 1.1rem;
  }
}
.life-card-img, .md-editor-preview img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0 auto;
}
</style>
