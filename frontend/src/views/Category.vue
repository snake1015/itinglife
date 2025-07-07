<template>
  <div class="category-page">
    <div class="page-header">
      <h1 class="page-title">所有分类</h1>
      <p class="page-subtitle">浏览所有分类与相关文章</p>
    </div>
    <div class="categories-grid">
      <div
        class="category-card"
        v-for="cat in categories"
        :key="cat.id"
        @click="selectCategory(cat.id)"
        :class="{ active: selectedCategory === cat.id }"
      >
        <div class="category-icon">
          <span v-if="cat.name.includes('技')">📝</span>
          <span v-else-if="cat.name.includes('生活')">🌱</span>
          <span v-else>📚</span>
        </div>
        <div class="category-title">{{ cat.name }}</div>
        <div class="category-desc">{{ cat.description || '丰富内容等你发现' }}</div>
      </div>
    </div>
    <div v-if="selectedCategory" class="category-articles">
      <h2 class="category-articles-title">“{{ getCategoryName(selectedCategory) }}” 相关文章</h2>
      <div class="articles-grid">
        <article
          v-for="article in filteredArticles"
          :key="article.id"
          class="article-card"
        >
          <div class="article-header">
            <span class="article-date">{{ formatDate(article.created_at) }}</span>
          </div>
          <h3 class="article-title">{{ article.title }}</h3>
          <p class="article-excerpt">{{ article.summary }}</p>
        </article>
      </div>
    </div>
    <div v-else class="empty-state">
      <div class="empty-icon">📚</div>
      <h3>请选择分类查看相关文章</h3>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
import { getApiUrl } from '../config.js'
export default {
  name: 'Category',
  data() {
    return {
      articles: [],
      categories: [],
      selectedCategory: null,
    }
  },
  computed: {
    filteredArticles() {
      if (!this.selectedCategory) return []
      return this.articles.filter(article => article.category_id === this.selectedCategory)
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
    selectCategory(id) {
      this.selectedCategory = id
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
.category-page {
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
.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 30px;
  margin: 40px 0 30px 0;
}
.category-card {
  background: white;
  border-radius: 14px;
  padding: 32px 18px 24px 18px;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.10);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  border: 2px solid transparent;
}
.category-card:hover, .category-card.active {
  transform: translateY(-6px) scale(1.03);
  box-shadow: 0 12px 32px rgba(102,126,234,0.13);
  border: 2px solid #764ba2;
}
.category-icon {
  font-size: 2.5rem;
  margin-bottom: 18px;
}
.category-title {
  font-size: 1.3rem;
  font-weight: bold;
  margin-bottom: 10px;
  color: #2c3e50;
}
.category-desc {
  color: #6c757d;
  line-height: 1.6;
  min-height: 32px;
}
.category-articles-title {
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
  justify-content: flex-end;
  margin-bottom: 15px;
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
  .categories-grid {
    grid-template-columns: 1fr;
    gap: 18px;
  }
  .articles-grid {
    grid-template-columns: 1fr;
  }
  .page-title {
    font-size: 2rem;
  }
}
</style> 