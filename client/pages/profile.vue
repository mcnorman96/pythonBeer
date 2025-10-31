<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Button from '~/components/ui/Button.vue';
import { authService } from '~/services/AuthService/authService';
import TextInput from '~/components/ui/TextInput.vue';
import StatusMessage from '~/components/ui/StatusMessage.vue';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const username = ref<string>('');
const email = ref<string>('');
const password = ref<string>('');
const errorMsg = ref<string | null>(null);
const successMsg = ref<string | null>(null);

onMounted(async () => {
  const userData = await authService.getUser();
  if (userData.response) {
    username.value = userData.response.username;
    email.value = userData.response.email;
    password.value = userData.response.password;
  }
});

const handleSave = async () => {
  const saveRating = await authService.updateUser({
    username: username.value,
    email: email.value,
  });

  if (saveRating.errorMsg) {
    errorMsg.value = saveRating.errorMsg;
    successMsg.value = null;
    return;
  } else {
    errorMsg.value = null;
    successMsg.value = 'Successfully updated user';
  }
};
</script>

<template>
  <h1 class="text-center">{{ t('profile') }}</h1>
  <form @submit.prevent="handleSave" class="profileContainer max-w-3xl m-auto flex flex-wrap">
    <div class="w-full md:w-1/2">
      <TextInput v-model="username" name="username" title="username" />
      <TextInput v-model="email" name="email" type="email" title="email" />
    </div>

    <div class="w-full md:w-1/2">
      <img src="/img/user.png" alt="profile" class="w-1/2 m-auto" />
    </div>

    <Button type="submit" color="yellow" class="ml-auto mt-5">{{ t('save') }}</Button>
    <StatusMessage class="text-right w-full" :error="errorMsg" :success="successMsg" />
  </form>
</template>
