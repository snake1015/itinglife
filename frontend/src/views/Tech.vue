<template>
  <div class="tech-page">
    <div class="page-header">
      <h1 class="page-title">技术分享</h1>
      <p class="page-subtitle">分享编程经验、技术心得和项目实践</p>
    </div>

    <div class="content-wrapper">
      <div class="sidebar">
        <div class="filter-section">
          <h3>分类筛选</h3>
          <div class="filter-options">
            <button
              v-for="category in categories"
              :key="category.id"
              :class="[
                'filter-btn',
                { active: selectedCategory === category.id },
              ]"
              @click="selectCategory(category.id)"
            >
              {{ category.name }}
            </button>
          </div>
        </div>

        <div class="tag-section">
          <h3>标签云</h3>
          <div class="tag-cloud">
            <span
              v-for="tag in tagCloud"
              :key="tag"
              :class="['tag', { active: selectedTag === tag }]"
              @click="selectTag(tag)"
            >
              {{ tag }}
            </span>
          </div>
        </div>
      </div>

      <div class="main-content">
        <div class="articles-grid">
          <article
            v-for="article in filteredArticles"
            :key="article.id"
            class="article-card"
            @click="viewArticle(article)"
          >
            <div class="article-header">
              <span class="article-category">{{
                getCategoryName(article.category_id)
              }}</span>
              <span class="article-date">{{
                formatDate(article.created_at)
              }}</span>
            </div>
            <h3 class="article-title">{{ article.title }}</h3>
            <p class="article-excerpt">{{ article.summary }}</p>
            <div class="article-tags">
              <span v-for="tag in article.tags" :key="tag" class="article-tag">
                {{ tag }}
              </span>
            </div>
            <div class="article-meta">
              <span class="views">👁 {{ article.views || 0 }}</span>
              <span class="likes">❤ {{ article.likes || 0 }}</span>
            </div>
          </article>
        </div>

        <div v-if="filteredArticles.length === 0" class="empty-state">
          <div class="empty-icon">📝</div>
          <h3>暂无内容</h3>
          <p>当前筛选条件下暂无文章，请尝试其他分类或标签</p>
        </div>
      </div>
    </div>

    <!-- 文章详情弹窗 -->
    <div
      v-if="showArticleDetail"
      class="modal-overlay"
      @click="closeArticleDetail"
    >
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ selectedArticle.title }}</h2>
          <button class="close-btn" @click="closeArticleDetail">×</button>
        </div>
        <div class="modal-body">
          <div class="article-meta-info">
            <span class="meta-item"
              >分类：{{ getCategoryName(selectedArticle.category_id) }}</span
            >
            <span class="meta-item"
              >发布时间：{{ formatDate(selectedArticle.created_at) }}</span
            >
            <span class="meta-item"
              >浏览量：{{ selectedArticle.views || 0 }}</span
            >
          </div>
          <div class="article-content" v-html="selectedArticle.content"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { getApiUrl } from '../config.js'

export default {
  name: 'Tech',
  data() {
    return {
      articles: [],
      categories: [],
      selectedCategory: null,
      selectedTag: null,
      showArticleDetail: false,
      selectedArticle: {},
    }
  },
  computed: {
    tagCloud() {
      const tags = new Set()
      this.articles.forEach(article => {
        if (article.tags) {
          // 支持后端tags为字符串或数组
          let tagArr = Array.isArray(article.tags)
            ? article.tags
            : (article.tags ? article.tags.split(',').map(t => t.trim()).filter(Boolean) : [])
          tagArr.forEach(tag => tags.add(tag))
        }
      })
      return Array.from(tags)
    },
    filteredArticles() {
      let filtered = this.articles
      if (this.selectedCategory) {
        filtered = filtered.filter(
          article => article.category_id === this.selectedCategory
        )
      }
      if (this.selectedTag) {
        filtered = filtered.filter(article => {
          let tagArr = Array.isArray(article.tags)
            ? article.tags
            : (article.tags ? article.tags.split(',').map(t => t.trim()).filter(Boolean) : [])
          return tagArr.includes(this.selectedTag)
        })
      }
      return filtered
    },
  },
  methods: {
    fetchArticles() {
      axios.get(getApiUrl('/api/articles')).then(res => {
        this.articles = res.data
      })
    },
    fetchCategories() {
      axios.get(getApiUrl('/api/categories')).then(res => {
        this.categories = res.data
      })
    },
    selectCategory(categoryId) {
      this.selectedCategory =
        this.selectedCategory === categoryId ? null : categoryId
    },
    selectTag(tag) {
      this.selectedTag = this.selectedTag === tag ? null : tag
    },
    getCategoryName(categoryId) {
      const category = this.categories.find(c => c.id === categoryId)
      return category ? category.name : '未分类'
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN')
    },
    viewArticle(article) {
      this.selectedArticle = article
      this.showArticleDetail = true
    },
    closeArticleDetail() {
      this.showArticleDetail = false
      this.selectedArticle = {}
    },
  },
  mounted() {
    this.fetchArticles()
    this.fetchCategories()
  },
}
</script>

<style scoped>
.tech-page {
  min-height: 100vh;
}

.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 60px 20px;
  text-align: center;
}

.page-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 15px;
}

.page-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
}

.content-wrapper {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

.sidebar {
  background: white;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.filter-section,
.tag-section {
  margin-bottom: 30px;
}

.filter-section h3,
.tag-section h3 {
  font-size: 1.2rem;
  margin-bottom: 15px;
  color: #2c3e50;
}

.filter-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.filter-btn {
  padding: 10px 15px;
  border: none;
  background: #f8f9fa;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.filter-btn:hover {
  background: #e9ecef;
}

.filter-btn.active {
  background: #007bff;
  color: white;
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 5px 12px;
  background: #f8f9fa;
  border-radius: 15px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.tag:hover {
  background: #e9ecef;
}

.tag.active {
  background: #007bff;
  color: white;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 30px;
}

.article-card {
  background: white;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s ease;
}

.article-card:hover {
  transform: translateY(-5px);
}

.article-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.article-category {
  background: #007bff;
  color: white;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 0.8rem;
}

.article-date {
  color: #6c757d;
  font-size: 0.9rem;
}

.article-title {
  font-size: 1.3rem;
  margin-bottom: 15px;
  color: #2c3e50;
  line-height: 1.4;
}

.article-excerpt {
  color: #6c757d;
  line-height: 1.6;
  margin-bottom: 15px;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-bottom: 15px;
}

.article-tag {
  padding: 3px 8px;
  background: #f8f9fa;
  border-radius: 10px;
  font-size: 0.8rem;
  color: #6c757d;
}

.article-meta {
  display: flex;
  gap: 15px;
  color: #6c757d;
  font-size: 0.9rem;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #6c757d;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 10px;
  max-width: 800px;
  max-height: 80vh;
  overflow-y: auto;
  margin: 20px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h2 {
  margin: 0;
  color: #2c3e50;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6c757d;
}

.modal-body {
  padding: 30px;
}

.article-meta-info {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e9ecef;
  color: #6c757d;
  font-size: 0.9rem;
}

.article-content {
  line-height: 1.8;
  color: #2c3e50;
}

.article-content h2 {
  color: #2c3e50;
  margin-bottom: 15px;
}

.article-content p {
  margin-bottom: 15px;
}

@media (max-width: 768px) {
  .content-wrapper {
    grid-template-columns: 1fr;
  }

  .articles-grid {
    grid-template-columns: 1fr;
  }

  .page-title {
    font-size: 2rem;
  }
}
</style>
