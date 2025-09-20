import { useAuth } from '~/composables/useAuth';

export default defineNuxtRouteMiddleware((to, from) => {
  const { isAuthenticated, checkAuth } = useAuth();
  checkAuth();
  if (!isAuthenticated.value && to.path !== '/login' && to.path !== '/register') {
    return navigateTo('/login');
  }
});
