<script setup lang="ts">
import RatingCircle from './ratingCircle.vue';
import { computed } from 'vue';

const props = defineProps<{
  beer: any;
}>();

const emit = defineEmits(['add-rating']);

const taste = computed(() => props.beer.average_taste || 0);
const aftertaste = computed(() => props.beer.average_aftertaste || 0);
const smell = computed(() => props.beer.average_smell || 0);
const bottle_design = computed(() => props.beer.average_design || 0);
const average_score = computed(() => {
  console.log(props.beer.average_score);
  return props.beer.average_score || 0;
});

const handleAddRating = () => {
  emit('add-rating', props.beer);
};
</script>

<template>
  <div class="flex justify-between py-5 border-t border-t-black">
   <div class="name">
    {{ props.beer.name }}
   </div>
   <div class="rightside">
    <div class="flex -mr-6">
      <RatingCircle :rating="taste" name="Taste"/>
      <RatingCircle :rating="aftertaste" name="Aftertaste"/>
      <RatingCircle :rating="smell" name="Smell"/>
      <RatingCircle :rating="bottle_design" name="Bottle Design"/>
      <RatingCircle :rating="average_score" name="Score"/>
    </div>
   <button @click="handleAddRating" class="ml-auto block pt-3">Add rating</button>
   </div>
  </div>
</template>