<template>
  <div id="app">
    <el-container style="min-height: 100vh;">
      <el-header>
        <nav class="navigation">
          <router-link to="/" class="nav-item">首页</router-link>
          <router-link to="/tech" class="nav-item">技术分享</router-link>
          <router-link to="/life" class="nav-item">生活分享</router-link>
          <router-link to="/about" class="nav-item">关于</router-link>
          <router-link to="/contact" class="nav-item">联系我们</router-link>
          <router-link to="/admin" class="nav-item">后台管理</router-link>
        </nav>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
// 空的setup，确保没有任何可能导致解析问题的代码
</script>

<style scoped>
#app {
  font-family: Arial, sans-serif;
}

.navigation {
  display: flex;
  align-items: center;
  height: 60px;
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
}

.nav-item {
  padding: 0 20px;
  height: 60px;
  line-height: 60px;
  text-decoration: none;
  color: #303133;
  font-size: 14px;
  transition: color 0.3s;
}

.nav-item:hover {
  color: #409eff;
}

.nav-item.router-link-active {
  color: #409eff;
  border-bottom: 2px solid #409eff;
}
</style>

 