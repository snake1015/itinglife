<template>
  <div class="home">
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">欢迎来到 itinglife</h1>
        <p class="hero-subtitle">分享技术，记录生活，连接世界</p>
        <div class="hero-buttons">
          <a href="/tech" class="btn btn-primary">技术分享</a>
          <a href="/life" class="btn btn-secondary">生活记录</a>
        </div>
      </div>
    </section>

    <section class="features">
      <div class="container">
        <h2 class="section-title">功能特色</h2>
        <div class="features-grid">
          <a
            class="feature-card"
            v-for="cat in categories"
            :key="cat.id"
            :href="cat.name.includes('技') ? '/tech' : (cat.name.includes('生活') ? '/life' : '/contact')"
          >
            <div class="feature-icon" :style="{fontSize: '3.5rem'}">
              <!-- 根据分类名显示不同emoji，实际可用iconfont或svg -->
              <span v-if="cat.name.includes('技')">📝</span>
              <span v-else-if="cat.name.includes('生活')">🌱</span>
              <span v-else>💬</span>
            </div>
            <h3 class="feature-title">{{ cat.name }}</h3>
            <p class="feature-desc">{{ cat.description || '欢迎体验丰富内容' }}</p>
          </a>
        </div>
      </div>
    </section>

    <section class="latest-posts">
      <div class="container">
        <h2 class="section-title">最新内容</h2>
        <div class="posts-grid">
          <div class="post-card" v-for="post in latestPosts" :key="post.id">
            <div class="post-header">
              <span class="post-category">{{ getCategoryName(post.category_id) }}</span>
              <span class="post-date">{{ formatDate(post.created_at) }}</span>
            </div>
            <h3 class="post-title">{{ post.title }}</h3>
            <p class="post-excerpt">{{ post.summary }}</p>
            <a :href="'/tech'" class="read-more">阅读更多</a>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios'
import { getApiUrl } from '../config.js'

export default {
  name: 'Home',
  data() {
    return {
      latestPosts: [],
      categories: [],
    }
  },
  methods: {
    fetchLatestPosts() {
      axios
        .get(getApiUrl('/api/articles'))
        .then(res => {
          // 只取前5条
          this.latestPosts = res.data.slice(0, 5)
        })
        .catch(() => {
          this.latestPosts = []
        })
    },
    fetchCategories() {
      axios
        .get(getApiUrl('/api/categories'))
        .then(res => {
          this.categories = res.data
        })
        .catch(() => {
          this.categories = []
        })
    },
    getCategoryName(categoryId) {
      if (!categoryId) return '未分类'
      const cat = this.categories.find(c => c.id === categoryId)
      return cat ? cat.name : '未分类'
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      const d = new Date(dateStr)
      return d.toLocaleDateString('zh-CN')
    },
  },
  mounted() {
    this.fetchLatestPosts()
    this.fetchCategories()
  },
}
</script>

<style scoped>
.home {
  min-height: 100vh;
}

.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 20px;
  text-align: center;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 20px;
  animation: fadeInUp 1s ease;
}

.hero-subtitle {
  font-size: 1.2rem;
  margin-bottom: 40px;
  opacity: 0.9;
  animation: fadeInUp 1s ease 0.2s both;
}

.hero-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  animation: fadeInUp 1s ease 0.4s both;
}

.btn {
  padding: 12px 30px;
  border-radius: 25px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-block;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-primary:hover {
  background: #0056b3;
  transform: translateY(-2px);
}

.btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background: white;
  color: #667eea;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 60px;
  color: #2c3e50;
}

.features {
  padding: 80px 0;
  background: #f8f9fa;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 40px;
}

.feature-card {
  background: none;
  padding: 44px 24px 32px 24px;
  border-radius: 16px;
  text-align: center;
  box-shadow: none;
  transition: transform 0.25s, background 0.25s;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  text-decoration: none;
  color: inherit;
  display: block;
}

.feature-card:hover {
  transform: translateY(-6px) scale(1.03);
  background: linear-gradient(90deg, #f8f9fa 60%, #e9e6f7 100%);
  box-shadow: 0 8px 32px rgba(102,126,234,0.10);
}

.feature-icon {
  font-size: 3.5rem;
  margin-bottom: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 64px;
}

.feature-title {
  font-size: 1.7rem;
  font-weight: bold;
  margin-bottom: 18px;
  color: #2c3e50;
  letter-spacing: 1px;
}

.feature-desc {
  color: #6c757d;
  line-height: 1.7;
  margin-bottom: 0;
  min-height: 40px;
}

.latest-posts {
  padding: 80px 0;
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
}

.post-card {
  background: white;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.post-card:hover {
  transform: translateY(-3px);
}

.post-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.post-category {
  background: #007bff;
  color: white;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 0.8rem;
}

.post-date {
  color: #6c757d;
  font-size: 0.9rem;
}

.post-title {
  font-size: 1.3rem;
  margin-bottom: 15px;
  color: #2c3e50;
}

.post-excerpt {
  color: #6c757d;
  line-height: 1.6;
  margin-bottom: 20px;
}

.read-more {
  color: #007bff;
  text-decoration: none;
  font-weight: 500;
}

.read-more:hover {
  text-decoration: underline;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }

  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }

  .features-grid,
  .posts-grid {
    grid-template-columns: 1fr;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .feature-card {
    padding: 28px 8px 18px 8px;
  }

  .feature-title {
    font-size: 1.2rem;
  }

  .feature-icon {
    font-size: 2.2rem;
    height: 40px;
  }
}
</style>
