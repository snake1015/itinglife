import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', component: () => import('../views/Home.vue') },
  { path: '/tech', component: () => import('../views/Tech.vue') },
  { path: '/life', component: () => import('../views/Life.vue') },
  { path: '/about', component: () => import('../views/About.vue') },
  { path: '/contact', component: () => import('../views/Contact.vue') },
  { 
    path: '/admin', 
    component: () => import('../views/Admin.vue'),
    meta: { requiresAuth: true }
  },
  { path: '/login', component: () => import('../views/Login.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('user')
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    // 需要登录但未登录，重定向到登录页
    next('/login')
  } else if (to.path === '/login' && isAuthenticated) {
    // 已登录用户访问登录页，重定向到后台
    next('/admin')
  } else {
    next()
  }
})

export default router
