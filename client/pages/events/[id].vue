<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import BeerCard from '~/components/beerCard.vue';
import AddRatingModal from '~/components/modals/addRatingModal.vue';
import AddBeerModal from '~/components/modals/addBeerModal.vue';
import ViewRatingsModal from '~/components/modals/viewRatingsModal.vue';
import EditEventModal from '~/components/modals/editEventModal.vue';
import EditBeerModal from '~/components/modals/editBeerModal.vue';
import type { Beer, ResponseTypeBeers, Event } from '~/types/types';
import beerService from '~/services/BeerService/beerService';
import { onMounted, onUnmounted } from 'vue';
import { socket } from '~/services/vars';
import Button from '~/components/ui/Button.vue';
import { useModalManager } from '~/composables/useModalManager';

const route = useRoute();
const eventId = route.params.id;
const event_beers = ref<Beer[]>([]);
const event_data = ref<Event | null>(null);
const event_ended = ref<boolean>(false);
const sortOption = ref<string>('new');
const beersPending = ref<boolean>(false);
const { modalState, openModal, closeModal } = useModalManager();

const fetchBeersinEvent: () => Promise<void> = async () => {
  beersPending.value = true;
  const beerData: ResponseTypeBeers = await beerService.eventBeer.toplistBeersInEvent(
    eventId as string
  );
  if (beerData.success && beerData.response) {
    event_beers.value = beerData.response;
  }
  beersPending.value = false;
};

const fetchEventData: () => Promise<void> = async () => {
  const eventData = await beerService.events.getEventById(eventId as string);
  if (eventData?.data?.value?.response) {
    event_data.value = eventData.data.value.response;
    event_ended.value = eventData.data.value.response.end_date < new Date().toISOString();
  }
};

const sortBeers: () => void = () => {
  if (Array.isArray(event_beers.value)) {
    let sorted = [...event_beers.value];
    if (sortOption.value === 'new') {
      sorted.sort((a: Beer, b: Beer) => a.event_beer_id - b.event_beer_id);
    } else if (sortOption.value === 'top') {
      sorted.sort((a: Beer, b: Beer) => Number(b.average_score) - Number(a.average_score));
    }
    event_beers.value = sorted;
  }
};

watch(sortOption, () => {
  sortBeers();
});

onMounted(async () => {
  await fetchBeersinEvent();
  await fetchEventData();

  socket.on('rating_updated', async (data: Event) => {
    if (String(data.event_id) === String(eventId)) {
      await fetchBeersinEvent();
      sortBeers();
    }
  });

  socket.on('beers_in_event_updated', async (data: Event) => {
    if (String(data.event_id) === String(eventId)) {
      await fetchBeersinEvent();
      sortBeers();
    }
  });

  socket.on('beer_updated', async (data: Beer) => {
    const containsBeer = event_beers.value.some((beer) => {
      return beer.id === data.beer.id;
    });

    if (containsBeer) {
      await fetchBeersinEvent();
      sortBeers();
    }
  });

  socket.on('event_updated', async (data: Event) => {
    if (String(data.event.id) === String(eventId)) {
      await fetchEventData();
    }
  });
});

onUnmounted(() => {
  socket.off('rating_updated');
  socket.off('beers_in_event_updated');
  socket.off('event_updated');
  socket.off('beer_updated');
});
</script>

<template>
  <h1 class="text-center">{{ event_data?.name }}</h1>
  <p class="text-center mb-5">{{ event_data?.description }}</p>
  <div class="beerContainer max-w-3xl m-auto mb-5">
    <div v-if="event_beers">
      <div class="flex justify-between mb-4">
        <select class="p-2 border border-gray-300 rounded" v-model="sortOption">
          <option value="new">Newest</option>
          <option value="top">Top Rated</option>
        </select>
        <Button
          edit
          :class="'ml-2 px-4 py-2 bg-zinc-800 text-white rounded'"
          @click="openModal('editEvent')"
          >Edit event</Button
        >
      </div>
      <div v-for="beer in event_beers" :key="beer.id">
        <BeerCard
          :buttonsAvailable="event_ended ? false : true"
          :beer="beer"
          @add-rating="() => openModal('addRating', beer)"
          @view-ratings="() => openModal('viewRatings', beer)"
          @edit-beer="() => openModal('editBeer', beer)"
        />
      </div>
    </div>
    <div v-if="beersPending" class="text-center">Loading beers...</div>
    <div class="text-center" v-if="event_beers.length === 0">No beers in this event yet.</div>
    <Button
      color="yellow"
      v-if="!event_ended"
      :class="'mt-5 ml-auto block'"
      @click="openModal('addBeer')"
      >Add Beer to Event</Button
    >
  </div>

  <!-- Modals -->
  <EditBeerModal
    v-if="modalState.type === 'editBeer'"
    :beer="modalState.beer"
    @close="closeModal"
  />
  <EditEventModal v-if="modalState.type === 'editEvent'" @close="closeModal" />
  <AddBeerModal v-if="modalState.type === 'addBeer'" @close="closeModal" />
  <AddRatingModal
    v-if="modalState.type === 'addRating'"
    :beer="modalState.beer"
    :eventId="eventId"
    @close="closeModal"
  />
  <ViewRatingsModal
    v-if="modalState.type === 'viewRatings'"
    :beer="modalState.beer"
    @close="closeModal"
  />
</template>
