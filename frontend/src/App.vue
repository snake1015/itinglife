<template>
  <div id="app">
    <header class="header">
      <div class="nav-container">
        <router-link to="/" class="nav-item">首页</router-link>
        <router-link to="/tech" class="nav-item">技术分享</router-link>
        <router-link to="/life" class="nav-item">生活分享</router-link>
        <router-link to="/about" class="nav-item">关于</router-link>
        <router-link to="/contact" class="nav-item">联系我们</router-link>
        <router-link to="/admin" class="nav-item">后台管理</router-link>
      </div>
    </header>
    <main class="main">
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
  font-family: Arial, sans-serif;
  min-height: 100vh;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
  height: 60px;
  display: flex;
  align-items: center;
}

.nav-container {
  display: flex;
  align-items: center;
  height: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.nav-item {
  padding: 0 20px;
  height: 60px;
  line-height: 60px;
  color: #303133;
  font-size: 14px;
  cursor: pointer;
  transition: color 0.3s;
  text-decoration: none;
}

.nav-item:hover {
  color: #409eff;
}

.nav-item.router-link-active {
  color: #409eff;
  border-bottom: 2px solid #409eff;
}

.main {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}
</style>

 