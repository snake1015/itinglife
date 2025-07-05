<template>
  <div id="app">
    <header class="header">
      <div class="nav-container">
        <div class="nav-item" @click="goTo('/')">首页</div>
        <div class="nav-item" @click="goTo('/tech')">技术分享</div>
        <div class="nav-item" @click="goTo('/life')">生活分享</div>
        <div class="nav-item" @click="goTo('/about')">关于</div>
        <div class="nav-item" @click="goTo('/contact')">联系我们</div>
        <div class="nav-item" @click="goTo('/admin')">后台管理</div>
      </div>
    </header>
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    
    const goTo = (path) => {
      router.push(path)
    }
    
    return {
      goTo
    }
  }
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

.main {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}
</style>

 