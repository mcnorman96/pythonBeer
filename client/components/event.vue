<script setup lang="ts">
import type { Event, Beer } from '~/types/types';
import beerService from '~/services/BeerService/beerService';
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const props = defineProps<{
  event: Event | null;
}>();

const event = props.event || '';
const newDate = new Date(event.start_date);
const eventDate = newDate.toLocaleDateString();
const event_beers = ref<Beer[]>([]);
const event_status = ref('');

if (event) {
  event_status.value = event.end_date < new Date().toISOString() ? 'Ended' : 'Active';
}

onMounted(async () => {
  const beerData = await beerService.eventBeer.toplistBeersInEvent(event.id as string);
  if (beerData.success && beerData.response) {
    event_beers.value = beerData.response;
  }
});

const getTrophy = (position: number) => {
  if (position === 1) return 'gold.svg';
  if (position === 2) return 'silver.svg';
  if (position === 3) return 'bronze.svg';
  return '';
};
</script>

<template>
  <NuxtLink
    :to="`/events/${event.id}`"
    class="mt-5 flex flex-wrap justify-between bg-white border-gray-400 border-solid shadow-md rounded-2xl p-6 hover:shadow-lg transition"
    style="border-width: 0.5px"
  >
    <div class="leftside">
      <div class="date text-xs flex items-center">
        <div class="mr-1">{{ eventDate }} →</div>
        <div
          :class="
            'status text-xs ' + (event_status === 'Active' ? 'text-green-600' : 'text-red-600')
          "
        >
          {{ t(event_status) }}
        </div>
      </div>
      <div class="name font-bold">
        {{ event.name }}
      </div>
      <div class="description text-sm">
        {{ event.description }}
      </div>
    </div>
    <div class="rightside flex flex-col justify-center" v-if="event_beers">
      <div
        class="col flex text-sm items-center"
        v-for="(beers, index) in event_beers.slice(0, 3)"
        :key="index"
      >
        <img class="mr-2 h-5" :src="'img/' + getTrophy(index + 1)" />
        {{ beers.name }}
      </div>
    </div>
  </NuxtLink>
</template>
