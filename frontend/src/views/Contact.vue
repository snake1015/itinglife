<template>
  <div>
    <el-card>
      <el-form :model="form" label-width="80px" @submit.prevent="submitForm">
        <el-form-item label="姓名">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="内容">
          <el-input type="textarea" v-model="form.content" rows="4" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm">发送</el-button>
        </el-form-item>
      </el-form>
      <el-divider>社交媒体</el-divider>
      <el-link href="https://github.com/" target="_blank">GitHub</el-link>
      <el-link href="https://weibo.com/" target="_blank" class="ml">微博</el-link>
      <el-divider>地址信息</el-divider>
      <div>北京市朝阳区XX路XX号</div>
    </el-card>
  </div>
</template>
<script setup>
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
const form = ref({ name: '', email: '', content: '' });
function submitForm() {
  // 示例：可对接后端留言/邮件API
  if (!form.value.name || !form.value.email || !form.value.content) {
    ElMessage.error('请填写完整信息');
    return;
  }
  // 这里可用axios.post('/api/messages', form.value)
  ElMessage.success('发送成功（模拟）');
  form.value = { name: '', email: '', content: '' };
}
</script>
<style scoped>
.el-card { margin: 40px auto; max-width: 600px; }
.ml { margin-left: 16px; }
</style> 