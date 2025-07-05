import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  { path: '/', component: () => import('../views/Home.vue') },
  { path: '/tech', component: () => import('../views/Tech.vue') },
  { path: '/life', component: () => import('../views/Life.vue') },
  { path: '/about', component: () => import('../views/About.vue') },
  { path: '/contact', component: () => import('../views/Contact.vue') },
  { path: '/admin', component: () => import('../views/Admin.vue') },
  { path: '/login', component: () => import('../views/Login.vue') },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router; 