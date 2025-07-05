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
          <div class="feature-card">
            <div class="feature-icon">📝</div>
            <h3>技术分享</h3>
            <p>分享编程经验、技术心得和项目实践</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🌱</div>
            <h3>生活记录</h3>
            <p>记录日常生活、旅行见闻和人生感悟</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">💬</div>
            <h3>社区交流</h3>
            <p>与志同道合的朋友交流分享</p>
          </div>
        </div>
      </div>
    </section>

    <section class="latest-posts">
      <div class="container">
        <h2 class="section-title">最新内容</h2>
        <div class="posts-grid">
          <div class="post-card" v-for="post in latestPosts" :key="post.id">
            <div class="post-header">
              <span class="post-category">{{ post.category }}</span>
              <span class="post-date">{{ post.date }}</span>
            </div>
            <h3 class="post-title">{{ post.title }}</h3>
            <p class="post-excerpt">{{ post.excerpt }}</p>
            <a :href="post.link" class="read-more">阅读更多</a>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      latestPosts: [
        {
          id: 1,
          title: 'Vue.js 3.0 新特性详解',
          excerpt: '探索Vue.js 3.0带来的Composition API、性能提升等新特性...',
          category: '技术分享',
          date: '2024-01-15',
          link: '/tech'
        },
        {
          id: 2,
          title: '我的编程学习之路',
          excerpt: '分享从零开始学习编程的经历和心得体会...',
          category: '生活记录',
          date: '2024-01-10',
          link: '/life'
        },
        {
          id: 3,
          title: '前端工程化实践',
          excerpt: '探讨现代前端开发中的工程化工具和最佳实践...',
          category: '技术分享',
          date: '2024-01-05',
          link: '/tech'
        }
      ]
    }
  }
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
  background: white;
  padding: 40px 30px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 15px;
  color: #2c3e50;
}

.feature-card p {
  color: #6c757d;
  line-height: 1.6;
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
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
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
}
</style> 