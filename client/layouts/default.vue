<script lang="ts" setup>
import { useAuth } from '~/composables/useAuth';
import { ref, onMounted, watch } from 'vue';

const menuItemsClass = "px-5";
const isLoggedIn = ref(false);

const { isAuthenticated, logout, checkAuth } = useAuth();

onMounted(() => {
  checkAuth();
  isLoggedIn.value = isAuthenticated.value;
});

// Watch for changes in authentication state
watch(isAuthenticated, (val) => {
  isLoggedIn.value = val;
});
</script>

<template>
  <header class="bg-black h-24 w-screen text-white relative">
    <nav>
      <div class="logo absolute left-0 top-1/2 -translate-y-1/2 flex px-5">
        <img src="/img/beer.svg"> 
        <div class="ml-3 text-2xl mt-1">BAJER KLUBBEN</div>
      </div>
      <div class="middle-menu absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 flex">
        <NuxtLink :class=menuItemsClass to="/events">Events</NuxtLink>
        <NuxtLink :class=menuItemsClass to="/toplist">Toplist</NuxtLink>
      </div>
      <client-only>
        <div class="right-menu absolute right-0 top-1/2  -translate-y-1/2 flex" v-if="!isLoggedIn">
          <NuxtLink :class=menuItemsClass to="/login">Log ind</NuxtLink>
          <NuxtLink :class=menuItemsClass to="/register">Register</NuxtLink>
        </div>
        <div class="right-menu absolute right-0 top-1/2  -translate-y-1/2 flex" v-if="isLoggedIn">
          <NuxtLink :class=menuItemsClass to="/">Profile</NuxtLink>
          <a @click="logout" :class=menuItemsClass>Log out</a>
        </div>
      </client-only>
    </nav>
  </header>
  <slot />
</template>

