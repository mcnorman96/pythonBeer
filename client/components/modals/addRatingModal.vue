<script setup lang="ts">
import { ref } from 'vue';
import beerService from '~/services/BeerService/beerService';
import type { Beer, Rating } from '~/types/types';
import Button from '~/components/ui/Button.vue';

const props = defineProps<{ beer: Beer }>();
const emit = defineEmits<{(e: 'close'): void}>();
const route = useRoute();
const eventId = route.params.id;

const getRating = ref<Rating | null>(null);
const taste = ref<number | undefined>(undefined);
const aftertaste = ref<number | undefined>(undefined);
const smell = ref<number | undefined>(undefined);
const design = ref<number | undefined>(undefined);
const total_score = ref<number | undefined>(undefined);
const errorMsg = ref<string | null>(null);

const errors = ref<{ [key: string]: string }>({
  taste: '',
  aftertaste: '',
  smell: '',
  design: '',
  total_score: ''
});

onMounted(async () => {
  const rating: Response<Rating> = await beerService.ratings.getRating(eventId as string, props.beer.id);
  getRating.value = rating.response;
});

watch(getRating, (beerRated: Response<Rating>) => {
  if (beerRated && beerRated.response) {
    taste.value = beerRated.response.taste;
    aftertaste.value = beerRated.response.aftertaste;
    smell.value = beerRated.response.smell;
    design.value = beerRated.response.design;
    total_score.value = beerRated.response.score;
  }
}, { immediate: true });

const validate = () => {
  errors.value.taste = taste.value === undefined || taste.value < 0 || taste.value > 5 ? 'Taste must be between 0 and 5' : '';
  errors.value.aftertaste = aftertaste.value === undefined || aftertaste.value < 0 || aftertaste.value > 5 ? 'Aftertaste must be between 0 and 5' : '';
  errors.value.smell = smell.value === undefined || smell.value < 0 || smell.value > 5 ? 'Smell must be between 0 and 5' : '';
  errors.value.design = design.value === undefined || design.value < 0 || design.value > 5 ? 'Design must be between 0 and 5' : '';
  errors.value.total_score = total_score.value === undefined || total_score.value < 0 || total_score.value > 5 ? 'Total score must be between 0 and 5' : '';
  return Object.values(errors.value).every(e => !e);
}

const handleSave = async () => {
  if (!validate()) {
    errorMsg.value = 'Please fix validation errors.';
    return;
  }

  const saveRating = await beerService.ratings.addRating({
    event_id: eventId,
    beer_id: props.beer.id,
    taste: taste.value!,
    aftertaste: aftertaste.value!,
    smell: smell.value!,
    design: design.value!,
    score: total_score.value!
  });

  if (saveRating.errorMsg) {
    errorMsg.value = saveRating.errorMsg;
    return;
  } else {
    errorMsg.value = null;
    emit('close');
  }
};

const handleClose = () => {
  emit('close');
};
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white p-6 rounded shadow-lg w-96 relative m-2 max-h-[80vh] overflow-y-auto">
      <Button close @click="handleClose" :class="'absolute top-2 right-2'"></Button>
      <h2 class="text-xl mb-4">Rate {{ props.beer.name }}</h2>
      <div class="mb-4">
        <label class="block mb-2">Taste</label>
        <input v-model="taste" type="number" min="0" max="5" step="0.1" class="border p-2 w-full mb-2" placeholder="Taste" />
        <div v-if="errors.taste" class="text-red-500 text-xs mb-2">{{ errors.taste }}</div>
        <label class="block mb-2">Aftertaste</label>
        <input v-model="aftertaste" type="number" min="0" max="5" step="0.1" class="border p-2 w-full mb-2" placeholder="Aftertaste" />
        <div v-if="errors.aftertaste" class="text-red-500 text-xs mb-2">{{ errors.aftertaste }}</div>
        <label class="block mb-2">Smell</label>
        <input v-model="smell" type="number" min="0" max="5" step="0.1" class="border p-2 w-full mb-2" placeholder="Smell" />
        <div v-if="errors.smell" class="text-red-500 text-xs mb-2">{{ errors.smell }}</div>
        <label class="block mb-2">Design</label>
        <input v-model="design" type="number" min="0" max="5" step="0.1" class="border p-2 w-full mb-2" placeholder="Design" />
        <div v-if="errors.design" class="text-red-500 text-xs mb-2">{{ errors.design }}</div>
        <label class="block mb-2">Total score</label>
        <input v-model="total_score" type="number" min="0" max="5" step="0.1" class="border p-2 w-full mb-2" placeholder="Total Score" />
        <div v-if="errors.total_score" class="text-red-500 text-xs mb-2">{{ errors.total_score }}</div>
      </div>
      <div class="flex justify-end space-x-2">
        <Button color="yellow" @click="handleSave" class="w-full savebtn ">Save</Button>
      </div>
      <div v-if="errorMsg" class="mt-4 text-red-500">
        {{ errorMsg }}
      </div>
    </div>
  </div>
</template>