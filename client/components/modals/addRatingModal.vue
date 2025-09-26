<script setup lang="ts">
import { ref } from 'vue';
import beerService from '~/services/BeerService/beerService';
import type { Beer } from '~/types/types';

const props = defineProps<{ beer: Beer }>();
const emit = defineEmits(['close']);
const route = useRoute();
const eventId = route.params.id;

const taste = ref(0);
const aftertaste = ref(0);
const smell = ref(0);
const design = ref(0);
const total_score = ref(0);

const { data: beerRating, error, pending } = await beerService.ratings.getRating(eventId as string, props.beer.id);

watch(beerRating, (beerRated) => {
  if (beerRated && beerRated.response) {
    taste.value = beerRated.response.taste;
    aftertaste.value = beerRated.response.aftertaste;
    smell.value = beerRated.response.smell;
    design.value = beerRated.response.design;
    total_score.value = beerRated.response.score;
  }
}, { immediate: true });

const handleSave = async () => {
  const saveRating = await beerService.ratings.addRating({
    event_id: eventId,
    beer_id: props.beer.id,
    taste: taste.value,
    aftertaste: aftertaste.value,
    smell: smell.value,
    design: design.value,
    score: total_score.value
  });
  emit('close');
};

const handleClose = () => {
  emit('close');
};
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white p-6 rounded shadow-lg w-96 relative m-2 max-h-[80vh] overflow-y-auto">
      <button @click="handleClose" class="bg-black text-white rounded absolute top-2 right-2">X</button>
      <h2 class="text-xl mb-4">Rate {{ props.beer.name }}</h2>
      <div class="mb-4">
        <label class="block mb-2">Taste</label>
        <input v-model="taste" type="number" min="0" max="5" step="0.1" class="border p-2 w-full mb-2" placeholder="Taste" />
        <label class="block mb-2">Aftertaste</label>
        <input v-model="aftertaste" type="number" min="0" max="5" step="0.1" class="border p-2 w-full mb-2" placeholder="Aftertaste" />
        <label class="block mb-2">Smell</label>
        <input v-model="smell" type="number" min="0" max="5" step="0.1" class="border p-2 w-full mb-2" placeholder="Smell" />
        <label class="block mb-2">Design</label>
        <input v-model="design" type="number" min="0" max="5" step="0.1" class="border p-2 w-full mb-2" placeholder="Design" />
        <label class="block mb-2">Total score</label>
        <input v-model="total_score" type="number" min="0" max="5" step="0.1" class="border p-2 w-full mb-2" placeholder="Total Score" />
      </div>
      <div class="flex justify-end space-x-2">
        <button @click="handleSave" class="px-4 py-2 w-full yellow rounded">Save</button>
      </div>
    </div>
  </div>
</template>