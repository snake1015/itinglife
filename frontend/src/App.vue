<template>
  <div>
    <header>
      <div>
        <div>itinglife</div>
        <div>
          <a href="/">首页</a>
          <a href="/tech">技术分享</a>
          <a href="/life">生活分享</a>
          <a href="/about">关于</a>
          <a href="/contact">联系我们</a>
          <a href="/admin">后台管理</a>
        </div>
      </div>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
}

header {
  background: #fff;
  border-bottom: 1px solid #e1e5e9;
  padding: 15px 0;
}

header > div {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

header > div > div:first-child {
  font-size: 20px;
  font-weight: bold;
  color: #2c3e50;
}

header > div > div:last-child {
  display: flex;
  gap: 30px;
}

header a {
  text-decoration: none;
  color: #6c757d;
  font-size: 14px;
  padding: 8px 0;
  transition: color 0.3s ease;
}

header a:hover {
  color: #007bff;
}

main {
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  header > div {
    flex-direction: column;
    gap: 15px;
  }
  
  header > div > div:last-child {
    gap: 20px;
  }
  
  main {
    padding: 20px;
  }
}
</style>

 