<script setup lang="ts">
import RatingCircle from './ratingCircle.vue';
import { computed } from 'vue';

const props = defineProps<{
  beer: any;
  toplist?: boolean;
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
  <div class="flex justify-between mt-5 bg-white border-gray-400 border-solid shadow-md rounded-2xl p-6" style="border-width: 0.5px;">
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
   <div class="rightside">
    <div class="flex -mr-6">
      <RatingCircle :rating="taste" name="Taste"/>
      <RatingCircle :rating="aftertaste" name="Aftertaste"/>
      <RatingCircle :rating="smell" name="Smell"/>
      <RatingCircle :rating="bottle_design" name="Bottle Design"/>
      <RatingCircle :rating="average_score" name="Score"/>
    </div>
    <div v-if="!props.toplist" class="flex w-max ml-auto mt-5">
      <button @click="$emit('view-ratings', props.beer)">View ratings</button>
      <button @click="handleAddRating" class="ml-5 yellow">Add rating</button>
   </div>
   </div>
  </div>
</template>