<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useFetch } from '#app';
import BeerCard from '~/components/beerCard.vue';
import type { Beer, Participants, ResponseTypeBeers, ResponseTypeParticipants } from '~/types/types';
import beerService from '~/services/BeerService/beerService';

const route = useRoute();
const eventId = route.params.id;

// Use useFetch for SSR and immediate data loading
const { data: event_beers, pending: beersPending, error: beersError } = await beerService.eventBeer.allBeersInEvent(eventId as string);
const { data: event_participants, pending: participantsPending, error: participantsError } = await beerService.eventParticipants.getEventParticipants(eventId as string);

// Modal state
const showModal = ref(false);
const beerName = ref('');
const beerDescription = ref('');
const beerBrewery = ref('');
const beerType = ref('');

// For adding existing beers
const existingBeers = ref<Beer[]>([]);
const selectedBeerId = ref('');

const openModal = async () => {
  // Fetch all beers in the system (not just event beers)
  // Example: existingBeers.value = await beerService.beer.getAllBeers();
  showModal.value = true;
};
const closeModal = () => {
  showModal.value = false;
  beerName.value = '';
  beerDescription.value = '';
  beerBrewery.value = '';
  beerType.value = '';
  selectedBeerId.value = '';
};
const saveBeer = () => {
  // Add logic to save the beer (API call)
  // Example: beerService.eventBeer.addBeerToEvent(eventId, { name: beerName.value, description: beerDescription.value, brewery: beerBrewery.value, type: beerType.value })
  closeModal();
};
const addExistingBeerToEvent = () => {
  // Add logic to add selected beer to event (API call)
  // Example: beerService.eventBeer.addBeerToEvent(eventId, { beerId: selectedBeerId.value })
  closeModal();
};
</script>

<template>
  <h1 class="text-center">Event page</h1>
  <div class="beerContainer max-w-3xl m-auto">
    <div class="flex justify-between pb-5">
      <p>Øl</p>
      <button @click="openModal">Ny øl / Legg til eksisterende øl</button>
    </div>
    <div v-if="beersPending">Loading beers...</div>
    <div v-if="event_beers" v-for="beer in event_beers.response">
      <BeerCard :beer="beer"/>
    </div>
  </div>

  <!-- Unified Modal for Adding Beer -->
  <div v-if="showModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white p-6 rounded shadow-lg w-96">
      <h2 class="text-xl mb-4">Add Beer to Event</h2>
      <div class="mb-6">
        <h3 class="font-semibold mb-2">Add New Beer</h3>
        <label class="block mb-2">Name</label>
        <input v-model="beerName" class="border p-2 w-full mb-2" placeholder="Beer name" />
        <label class="block mb-2">Description</label>
        <input v-model="beerDescription" class="border p-2 w-full mb-2" placeholder="Description" />
        <label class="block mb-2">Brewery</label>
        <input v-model="beerBrewery" class="border p-2 w-full mb-2" placeholder="Brewery" />
        <label class="block mb-2">Type</label>
        <input v-model="beerType" class="border p-2 w-full mb-4" placeholder="Type" />
        <button @click="saveBeer" class="px-4 py-2 bg-blue-500 text-white rounded w-full mb-2">Save New Beer</button>
      </div>
      <div>
        <h3 class="font-semibold mb-2">Add Existing Beer</h3>
        <label class="block mb-2">Select Beer</label>
        <select v-model="selectedBeerId" class="border p-2 w-full mb-4">
          <option value="" disabled>Select a beer</option>
          <option v-for="beer in existingBeers" :key="beer.id" :value="beer.id">{{ beer.name }}</option>
        </select>
        <button @click="addExistingBeerToEvent" class="px-4 py-2 bg-green-500 text-white rounded w-full mb-2" :disabled="!selectedBeerId">Add Existing Beer</button>
      </div>
      <div class="flex justify-end mt-4">
        <button @click="closeModal" class="px-4 py-2 bg-gray-300 rounded">Close</button>
      </div>
    </div>
  </div>
</template>
