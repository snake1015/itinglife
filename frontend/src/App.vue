<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <div class="nav-brand">itinglife</div>
        <div class="nav-links">
          <a href="/" class="nav-link">首页</a>
          <a href="/tech" class="nav-link">技术分享</a>
          <a href="/life" class="nav-link">生活分享</a>
          <a href="/about" class="nav-link">关于</a>
          <a href="/contact" class="nav-link">联系我们</a>
          <a href="/admin" class="nav-link">后台管理</a>
        </div>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  background: #fff;
  border-bottom: 1px solid #e1e5e9;
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: 60px;
}

.nav-brand {
  font-size: 20px;
  font-weight: bold;
  color: #2c3e50;
}

.nav-links {
  display: flex;
  gap: 30px;
}

.nav-link {
  text-decoration: none;
  color: #6c757d;
  font-size: 14px;
  padding: 8px 0;
  transition: color 0.3s ease;
  position: relative;
}

.nav-link:hover {
  color: #007bff;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: #007bff;
  transition: width 0.3s ease;
}

.nav-link:hover::after {
  width: 100%;
}

.main-content {
  flex: 1;
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    height: auto;
    padding: 15px 20px;
  }
  
  .nav-links {
    margin-top: 15px;
    gap: 20px;
  }
  
  .main-content {
    padding: 20px;
  }
}
</style>

 