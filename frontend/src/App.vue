<template>
  <el-container style="min-height: 100vh;">
    <el-header>
      <el-menu :default-active="$route.path" mode="horizontal">
        <el-menu-item index="/" @click="() => go('/')">首页</el-menu-item>
        <el-menu-item index="/tech" @click="() => go('/tech')">技术分享</el-menu-item>
        <el-menu-item index="/life" @click="() => go('/life')">生活分享</el-menu-item>
        <el-menu-item index="/about" @click="() => go('/about')">关于</el-menu-item>
        <el-menu-item index="/contact" @click="() => go('/contact')">联系我们</el-menu-item>
        <el-menu-item index="/admin" @click="() => go('/admin')">后台管理</el-menu-item>
      </el-menu>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
  import { useRouter } from 'vue-router';
  const router = useRouter();
  function go(path) {
    router.push(path);
  }
</script> 