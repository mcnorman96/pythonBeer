<script setup lang="ts">
import type { EventInterface } from '~/types/types';

interface ResponseType {
  response: Array<EventInterface>;
}

const props = defineProps<{
  event: any;
}>();

const event = props.event || '';
const newDate = new Date(event.start_date);
const eventDate = newDate.toLocaleDateString();

// Define refs to store the data, error, and pending state
const event_beers = ref<ResponseType | null>(null);
const error = ref<Error | null>(null);
const pending = ref<boolean>(true);

onMounted(async () => {
  const { data: fetchedData, error: fetchError, pending: fetchPending } = await useFetch<ResponseType>(`http://127.0.0.1:5000/events/${event.id}/beers`);
  event_beers.value = fetchedData.value;
  error.value = fetchError.value;
  pending.value = fetchPending.value;
});
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
    <div class="rightside" v-if="event_beers" v-for="beers in event_beers.response">
      1. {{ beers.name }}
    </div>
  </NuxtLink>
</template>