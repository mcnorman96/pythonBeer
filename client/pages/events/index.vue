<script setup lang="ts">
import beerService from '~/services/BeerService/beerService';
import { ref, onMounted, onUnmounted } from 'vue';
import Event from '~/components/event.vue';
import Button from '~/components/ui/Button.vue';
import { socket } from '~/services/vars.ts';

const showModal = ref<boolean>(false);
const eventName = ref<string>('');
const eventDescription = ref<string>('');
const errorMsg = ref<string>('');
const events = ref<Array<Event>>([]);
const error = ref<string | null>(null);
const pending = ref<boolean>(false);

const openModal = () => {
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  eventName.value = '';
  eventDescription.value = '';
};

const saveEvent = async () => {
  const newEvent = await beerService.events.createEvent({
    name: eventName.value,
    description: eventDescription.value,
  });
  if (!newEvent.success) {
    errorMsg.value = newEvent.error || 'Failed to create event';
    return;
  }
  closeModal();
};

const fetchingEvents = async () => {
  pending.value = true;

  const getEvents = await beerService.events.getEvents();

  if (getEvents.success) {
    events.value = getEvents.response || [];
  }
  if (getEvents.error) {
    error.value = getEvents.error.message || 'Error fetching events';
  }

  pending.value = false;
};

onMounted(async () => {
  await fetchingEvents();

  socket.on('event_created', async () => {
    await fetchingEvents();
  });
});

onUnmounted(() => {
  socket.off('event_created');
});
</script>

<template>
  <h1 class="text-center">Events</h1>
  <Button color="yellow" class="text-center m-auto block" @click="openModal">New Event</Button>
  <div v-if="error" class="max-w-screen-md m-auto pt-5">{{ error }}</div>
  <div v-else-if="pending" class="max-w-screen-md m-auto pt-5">Loading...</div>
  <div class="max-w-screen-md m-auto pt-5" v-if="events.length < 1">
    No events to show
  </div>
  <div v-else class="max-w-screen-md m-auto">
    <div class="eventbody pt-5">
      <div v-for="event in events" :key="event.id">
        <Event :event="event" />
      </div>
    </div>
  </div>

  <!-- Add Event Modal -->
  <div
    v-if="showModal"
    class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
  >
    <div class="bg-white p-6 rounded shadow-lg w-96 relative">
      <Button close @click="closeModal" class="absolute top-2 right-2"></Button>
      <h2 class="text-xl mb-4">Add New Event</h2>
      <label class="block mb-2">Name</label>
      <input v-model="eventName" class="border p-2 w-full mb-4" placeholder="Event name" />
      <label class="block mb-2">Description</label>
      <input v-model="eventDescription" class="border p-2 w-full mb-4" placeholder="Description" />
      <div class="flex justify-end space-x-2">
        <Button @click="saveEvent" color="yellow" class="w-full">Save Event</Button>
      </div>
      <div v-if="errorMsg" class="text-red-500 mt-2">{{ errorMsg }}</div>
    </div>
  </div>
</template>
