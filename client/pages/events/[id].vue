<script setup lang="ts">
import { useRoute } from 'vue-router';
import { useFetch } from '#app';
import BeerCard from '~/components/beerCard.vue';
import type { Beer, Participants } from '~/types/types';

interface ResponseTypeBeers {
  response: Array<Beer>;
}

interface ResponseTypeParticipants {
  response: Array<Participants>;
}

const route = useRoute();
const eventId = route.params.id;

// Define refs to store the data, error, and pending state
const event_beers = ref<ResponseTypeBeers | null>(null);
const event_participants = ref<ResponseTypeParticipants | null>(null);

onMounted(async () => {
  const { data: fetchedBeers, error: fetchError, pending: fetchPending } = await useFetch<ResponseTypeBeers>(`http://127.0.0.1:5000/events/${eventId}/beers`);
  const { data: fetchedParticipants } = await useFetch<ResponseTypeParticipants>(`http://127.0.0.1:5000/events/${eventId}/participants`);
  event_beers.value = fetchedBeers.value;
  event_participants.value = fetchedParticipants.value;

});
</script>

<template>
  <h1 class="text-center">Event page</h1>
  <div class="beerContainer max-w-3xl m-auto">
    <div class="flex justify-between pb-5">
      <p>Øl</p>
      <button>Ny øl</button>
    </div>
    <div v-if="event_beers" v-for="beer in event_beers.response">
      <BeerCard :beer="beer"/>
    </div>
    <div v-if="event_beers" v-for="beer in event_beers.response">
      <BeerCard :beer="beer"/>
    </div>
  </div>
</template>
