<template>
  <el-container style="min-height: 100vh;">
    <el-header>
      <el-menu :default-active="$route.path" mode="horizontal" router>
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/tech">技术分享</el-menu-item>
        <el-menu-item index="/life">生活分享</el-menu-item>
        <el-menu-item index="/about">关于</el-menu-item>
        <el-menu-item index="/contact">联系我们</el-menu-item>
        <el-menu-item index="/admin">后台管理</el-menu-item>
      </el-menu>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
</script> 