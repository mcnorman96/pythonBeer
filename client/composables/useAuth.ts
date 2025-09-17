import { ref } from 'vue';

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
      isAuthenticated.value = !!localStorage.getItem('token');
    }
  }
  function logout() {
    if (process.client) {
      localStorage.removeItem('token');
    }
    isAuthenticated.value = false;
  }
  return { isAuthenticated, login, logout, checkAuth };
}
