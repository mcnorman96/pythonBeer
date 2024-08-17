<script setup>
import { useFetch } from '#app';
import events from '~/components/events.vue';

const { data, error, pending } = await useFetch('http://127.0.0.1:5000/events');
console.log(data.response);
</script>

<template>
  <h1 class="text-center">Events</h1>
  <events :data="data" :error="error" :pending="pending"/>
</template>
