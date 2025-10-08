import type { RouteLocationNormalized } from 'vue-router';

export default defineNuxtRouteMiddleware((to: RouteLocationNormalized) => {
  if (process.client) {
    const token = localStorage.getItem('token');
    if (!token && to.path !== '/login' && to.path !== '/register') {
      return navigateTo('/login');
    }
  }
});
