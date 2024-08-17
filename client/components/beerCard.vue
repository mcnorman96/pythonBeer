<script setup lang="ts">
import RatingCircle from './ratingCircle.vue';

const props = defineProps<{
  beer: any;
}>();

const beer = props.beer || '';
const currentRating = 7.5;
</script>

<template>
  <div class="flex justify-between py-5 border-t border-t-black">
   <div class="name">
    {{ beer.name }}
   </div>
   <div class="rigthside flex">
    <RatingCircle :rating="currentRating" name="Smag"/>
    <RatingCircle :rating="currentRating" name="Eftersmag"/>
    <RatingCircle :rating="currentRating" name="Duft"/>
    <RatingCircle :rating="currentRating" name="Flaskedesign"/>
    <RatingCircle :rating="currentRating" name="Score"/>
   </div>
  </div>
</template>