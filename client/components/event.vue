<script setup lang="ts">
import type { EventInterface } from '~/types/types';
import beerService from '~/services/BeerService/beerService';

interface ResponseType {
  response: Array<EventInterface>;
}

const props = defineProps<{
  event: any;
}>();

const event = props.event || '';
const newDate = new Date(event.start_date);
const eventDate = newDate.toLocaleDateString();

  // Use useFetch for SSR and immediate data loading
const { data: event_beers, pending: beersPending, error: beersError } = await beerService.eventBeer.toplistBeersInEvent(event.id as string);

</script>

<template>
  <NuxtLink :to="{ name: 'events-id', params: { id: event.id } }" class="flex justify-between pt-5 pb-5 border-t border-t-black">
    <div class="leftside">
      <div class="date">
        {{ eventDate }}
      </div>
      <div class="name font-bold">
        {{ event.name }}
      </div>
    </div>
    <div class="rightside" v-if="event_beers">
      <div class="col" v-for="(beers, index) in event_beers.response.slice(0, 3)" :key="index">
        {{ index + 1 }}. {{ beers.name }}
      </div>
    </div>
  </NuxtLink>
</template>