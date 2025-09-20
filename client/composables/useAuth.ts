import { ref, onMounted } from 'vue';

const isAuthenticated = ref(false);

export function useAuth() {
  function login(token: string) {
    if (process.client) {
      localStorage.setItem('token', token);
    }
    isAuthenticated.value = true;
  }
  function checkAuth() {
    if (process.client) {
      const token = localStorage.getItem('token');
      isAuthenticated.value = !!token;
    }
  }
  function logout() {
    if (process.client) {
      localStorage.removeItem('token');
    }
    isAuthenticated.value = false;
  }
  // Ensure auth state is synced on page load
  if (process.client) {
    onMounted(() => {
      checkAuth();
    });
  }
  return { isAuthenticated, login, logout, checkAuth };
}
