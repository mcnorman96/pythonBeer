<script setup lang="ts">
import { ref } from 'vue';
import beerService from '~/services/BeerService/beerService';

const props = defineProps<{ beer: any }>();
const emit = defineEmits(['close']);
const route = useRoute();
const eventId = route.params.id;

const { data: ratings, error, pending } = await beerService.ratings.getAllRatingsForBeer(eventId as string, props.beer.id);

const handleClose = () => {
  emit('close');
};
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white p-6 rounded shadow-lg w-120">
      <h2 class="text-xl mb-4">Ratings for {{ props.beer.name }}</h2>
      <div v-if="pending" class="mb-4">Loading ratings...</div>
      <div v-else-if="error" class="mb-4 text-red-500">Error loading ratings: {{ error.message }}</div>
      <div v-else-if="ratings && ratings.response.length === 0" class="mb-4">No ratings available.</div>
      <div v-else class="">
        <div v-for="rating in ratings.response" :key="rating.id" class="mb-2">
          <div class="flex justify-between py-5 border-t border-t-black">
            <div class="name mr-3 capitalize">
              {{ rating.username }}
            </div>
            <div class="rightside">
              <div class="flex -mr-6">
                <RatingCircle :rating="rating.taste" name="Taste"/>
                <RatingCircle :rating="rating.aftertaste" name="Aftertaste"/>
                <RatingCircle :rating="rating.smell" name="Smell"/>
                <RatingCircle :rating="rating.design" name="Bottle Design"/>
                <RatingCircle :rating="rating.score" name="Score"/>
              </div>
            </div>
          </div>
        </div>

    </div>
      <div class="flex justify-end space-x-2">
        <button @click="handleClose" class="px-4 py-2 bg-black text-white rounded">Close</button>
      </div>
    </div>
  </div>
</template>