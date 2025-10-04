<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useFetch } from '#app';
import BeerCard from '~/components/beerCard.vue';
import AddRatingModal from '~/components/modals/AddRatingModal.vue';
import AddBeerModal from '~/components/modals/AddBeerModal.vue';
import ViewRatingsModal from '~/components/modals/ViewRatingsModal.vue';
import EditEventModal from '~/components/modals/editEventModal.vue';
import type { Beer, Participants, ResponseTypeBeers, ResponseTypeParticipants, Event } from '~/types/types';
import beerService from '~/services/BeerService/beerService';
import { onMounted, onUnmounted } from 'vue';
import { socket } from '~/services/vars';
import Button from '~/components/ui/Button.vue';

const route = useRoute();
const eventId = route.params.id;
const event_beers = ref<Beer[]>([]);
const event_data = ref<Event | null>(null);
const event_ended = ref<boolean>(false);
const sortOption = ref<string>('new');

const fetchBeersinEvent: () => Promise<void> = async () => {
  const beerData: ResponseTypeBeers = await beerService.eventBeer.toplistBeersInEvent(eventId as string);
  if (beerData.success && beerData.response) {
      event_beers.value = beerData.response;
  }
}

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

watch(sortOption, (newVal: string) => {
  sortBeers();
});

onMounted(async () => {
  await fetchBeersinEvent();

  const eventData = await beerService.events.getEventById(eventId as string);
  if (eventData?.data?.value?.response) {
    event_data.value = eventData.data.value.response;
    event_ended.value = eventData.data.value.response.end_date < new Date().toISOString();
  }
  
  socket.on('rating_updated', async (data: Event) => {
    if (String(data.event_id) === String(eventId)) {
      await fetchBeersinEvent();
      sortBeers();
    }
  });

  socket.on('beer_added', async (data: Event) => {
    if (String(data.event_id) === String(eventId)) {
      await fetchBeersinEvent();
      sortBeers();
    }
  });
});

onUnmounted(() => {
  socket.off('rating_updated');
});


// Modal state
const showModal = ref<boolean>(false);
const showEditEventModal = ref<boolean>(false);
const ratingModal = ref<boolean>(false);
const viewRatingsModal = ref<boolean>(false);
const selectedBeerForRating = ref<Beer | null>(null);

// Add Beer Modal functions
const openModal = async () => {
  showModal.value = true;
};
const closeModal = () => {
  showModal.value = false;
};

// Rating Modal functions
const openRatingModal = (beer: Beer) => {
  selectedBeerForRating.value = beer;
  ratingModal.value = true;
};
const closeRatingModal = () => {
  ratingModal.value = false;
  selectedBeerForRating.value = null;
};

const openViewRatingModal = (beer: Beer) => {
  selectedBeerForRating.value = beer;
  viewRatingsModal.value = true;
};
const closeViewRatingsModal = () => {
  viewRatingsModal.value = false;
  selectedBeerForRating.value = null;
};

const openEditEventModal = async () => {
  showEditEventModal.value = true;
};
const closeEditEventModal = () => {
  showEditEventModal.value = false;
};
</script>

<template>
  <h1 class="text-center">{{ event_data?.name }}</h1>
  <p class="text-center mb-5">{{ event_data?.description }}</p>
  <div class="beerContainer max-w-3xl m-auto mb-5">
    <div v-if="beersPending">Loading beers...</div>
    <div class="text-center" v-if="event_beers.length === 0 && !beersPending">No beers in this event yet.</div>
    <div v-if="event_beers">
      <div class="flex justify-between mb-4">
        <select class="p-2 border border-gray-300 rounded" v-model="sortOption">
          <option value="new">Newest</option>
          <option value="top">Top Rated</option>
        </select>
        <Button edit :class="'ml-2 px-4 py-2 bg-zinc-800 text-white rounded'" @click="openEditEventModal">Edit event</Button>
      </div>
      <div v-for="beer in event_beers" :key="beer.id">
        <BeerCard :buttonsAvailable="event_ended ? false : true"  :beer="beer" @add-rating="openRatingModal" @view-ratings="openViewRatingModal" />
      </div>
    </div>
    <Button color="yellow" v-if="!event_ended" :class="'mt-5 ml-auto block'" @click="openModal">Add Beer to Event</Button>
  </div>

  <!-- Modals -->
  <EditEventModal v-if="showEditEventModal" @close="closeEditEventModal" />
  <AddBeerModal v-if="showModal" @close="closeModal" />
  <AddRatingModal v-if="ratingModal" :beer="selectedBeerForRating" :eventId="eventId" @close="closeRatingModal" />
  <ViewRatingsModal v-if="viewRatingsModal" :beer="selectedBeerForRating" @close="closeViewRatingsModal" />  
</template>
