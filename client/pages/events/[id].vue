<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useFetch } from '#app';
import BeerCard from '~/components/beerCard.vue';
import AddRatingModal from '~/components/modals/AddRatingModal.vue';
import AddBeerModal from '~/components/modals/AddBeerModal.vue';
import ViewRatingsModal from '~/components/modals/ViewRatingsModal.vue';
import type { Beer, Participants, ResponseTypeBeers, ResponseTypeParticipants } from '~/types/types';
import beerService from '~/services/BeerService/beerService';
import { onMounted, onUnmounted } from 'vue';
import { io } from 'socket.io-client';

const route = useRoute();
const eventId = route.params.id;
const event_beers = ref<Beer[]>([]);

const socket = io('http://localhost:8000'); // Flask-SocketIO default port

onMounted(async () => {
  const beerData = await beerService.eventBeer.toplistBeersInEvent(eventId as string);
  if (beerData.success && beerData.response) {
      event_beers.value = beerData.response;
  }

  // const { 
  //   data: event_participants, 
  //   pending: participantsPending, 
  //   error: participantsError 
  // } = await beerService.eventParticipants.getEventParticipants(eventId as string);

  socket.on('rating_updated', async (data) => {
    if (String(data.event_id) === String(eventId)) {
      const newBeerData = await beerService.eventBeer.toplistBeersInEvent(eventId as string);
      event_beers.value = newBeerData.response || [];
    }
  });

  socket.on('beer_added', async (data) => {
    if (String(data.event_id) === String(eventId)) {
      const newBeerData = await beerService.eventBeer.toplistBeersInEvent(eventId as string);
      event_beers.value = newBeerData.response || [];
    }
  });
});

onUnmounted(() => {
  socket.off('rating_updated');
});


// Modal state
const showModal = ref(false);
const ratingModal = ref(false);
const viewRatingsModal = ref(false);
const selectedBeerForRating = ref<Beer | null>(null);

// Add Beer Modal functions
const openModal = async () => {
  showModal.value = true;
};
const closeModal = () => {
  showModal.value = false;
};

// Rating Modal functions
const openRatingModal = (beer: Beer) => {
  selectedBeerForRating.value = beer;
  ratingModal.value = true;
};
const closeRatingModal = () => {
  ratingModal.value = false;
  selectedBeerForRating.value = null;
};

const openViewRatingModal = (beer: Beer) => {
  selectedBeerForRating.value = beer;
  viewRatingsModal.value = true;
};
const closeViewRatingsModal = () => {
  viewRatingsModal.value = false;
  selectedBeerForRating.value = null;
};
</script>

<template>
  <h1 class="text-center">Event page</h1>
  <div class="beerContainer max-w-3xl m-auto mb-5">
    <div class="flex justify-between pb-5 items-center">
      <h3 class="text-lg font-semibold">Beers</h3>
      <button class="yellow" @click="openModal">Add Beer to Event</button>
    </div>
    <div v-if="beersPending">Loading beers...</div>
    <div v-if="event_beers">
      <div v-for="beer in event_beers" :key="beer.id">
        <BeerCard :beer="beer" @add-rating="openRatingModal" @view-ratings="openViewRatingModal" />
      </div>
    </div>
  </div>

  <!-- Modals -->
  <AddBeerModal v-if="showModal" @close="closeModal" />
  <AddRatingModal v-if="ratingModal" :beer="selectedBeerForRating" :eventId="eventId" @close="closeRatingModal" />
  <ViewRatingsModal v-if="viewRatingsModal" :beer="selectedBeerForRating" @close="closeViewRatingsModal" />  
</template>
