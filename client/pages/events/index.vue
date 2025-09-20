<script setup>
import { useFetch } from '#app';
import events from '~/components/events.vue';
import beerService from '~/services/BeerService/beerService';

const { data, error, pending } = await beerService.events.getEvents();
</script>

<template>
  <h1 class="text-center">Events</h1>
  <events :data="data" :error="error" :pending="pending"/>
</template>
