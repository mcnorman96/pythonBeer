<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Button from '~/components/ui/Button.vue';
import { authService } from '~/services/AuthService/authService';

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
  <h1 class="text-center">Profile</h1>
  <div class="profileContainer max-w-3xl m-auto flex flex-wrap">
    <div class="w-full md:w-1/2">
      <label class="block mb-2">Username</label>
      <input
        name="username"
        v-model="username"
        class="border p-2 w-full mb-2"
        placeholder="Username"
      />

      <label class="block mb-2">Email</label>
      <input
        name="email"
        type="email"
        v-model="email"
        class="border p-2 w-full mb-2"
        placeholder="Email"
      />

      <!-- <label class="block mb-2">Password</label>
      <input
        name="password"
        type="password"
        v-model="password"
        class="border p-2 w-full mb-2"
        placeholder="Password"
      /> -->
    </div>

    <div class="w-full md:w-1/2">
      <img src="/img/user.png" alt="profile" class="w-1/2 m-auto" />
    </div>
    <Button color="yellow" class="ml-auto mt-5" @click="handleSave"> Save </Button>
    <div v-if="errorMsg" class="text-red-500 mb-4 w-full text-right">{{ errorMsg }}</div>
    <div v-if="successMsg" class="text-green-500 mb-4 w-full text-right">{{ successMsg }}</div>
  </div>
</template>
