<script setup lang="ts">
import BeerCard from '~/components/beerCard.vue';
import beerService from '~/services/BeerService/beerService';

const { data: event_beers, pending: beersPending } = await beerService.eventBeer.toplist();
</script>

<template>
  <h1 class="text-center">Toplist</h1>
  <div class="beerContainer max-w-3xl m-auto">
    <div v-if="beersPending">Loading beers...</div>
    <div v-if="!event_beers || event_beers.response.length < 1">No beers rated yet</div>
    <div v-if="event_beers && event_beers.response.length > 0">
      <div v-for="beer in event_beers.response" :key="beer.id">
        <BeerCard :beer="beer" :buttonsAvailable="false" />
      </div>
    </div>
  </div>
</template>
