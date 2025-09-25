<script setup lang="ts">
import RatingCircle from './ratingCircle.vue';
import { computed } from 'vue';

const props = defineProps<{
  beer: any;
  buttonsAvailable: boolean | true;
}>();

const emit = defineEmits(['add-rating', 'view-ratings']);

const taste = computed(() => props.beer.average_taste || 0);
const aftertaste = computed(() => props.beer.average_aftertaste || 0);
const smell = computed(() => props.beer.average_smell || 0);
const bottle_design = computed(() => props.beer.average_design || 0);
const average_score = computed(() => props.beer.average_score || 0);

const handleAddRating = () => {
  emit('add-rating', props.beer);
};
</script>

<template>
  <div class="flex flex-wrap justify-between mt-5 bg-white border-gray-400 border-solid shadow-md rounded-2xl p-6" style="border-width: 0.5px;">
    <div class="leftside">
      <div class="name text-large font-bold">
        {{ props.beer.name }}
      </div>
      <div class="brewery text-sm">
        {{ props.beer.brewery }}
      </div>
      <div class="type text-sm">
        {{ props.beer.type }}
      </div>
      <div class="description text-sm">
        {{ props.beer.description }}
      </div>
   </div>
   <div class="rightside w-full md:w-auto">
    <div class="flex justify-between mt-5 mr-auto ml-auto md:ml-0 md:mt-0 md:-mr-6">
      <RatingCircle :rating="taste" name="Taste"/>
      <RatingCircle :rating="aftertaste" name="Aftertaste"/>
      <RatingCircle :rating="smell" name="Smell"/>
      <RatingCircle :rating="bottle_design" name="Design"/>
      <RatingCircle :rating="average_score" name="Score"/>
    </div>
    <div v-if="props.buttonsAvailable" class="flex md:w-max ml-auto mt-5">
      <button @click="$emit('view-ratings', props.beer)" class="w-1/2 md:w-auto">View ratings</button>
      <button @click="handleAddRating" class="ml-5 yellow w-1/2 md:w-auto">Add rating</button>
   </div>
   </div>
  </div>
</template>