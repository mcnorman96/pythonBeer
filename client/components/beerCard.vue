<script setup lang="ts">
import RatingCircle from './ratingCircle.vue';
const props = defineProps<{
  beer: any;
}>();

const emit = defineEmits(['add-rating']);

const beer = props.beer || '';
const taste = props.beer.average_taste || 0;
const aftertaste = props.beer.average_aftertaste || 0;
const smell = props.beer.average_smell || 0;
const bottle_design = props.beer.average_design || 0;
const average_score = props.beer.average_score || 0;

const handleAddRating = () => {
  emit('add-rating', beer);
};
</script>

<template>
  <div class="flex justify-between py-5 border-t border-t-black">
   <div class="name">
    {{ beer.name }}
   </div>
   <div class="rightside">
    <div class="flex -mr-6">
      <RatingCircle :rating="taste" name="Smag"/>
      <RatingCircle :rating="aftertaste" name="Eftersmag"/>
      <RatingCircle :rating="smell" name="Duft"/>
      <RatingCircle :rating="bottle_design" name="Flaskedesign"/>
      <RatingCircle :rating="average_score" name="Score"/>
    </div>
   <button @click="handleAddRating" class="ml-auto block pt-3">Add rating</button>
   </div>
  </div>
</template>