<script setup lang="ts">
import { ref } from 'vue';
import { authService } from '~/services/AuthService/authService';
import Button from '~/components/ui/Button.vue';
import TextInput from '~/components/ui/TextInput.vue';
import StatusMessage from '~/components/ui/StatusMessage.vue';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const username = ref<string>('');
const password = ref<string>('');
const email = ref<string>('');
const success = ref<string>('');
const error = ref<string>('');

const handleRegister = async () => {
  error.value = '';

  if (!username.value || !password.value) {
    error.value = 'Username, Password and Email is required';
    return;
  }

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
      <h2 class="text-2xl mb-6 text-center">{{ t('register') }}</h2>
      <form @submit.prevent="handleRegister">
        <TextInput v-model="username" name="username" title="username" />
        <TextInput v-model="password" name="password" type="password" title="password" />
        <TextInput v-model="email" name="email" type="email" title="email" />
        <StatusMessage :error="error" :success="success" />
        <Button type="submit" color="yellow" class="w-full">{{ t('register') }}</Button>
      </form>
    </div>
  </div>
</template>
