<script setup lang="ts">
import { ref } from 'vue';
import { watch } from 'vue';
import type { Beer, newBeer } from '~/types/types';
import beerService from '~/services/BeerService/beerService';
import Button from '~/components/ui/Button.vue';

const route = useRoute();
const eventId: string = route.params.id;
const emit = defineEmits<{ (e: 'close'): void; (e: 'save'): void }>();

const beerName = ref<string>('');
const beerDescription = ref<string>('');
const beerBrewery = ref<string>('');
const beerType = ref<string>('');

const filteredBeers = ref<Beer[]>([]);
const selectedBeerId = ref<Beer | null>(null);
const beerSearch = ref<string>('');
const showDropdown = ref<boolean>(false);
const error = ref<string | null>(null);

watch(beerSearch, async (val: string) => {
  if (val.length < 3) {
    filteredBeers.value = [];
    showDropdown.value = false;
    return;
  }
  const { data: searchedBeers }: Beer[] = await beerService.eventBeer.searchBeer(val);

  filteredBeers.value = searchedBeers.value?.response || [];
  showDropdown.value = filteredBeers.value.length > 0;
});

const handleClose = () => {
  emit('close');
  beerName.value = '';
  beerDescription.value = '';
  beerBrewery.value = '';
  beerType.value = '';
  selectedBeerId.value = null;
  beerSearch.value = '';
  showDropdown.value = false;
  filteredBeers.value = [];
};

const saveBeer = async () => {
  try {
    if (!beerName.value || !beerDescription.value || !beerBrewery.value || !beerType.value) {
      error.value = 'All fields are required to create a new beer.';
      console.error('All fields are required to create a new beer.');
      return;
    }

    const createBeer: Response = await beerService.eventBeer.newBeer({
      name: beerName.value,
      description: beerDescription.value,
      brewery: beerBrewery.value,
      type: beerType.value,
    });

    if (!createBeer.success || !createBeer.response) {
      error.value = 'Failed to create beer.';
      console.error('Failed to create beer:', createBeer.error);
      return;
    }

    const beerIdString: string = createBeer.response.id.toString();
    const addBeerToEvent: Response = await beerService.eventBeer.addBeerToEvent(
      eventId as string,
      beerIdString
    );

    if (!addBeerToEvent.success) {
      console.error(addBeerToEvent.error);
    }
  } catch (error) {
    error.value = 'An error occurred while creating or adding the beer.';
    console.error('Error creating or adding beer:', error);
  }

  handleClose();
};

const addExistingBeerToEvent = async (beerId: number) => {
  const beerIdString = beerId.toString();
  const addBeerToEvent = await beerService.eventBeer.addBeerToEvent(
    eventId as string,
    beerIdString
  );

  if (!addBeerToEvent.success) {
    error.value = addBeerToEvent.error;
    return;
  }
  handleClose();
};
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white p-6 rounded shadow-lg w-96 relative m-2 max-h-[80vh] overflow-y-auto">
      <Button close @click="handleClose" :class="'rounded absolute top-2 right-2'"></Button>
      <h2 class="text-xl mb-4">Add Beer to Event</h2>

      <div class="mb-6 relative">
        <h3 class="font-semibold mb-2">Add Existing Beer</h3>
        <input
          name="beerSearch"
          v-model="beerSearch"
          class="border p-2 w-full mb-2"
          placeholder="Search for beer..."
          @focus="showDropdown = filteredBeers.length > 0"
          @blur="() => setTimeout(() => (showDropdown = false), 200)"
        />
        <ul
          v-if="showDropdown"
          class="absolute left-0 right-0 bg-white border rounded shadow z-10 max-h-48 overflow-auto"
        >
          <li
            v-for="beer in filteredBeers"
            :key="beer.id"
            @mousedown.prevent="addExistingBeerToEvent(beer.id)"
            class="px-4 py-2 cursor-pointer hover:bg-gray-100"
          >
            {{ beer.name }}
          </li>
        </ul>
      </div>

      <div>
        <h3 class="font-semibold mb-2">Add New Beer</h3>
        <label class="block mb-2">Name</label>
        <input
          name="name"
          v-model="beerName"
          class="border p-2 w-full mb-2"
          placeholder="Beer name"
        />
        <label class="block mb-2">Description</label>
        <input
          name="description"
          v-model="beerDescription"
          class="border p-2 w-full mb-2"
          placeholder="Description"
        />
        <label class="block mb-2">Brewery</label>
        <input
          name="brewery"
          v-model="beerBrewery"
          class="border p-2 w-full mb-2"
          placeholder="Brewery"
        />
        <label class="block mb-2">Type</label>
        <input name="type" v-model="beerType" class="border p-2 w-full mb-4" placeholder="Type" />
        <Button @click="saveBeer" color="yellow" :class="'px-4 py-2 rounded w-full mb-2'"
          >Save New Beer</Button
        >
      </div>

      <div v-if="error" class="text-red-500 mt-2">{{ error }}</div>
    </div>
  </div>
</template>
