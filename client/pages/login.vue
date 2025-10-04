<script setup lang="ts">
import { ref } from 'vue';
import { useAuth } from '~/composables/useAuth';
import { useRouter } from 'vue-router';
import { authService } from '~/services/AuthService/authService';
import Button from '~/components/ui/Button.vue';

const username = ref<string>('');
const password = ref<string>('');
const error = ref<string>('');
const { login } = useAuth();
const router = useRouter();

const handleLogin = async () => {
  error.value = '';
  try {
    const response = await authService.login({ username: username.value, password: password.value });

    if (!response.ok) {
      throw new Error('Login failed');
    }
    const data = await response.json();
    if (data.token) {
      login(data.token);
      router.push('/');
    } else {
      error.value = 'Invalid credentials';
    }
  } catch (e) {
    error.value = 'Login failed';
  }
};
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="bg-white p-8 rounded shadow-md w-96">
      <h2 class="text-2xl mb-6 text-center">Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block mb-2">Username</label>
          <input v-model="username" class="border p-2 w-full" placeholder="Username" />
        </div>
        <div class="mb-4">
          <label class="block mb-2">Password</label>
          <input v-model="password" type="password" class="border p-2 w-full" placeholder="Password" />
        </div>
        <div v-if="error" class="text-red-500 mb-4">{{ error }}</div>
        <Button color="yellow" type="submit" class="w-full">Login</Button>
      </form>
    </div>
  </div>
</template>
