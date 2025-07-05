<template>
  <div>
    <el-card>
      <MdPreview :modelValue="aboutContent" />
    </el-card>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'

const aboutContent = ref('')

function fetchAbout() {
  // 示例：可从后端获取Markdown内容
  aboutContent.value = `
# 关于作者

- **姓名**：张三
- **邮箱**：zhangsan@example.com
- **社交**：[GitHub](https://github.com/) | [微博](https://weibo.com/)

## 兴趣爱好
- 编程、摄影、旅行、阅读

## FAQ
- **Q:** 如何联系作者？
- **A:** 通过邮箱或社交媒体。

- **Q:** 网站内容可以转载吗？
- **A:** 署名即可。
`
}
onMounted(fetchAbout)
</script>
<style scoped>
.el-card {
  margin: 40px auto;
  max-width: 800px;
}
</style>
