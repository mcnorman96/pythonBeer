<script setup lang="ts">
import { ref } from 'vue';
import { watch } from 'vue';
import type { Beer } from '~/types/types';
import beerService from '~/services/BeerService/beerService';

const route = useRoute();
const eventId = route.params.id;
const emit = defineEmits(['close', 'save']);

const beerName = ref('');
const beerDescription = ref('');
const beerBrewery = ref('');
const beerType = ref('');

// For adding existing beers
const filteredBeers = ref<Beer[]>([]);
const selectedBeerId = ref('');
const beerSearch = ref('');
const showDropdown = ref(false);

watch(beerSearch, async (val) => {
  if (val.length < 2) {
    filteredBeers.value = [];
    showDropdown.value = false;
    return;
  }
  const { data: searchedBeers } = await beerService.eventBeer.searchBeer(val);
  filteredBeers.value = searchedBeers.value || [];
  showDropdown.value = filteredBeers.value.length > 0;
});

const handleClose = () => {
  emit('close');
  beerName.value = '';
  beerDescription.value = '';
  beerBrewery.value = '';
  beerType.value = '';
  selectedBeerId.value = '';
  beerSearch.value = '';
  showDropdown.value = false;
  filteredBeers.value = [];
};

const saveBeer = async () => {
  try {
    const createBeer = await beerService.eventBeer.newBeer({
      name: beerName.value,
      description: beerDescription.value,
      brewery: beerBrewery.value,
      type: beerType.value
    });

    const beerIdString = createBeer.data.beer.id.toString();
    const addBeerToEvent = await beerService.eventBeer.addBeerToEvent(eventId as string, beerIdString);

    if (!addBeerToEvent.success) {
      // Handle error
      console.error(addBeerToEvent.error);
    }
  } catch (error) {
    console.error('Error creating or adding beer:', error);
  }
  
  handleClose();
};

const addExistingBeerToEvent = async (beerId: number) => {
  const beerIdString = beerId.toString();
  const addBeerToEvent = await beerService.eventBeer.addBeerToEvent(eventId as string, beerIdString);
  
  if (!addBeerToEvent.success) {
    // Handle error
    console.error(addBeerToEvent.error);
  }
  handleClose();
};

</script>

<template>
    <!-- Unified Modal for Adding Beer -->
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white p-6 rounded shadow-lg w-96">
      <h2 class="text-xl mb-4">Add Beer to Event</h2>
      <!-- Add Existing Beer Search with Dropdown -->
      <div class="mb-6 relative">
        <h3 class="font-semibold mb-2">Add Existing Beer</h3>
        <input v-model="beerSearch" class="border p-2 w-full mb-2" placeholder="Search for beer..." @focus="showDropdown = filteredBeers.length > 0" @blur="setTimeout(() => showDropdown = false, 200)" />
        <ul v-if="showDropdown" class="absolute left-0 right-0 bg-white border rounded shadow z-10 max-h-48 overflow-auto">
          <li v-for="beer in filteredBeers" :key="beer.id" @mousedown.prevent="addExistingBeerToEvent(beer.id)" class="px-4 py-2 cursor-pointer hover:bg-gray-100">{{ beer.name }}</li>
        </ul>
      </div>
      <div>
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
      <div class="flex justify-end mt-4">
        <button @click="closeModal" class="px-4 py-2 bg-gray-300 rounded">Close</button>
      </div>
    </div>
  </div>
</template>