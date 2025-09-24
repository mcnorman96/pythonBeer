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

const { data: event_beers, pending: beersPending, error: beersError } = await beerService.eventBeer.toplistBeersInEvent(event.id as string);
</script>

<template>
  <NuxtLink :to="{ name: 'events-id', params: { id: event.id } }" class="mt-5 flex flex-wrap justify-between bg-white border-gray-400 border-solid shadow-md rounded-2xl p-6 hover:shadow-lg transition" style="border-width: 0.5px;">
    <div class="leftside">
      <div class="date">
        {{ eventDate }}
      </div>
      <div class="name font-bold">    
        {{ event.name }}
      </div>
      <div class="description text-sm">
        {{ event.description }}
      </div>
    </div>
    <div class="rightside" v-if="event_beers">
      <div class="col" v-for="(beers, index) in event_beers.response.slice(0, 3)" :key="index">
        {{ index + 1 }}. {{ beers.name }}
      </div>
    </div>
  </NuxtLink>
</template>