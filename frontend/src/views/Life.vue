<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="18">
        <el-card>
          <div class="flex-between">
            <el-date-picker
              v-model="selectedDate"
              type="date"
              placeholder="选择日期"
              @change="fetchLogs"
            />
            <el-button type="primary" @click="showEditor = true"
              >新建日志</el-button
            >
          </div>
          <el-divider>生活日志</el-divider>
          <el-list>
            <el-list-item
              v-for="log in logs"
              :key="log.id"
              @click="viewLog(log)"
            >
              <div class="title">{{ log.title }}</div>
              <div class="summary">{{ log.summary }}</div>
              <div class="meta">{{ log.created_at }}</div>
            </el-list-item>
          </el-list>
        </el-card>
        <el-dialog v-model="showEditor" width="70%">
          <template #header>{{ editId ? '编辑日志' : '新建日志' }}</template>
          <el-input v-model="form.title" placeholder="标题" class="mb" />
          <MdEditor
            v-model="form.content"
            :height="300"
            :toolbars="toolbars"
            @onUploadImg="handleUploadImage"
          />
          <el-input v-model="form.summary" placeholder="摘要" class="mb" />
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

function fetchLogs() {
  // 示例：可按日期筛选，实际应调用后端API
  axios
    .get('http://localhost:8000/api/articles', { params: { category_id: 2 } })
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
    .get('http://localhost:8000/api/comments', { params: { article_id } })
    .then(res => {
      comments.value = res.data
    })
}
function submitComment() {
  axios
    .post('http://localhost:8000/api/comments', {
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
    .post('http://localhost:8000/api/articles', {
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
  axios
    .post('http://localhost:8000/api/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    .then(res => {
      callback([res.data.url])
    })
}
onMounted(() => {
  fetchLogs()
})
</script>
<style scoped>
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
.title {
  font-weight: bold;
  font-size: 18px;
}
.summary {
  color: #888;
}
.meta {
  font-size: 12px;
  color: #aaa;
}
.comment {
  margin: 8px 0;
  padding: 8px;
  background: #f5f5f5;
  border-radius: 4px;
}
</style>
