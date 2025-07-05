<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="18">
        <el-card>
          <div class="flex-between">
            <el-select v-model="selectedCategory" placeholder="选择分类" @change="fetchArticles">
              <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
            </el-select>
            <el-input v-model="searchTag" placeholder="标签搜索" style="width:200px" @change="fetchArticles" />
          </div>
          <el-tag v-for="tag in tagCloud" :key="tag" class="tag" @click="handleTagClick(tag)">{{ tag }}</el-tag>
          <el-divider>文章列表</el-divider>
          <el-list>
            <el-list-item v-for="a in articles" :key="a.id" @click="viewArticle(a.id)">
              <div class="title">{{ a.title }} <el-tag v-if="a.is_featured" type="success">精华</el-tag></div>
              <div class="summary">{{ a.summary }}</div>
              <div class="meta">分类: {{ getCategoryName(a.category_id) }} | 标签: {{ a.tags }}</div>
            </el-list-item>
          </el-list>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div>标签云：</div>
          <el-tag v-for="tag in tagCloud" :key="tag" class="tag" @click="handleTagClick(tag)">{{ tag }}</el-tag>
        </el-card>
        <el-card class="mt">
          <div>精华文章：</div>
          <ul>
            <li v-for="a in featured" :key="a.id" @click="viewArticle(a.id)">{{ a.title }}</li>
          </ul>
        </el-card>
      </el-col>
    </el-row>
    <el-dialog v-model="showDetail" width="60%">
      <template #header> {{ detail.title }} </template>
      <v-md-preview :text="detail.content || ''" />
      <el-divider>评论区</el-divider>
      <div v-for="c in comments" :key="c.id" class="comment">{{ c.content }}</div>
      <el-input v-model="newComment" placeholder="写下你的评论..." />
      <el-button type="primary" @click="submitComment">提交评论</el-button>
    </el-dialog>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import githubTheme from '@kangc/v-md-editor-theme-github';
import '@kangc/v-md-editor/lib/style/preview.css';
import '@kangc/v-md-editor-theme-github/lib/theme.css';
VMdPreview.use(githubTheme);

const articles = ref([]);
const categories = ref([]);
const tagCloud = ref([]);
const featured = ref([]);
const selectedCategory = ref();
const searchTag = ref('');
const showDetail = ref(false);
const detail = ref({});
const comments = ref([]);
const newComment = ref('');

function getCategoryName(id) {
  const cat = categories.value.find(c => c.id === id);
  return cat ? cat.name : '';
}

function fetchArticles() {
  axios.get('http://localhost:8000/api/articles', {
    params: {
      category_id: selectedCategory.value,
      tag: searchTag.value
    }
  }).then(res => {
    articles.value = res.data;
    // 生成标签云
    const tags = new Set();
    res.data.forEach(a => a.tags && a.tags.split(',').forEach(t => tags.add(t.trim())));
    tagCloud.value = Array.from(tags);
  });
}
function fetchCategories() {
  axios.get('http://localhost:8000/api/categories').then(res => {
    categories.value = res.data;
  });
}
function fetchFeatured() {
  axios.get('http://localhost:8000/api/articles', { params: { is_featured: true } }).then(res => {
    featured.value = res.data;
  });
}
function viewArticle(id) {
  axios.get(`http://localhost:8000/api/articles/${id}`).then(res => {
    detail.value = res.data;
    showDetail.value = true;
    fetchComments(id);
  });
}
function fetchComments(article_id) {
  axios.get('http://localhost:8000/api/comments', { params: { article_id } }).then(res => {
    comments.value = res.data;
  });
}
function handleTagClick(tag) {
  searchTag.value = tag;
  fetchArticles();
}

function submitComment() {
  axios.post('http://localhost:8000/api/comments', {
    content: newComment.value,
    article_id: detail.value.id,
    user_id: 1 // TODO: 替换为当前登录用户
  }).then(() => {
    newComment.value = '';
    fetchComments(detail.value.id);
  });
}
onMounted(() => {
  fetchCategories();
  fetchArticles();
  fetchFeatured();
});
</script>
<style scoped>
.mt { margin-top: 20px; }
.flex-between { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.tag { margin: 0 4px 4px 0; cursor: pointer; }
.title { font-weight: bold; font-size: 18px; }
.summary { color: #888; }
.meta { font-size: 12px; color: #aaa; }
.comment { margin: 8px 0; padding: 8px; background: #f5f5f5; border-radius: 4px; }
</style> 