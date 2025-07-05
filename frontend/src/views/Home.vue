<template>
  <div>
    <el-carousel height="200px" v-if="banners.length">
      <el-carousel-item v-for="item in banners" :key="item.id">
        <a v-if="item.link" :href="item.link" target="_blank">
          <img :src="item.img" style="width:100%;height:200px;object-fit:cover;" />
        </a>
        <img v-else :src="item.img" style="width:100%;height:200px;object-fit:cover;" />
      </el-carousel-item>
    </el-carousel>
    <el-card class="mt">今日推荐：<el-link v-if="today.id" @click="viewArticle(today.id)">{{ today.title }}</el-link></el-card>
    <el-card class="mt">本月热门：<ul><li v-for="a in hot" :key="a.id"><el-link @click="viewArticle(a.id)">{{ a.title }}</el-link></li></ul></el-card>
    <el-card class="mt">
      <div class="flex-between">
        <span>实用小工具</span>
        <el-button size="small" @click="fetchWeather">刷新天气</el-button>
      </div>
      <div v-if="weather.city">{{ weather.city }}：{{ weather.weather }} {{ weather.temp }}℃</div>
      <div v-else>天气信息加载中...</div>
    </el-card>
    <el-card class="mt">
      <div>社区互动</div>
      <div>最新评论：</div>
      <ul><li v-for="c in comments" :key="c.id">{{ c.content }}</li></ul>
      <div>最新留言：</div>
      <ul><li v-for="m in messages" :key="m.id">{{ m.content }}</li></ul>
    </el-card>
    <el-dialog v-model="showDetail" width="60%">
      <template #header> {{ detail.title }} </template>
      <v-md-preview :text="detail.content || ''" />
    </el-dialog>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import VMdPreview from '@kangc/v-md-editor/lib/preview';
import githubTheme from '@kangc/v-md-editor-theme-github';
import '@kangc/v-md-editor/lib/style/preview.css';
import '@kangc/v-md-editor-theme-github/lib/theme.css';
VMdPreview.use(githubTheme);

const banners = ref([]);
const today = ref({});
const hot = ref([]);
const comments = ref([]);
const messages = ref([]);
const weather = ref({});
const showDetail = ref(false);
const detail = ref({});

function fetchBanners() {
  axios.get('http://localhost:8000/api/banners').then(res => {
    banners.value = res.data;
  });
}
function fetchToday() {
  axios.get('http://localhost:8000/api/articles', { params: { is_featured: true } }).then(res => {
    today.value = res.data[0] || {};
  });
}
function fetchHot() {
  axios.get('http://localhost:8000/api/articles/hot').then(res => {
    hot.value = res.data;
  });
}
function fetchComments() {
  axios.get('http://localhost:8000/api/comments').then(res => {
    comments.value = res.data.slice(0, 5);
  });
}
function fetchMessages() {
  axios.get('http://localhost:8000/api/messages').then(res => {
    messages.value = res.data.slice(0, 5);
  });
}
function fetchWeather() {
  // 示例：可用第三方天气API，这里用和风天气免费API（需替换key）
  axios.get('https://devapi.qweather.com/v7/weather/now', {
    params: {
      location: '101010100', // 北京
      key: 'demo-key' // 请替换为你自己的key
    }
  }).then(res => {
    if (res.data && res.data.now) {
      weather.value = {
        city: '北京',
        weather: res.data.now.text,
        temp: res.data.now.temp
      };
    }
  });
}
function viewArticle(id) {
  axios.get(`http://localhost:8000/api/articles/${id}`).then(res => {
    detail.value = res.data;
    showDetail.value = true;
  });
}
onMounted(() => {
  fetchBanners();
  fetchToday();
  fetchHot();
  fetchComments();
  fetchMessages();
  fetchWeather();
});
</script>
<style scoped>
.mt { margin-top: 20px; }
.flex-between { display: flex; justify-content: space-between; align-items: center; }
ul { margin: 0; padding-left: 20px; }
</style> 