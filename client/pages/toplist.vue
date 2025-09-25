<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useFetch } from '#app';
import BeerCard from '~/components/beerCard.vue';
import type { Beer } from '~/types/types';
import beerService from '~/services/BeerService/beerService';

// Use useFetch for SSR and immediate data loading
const { data: event_beers, pending: beersPending, error: beersError } = await beerService.eventBeer.toplist();

// For adding existing beers
const filteredBeers = ref<Beer[]>([]);
const selectedBeerId = ref('');
const beerSearch = ref('');
</script>

<template>
  <h1 class="text-center">Toplist</h1>
  <div class="beerContainer max-w-3xl m-auto">
    <div v-if="beersPending">Loading beers...</div>
    <div v-if="event_beers" v-for="beer in event_beers.response">
      <BeerCard :beer="beer" :buttonsAvailable="false"/>
    </div>
  </div>
</template>
