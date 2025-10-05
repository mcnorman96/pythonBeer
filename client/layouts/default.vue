<script lang="ts" setup>
import { useAuth } from '~/composables/useAuth';
import { ref, onMounted, watch } from 'vue';

const menuItemsClass = 'px-5';
const isLoggedIn = ref(false);
const showMobileMenu = ref(false);

const { isAuthenticated, logout, checkAuth } = useAuth();

onMounted(() => {
  checkAuth();
  isLoggedIn.value = isAuthenticated.value;
});

// Watch for changes in authentication state
watch(isAuthenticated, (val: boolean) => {
  isLoggedIn.value = val;
});

function toggleMobileMenu() {
  showMobileMenu.value = !showMobileMenu.value;
}
</script>

<template>
  <header class="bg-zinc-800 h-24 w-screen text-white relative">
    <nav>
      <div class="logo absolute left-0 top-1/2 -translate-y-1/2 px-5">
        <a href="/events" class="flex items-center">
          <img src="/img/beer.svg" />
          <div class="ml-3 text-2xl mt-1">BAJER KLUBBEN</div>
        </a>
      </div>
      <!-- Desktop menu -->
      <div
        v-if="isLoggedIn"
        class="middle-menu absolute right-0 top-1/2 -translate-y-1/2 flex hidden md:block"
      >
        <NuxtLink :class="menuItemsClass" to="/events">Events</NuxtLink>
        <NuxtLink :class="menuItemsClass" to="/toplist">Toplist</NuxtLink>
        <NuxtLink @click="logout" to="/login" :class="menuItemsClass">Log out</NuxtLink>
      </div>
      <client-only>
        <div class="right-menu absolute right-0 top-1/2 -translate-y-1/2 flex" v-if="!isLoggedIn">
          <NuxtLink :class="menuItemsClass" to="/login">Login</NuxtLink>
          <NuxtLink :class="menuItemsClass" to="/register">Register</NuxtLink>
        </div>
      </client-only>

      <!-- Mobile hamburger -->
      <div v-if="isLoggedIn" class="absolute right-0 top-1/2 -translate-y-1/2 md:hidden">
        <Button @click="toggleMobileMenu" :class="'focus:outline-none'">
          <svg
            class="w-8 h-8"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </Button>
        <div
          v-if="showMobileMenu"
          class="absolute bg-zinc-800 text-white rounded shadow-lg mt-2 right-0 z-50 w-max"
        >
          <NuxtLink
            :class="menuItemsClass + ' block py-2'"
            to="/events"
            @click="showMobileMenu = false"
            >Events</NuxtLink
          >
          <NuxtLink
            :class="menuItemsClass + ' block py-2'"
            to="/toplist"
            @click="showMobileMenu = false"
            >Toplist</NuxtLink
          >
          <NuxtLink
            :class="menuItemsClass + ' block py-2'"
            to="/login"
            @click="showMobileMenu = false && logout()"
            >Log out</NuxtLink
          >
        </div>
      </div>
    </nav>
  </header>
  <div class="mr-2 ml-2 mb-5">
    <slot />
  </div>
</template>
