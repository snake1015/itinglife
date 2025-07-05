<template>
  <el-container style="min-height: 100vh;">
    <el-header>
      <el-menu :default-active="$route.path" mode="horizontal">
        <el-menu-item index="/" @click="goHome">首页</el-menu-item>
        <el-menu-item index="/tech" @click="goTech">技术分享</el-menu-item>
        <el-menu-item index="/life" @click="goLife">生活分享</el-menu-item>
        <el-menu-item index="/about" @click="goAbout">关于</el-menu-item>
        <el-menu-item index="/contact" @click="goContact">联系我们</el-menu-item>
        <el-menu-item index="/admin" @click="goAdmin">后台管理</el-menu-item>
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
  
  function goHome() {
    router.push('/');
  }
  
  function goTech() {
    router.push('/tech');
  }
  
  function goLife() {
    router.push('/life');
  }
  
  function goAbout() {
    router.push('/about');
  }
  
  function goContact() {
    router.push('/contact');
  }
  
  function goAdmin() {
    router.push('/admin');
  }
</script> 