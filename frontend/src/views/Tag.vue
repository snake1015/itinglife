<template>
  <div class="tag-page">
    <div class="page-header">
      <h1 class="page-title">标签</h1>
      <p class="page-subtitle">所有标签与相关文章</p>
    </div>
    <div class="tag-cloud">
      <span
        v-for="tag in tags"
        :key="tag"
        :class="['tag', { active: tag === selectedTag }]"
        @click="selectTag(tag)"
      >
        {{ tag }}
      </span>
    </div>
    <div v-if="selectedTag" class="tag-articles">
      <h2 class="tag-articles-title">“{{ selectedTag }}” 相关文章</h2>
      <div class="articles-grid">
        <article
          v-for="article in filteredArticles"
          :key="article.id"
          class="article-card"
        >
          <div class="article-header">
            <span class="article-category">{{ getCategoryName(article.category_id) }}</span>
            <span class="article-date">{{ formatDate(article.created_at) }}</span>
          </div>
          <h3 class="article-title">{{ article.title }}</h3>
          <p class="article-excerpt">{{ article.summary }}</p>
        </article>
      </div>
    </div>
    <div v-else class="empty-state">
      <div class="empty-icon">🏷️</div>
      <h3>请选择标签查看相关文章</h3>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
import { getApiUrl } from '../config.js'
export default {
  name: 'Tag',
  data() {
    return {
      articles: [],
      categories: [],
      tags: [],
      selectedTag: null,
    }
  },
  computed: {
    filteredArticles() {
      if (!this.selectedTag) return []
      return this.articles.filter(article => {
        let tagArr = Array.isArray(article.tags)
          ? article.tags
          : (article.tags ? article.tags.split(',').map(t => t.trim()).filter(Boolean) : [])
        return tagArr.includes(this.selectedTag)
      })
    },
  },
  methods: {
    fetchArticles() {
      axios.get(getApiUrl('/api/articles')).then(res => {
        this.articles = res.data
        this.extractTags()
      })
    },
    fetchCategories() {
      axios.get(getApiUrl('/api/categories')).then(res => {
        this.categories = res.data
      })
    },
    extractTags() {
      const tags = new Set()
      this.articles.forEach(article => {
        if (article.tags) {
          let tagArr = Array.isArray(article.tags)
            ? article.tags
            : (article.tags ? article.tags.split(',').map(t => t.trim()).filter(Boolean) : [])
          tagArr.forEach(tag => tags.add(tag))
        }
      })
      this.tags = Array.from(tags)
    },
    selectTag(tag) {
      this.selectedTag = tag
    },
    getCategoryName(categoryId) {
      const category = this.categories.find(c => c.id === categoryId)
      return category ? category.name : '未分类'
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN')
    },
  },
  mounted() {
    this.fetchArticles()
    this.fetchCategories()
  },
}
</script>
<style scoped>
.tag-page {
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
.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
  margin: 40px 0 30px 0;
}
.tag {
  padding: 8px 22px;
  background: #f8f9fa;
  border-radius: 20px;
  font-size: 1.1rem;
  color: #764ba2;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  border: 1.5px solid #e1e5e9;
}
.tag.active, .tag:hover {
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border: 1.5px solid #764ba2;
}
.tag-articles-title {
  text-align: center;
  font-size: 1.4rem;
  margin: 30px 0 20px 0;
  color: #2c3e50;
}
.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}
.article-card {
  background: white;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  cursor: pointer;
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
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #6c757d;
}
.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}
@media (max-width: 768px) {
  .articles-grid {
    grid-template-columns: 1fr;
  }
  .page-title {
    font-size: 2rem;
  }
}
</style> 