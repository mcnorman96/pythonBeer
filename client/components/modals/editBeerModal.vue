<script setup lang="ts">
import { ref } from 'vue';
import { watch } from 'vue';
import type { Beer, newBeer } from '~/types/types';
import beerService from '~/services/BeerService/beerService';
import Button from '~/components/ui/Button.vue';

const props = defineProps<{ beer: Beer }>();
const route = useRoute();
const eventId: string = route.params.id;
const emit = defineEmits<{ (e: 'close'): void }>();

const beerName = ref<string>('');
const beerDescription = ref<string>('');
const beerBrewery = ref<string>('');
const beerType = ref<string>('');

const error = ref<string | null>(null);

const handleClose = () => {
  emit('close');
  beerName.value = '';
  beerDescription.value = '';
  beerBrewery.value = '';
  beerType.value = '';
};

onMounted(() => {
  if (props.beer) {
    beerName.value = props.beer.name;
    beerDescription.value = props.beer.description;
    beerBrewery.value = props.beer.brewery;
    beerType.value = props.beer.type;
  }
});

const updateBeer = async () => {
  const BeerObj: Beer = {
    id: props.beer.id,
    name: beerName.value,
    description: beerDescription.value,
    brewery: beerBrewery.value,
    type: beerType.value,
  };

  const updateBeer = await beerService.eventBeer.updateBeer(BeerObj);

  if (!updateBeer.success) {
    error.value = updateBeer.error;
    return;
  }
  handleClose();
};

const handleDeleteBeerFromEvent = () => {
  const deleteBeerFromEvent = beerService.eventBeer.deleteBeerFromEvent(props.beer.id, eventId);

  if (!deleteBeerFromEvent) {
    error.value = deleteBeerFromEvent.error;
    return;
  }

  handleClose();
};
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white p-6 rounded shadow-lg w-96 relative m-2 max-h-[80vh] overflow-y-auto">
      <Button close @click="handleClose" :class="'rounded absolute top-2 right-2'"></Button>
      <h2 class="text-xl mb-4">Update beer</h2>

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

      <Button @click="updateBeer" color="yellow" :class="'w-full mb-2'">Update Beer</Button>
      <Button delete @click="handleDeleteBeerFromEvent" class="w-full"
        >Delete beer from event</Button
      >

      <div v-if="error" class="text-red-500 mt-2">{{ error }}</div>
    </div>
  </div>
</template>
