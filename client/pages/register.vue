<script setup lang="ts">
import { ref } from 'vue';
import { authService } from '~/services/AuthService/authService';
import Button from '~/components/ui/Button.vue';

const username = ref<string>('');
const password = ref<string>('');
const email = ref<string>('');
const success = ref<string>('');
const error = ref<string>('');

const handleRegister = async () => {
  error.value = '';
  try {
    const response = await authService.registerUser({
      username: username.value,
      password: password.value,
      email: email.value,
    });

    if (!response.ok) {
      throw new Error('Registration failed');
    }

    success.value = 'Registration successful! You can now log in.';
  } catch (e) {
    console.error('Registration failed', e);
    error.value = 'Registration failed';
  }
};
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="bg-white p-8 rounded shadow-md w-96">
      <h2 class="text-2xl mb-6 text-center">Register</h2>
      <form @submit.prevent="handleRegister">
        <div class="mb-4">
          <label class="block mb-2">Username</label>
          <input v-model="username" class="border p-2 w-full" placeholder="Username" />
        </div>
        <div class="mb-4">
          <label class="block mb-2">Password</label>
          <input
            v-model="password"
            type="password"
            class="border p-2 w-full"
            placeholder="Password"
          />
        </div>
        <div class="mb-4">
          <label class="block mb-2">Email</label>
          <input v-model="email" type="email" class="border p-2 w-full" placeholder="Email" />
        </div>
        <div v-if="error" class="text-red-500 mb-4">{{ error }}</div>
        <div v-if="success" class="text-green-500 mb-4">{{ success }}</div>
        <Button type="submit" color="yellow" class="w-full">Register</Button>
      </form>
    </div>
  </div>
</template>
