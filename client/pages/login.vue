<script setup lang="ts">
import { ref } from 'vue';
import { useAuth } from '~/composables/useAuth';
import { useRouter } from 'vue-router';
import { authService } from '~/services/AuthService/authService';
import Button from '~/components/ui/Button.vue';
import TextInput from '~/components/ui/TextInput.vue';
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
        <TextInput v-model="username" name="username" title="username" />
        <TextInput v-model="password" type="password" name="password" title="password" />
        <StatusMessage :error="error" />
        <Button color="yellow" type="submit" class="w-full">{{ t('login') }}</Button>
      </form>
    </div>
  </div>
</template>
