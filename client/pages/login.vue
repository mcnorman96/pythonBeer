<script setup lang="ts">
import { ref } from 'vue';
import { useAuth } from '~/composables/useAuth';
import { useRouter } from 'vue-router';
import { authService } from '~/services/AuthService/authService';
import BaseButton from '~/components/ui/BaseButton.vue';
import BaseInput from '~/components/ui/BaseInput.vue';
import StatusMessage from '~/components/ui/StatusMessage.vue';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const username = ref<string>('');
const password = ref<string>('');
const error = ref<string>('');
const { login } = useAuth();
const router = useRouter();

const handleLogin = async () => {
  error.value = '';

  console.log(username, password);

  if (!username.value || !password.value) {
    error.value = 'Username and password is required';
    return;
  }

  try {
    const response = await authService.login({
      username: username.value,
      password: password.value,
    });

    console.log('response', response);

    if (!response.success) {
      throw new Error('Login failed');
    }

    if (response?.response?.token) {
      login(response?.response?.token);
      router.push('/');
    } else {
      error.value = 'Invalid credentials';
    }
  } catch (e) {
    console.error('login failed', e);
    error.value = 'Login failed';
  }
};
</script>

<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="bg-white p-8 rounded shadow-md w-96">
      <h2 class="text-2xl mb-6 text-center">{{ t('login') }}</h2>
      <form @submit.prevent="handleLogin">
        <BaseInput v-model="username" name="username" title="username" />
        <BaseInput v-model="password" type="password" name="password" title="password" />
        <StatusMessage :error="error" />
        <BaseButton color="yellow" type="submit" class="w-full">{{ t('login') }}</BaseButton>
      </form>
    </div>
  </div>
</template>
