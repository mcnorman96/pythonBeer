<script setup lang="ts">
import type { EventInterface } from '~/types/types';
import Event from './event.vue';
import { ref } from 'vue';
import beerService from '~/services/BeerService/beerService';

const props = defineProps<{
  data: { response: Array<EventInterface> };
  error: any;
  pending: any;
}>();

const showModal = ref(false);
const eventName = ref('');
const eventDescription = ref('');

const openModal = () => {
  showModal.value = true;
};
const closeModal = () => {
  showModal.value = false;
  eventName.value = '';
  eventDescription.value = '';
};
const saveEvent = () => {
  beerService.events.createEvent({ name: eventName.value, description: eventDescription.value });
  closeModal();
};

const data = ref(props.data);
const error = props.error;
const pending = props.pending;

</script>

<template>
  <div class="div">
    <div v-if="error">{{ error }}</div>
    <div v-else-if="pending">Loading...</div>
    <div v-else class=" max-w-screen-md m-auto">
      <div class="eventheader flex justify-between">
        <h2>Seneste Events</h2>
        <button @click="openModal">Nyt event</button>
      </div>
      <div class="eventbody pt-2">
        <div v-for="event in data.response" >
          <Event :event="event"/>
        </div>
      </div>
    </div>
  </div>

  <!-- Add Event Modal -->
  <div v-if="showModal" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white p-6 rounded shadow-lg w-96">
      <h2 class="text-xl mb-4">Add New Event</h2>
      <label class="block mb-2">Name</label>
      <input v-model="eventName" class="border p-2 w-full mb-4" placeholder="Event name" />
      <label class="block mb-2">Description</label>
      <input v-model="eventDescription" class="border p-2 w-full mb-4" placeholder="Description" />
      <div class="flex justify-end space-x-2">
        <button @click="closeModal" class="px-4 py-2 bg-gray-300 rounded">Close</button>
        <button @click="saveEvent" class="px-4 py-2 bg-blue-500 text-white rounded">Save</button>
      </div>
    </div>
  </div>
</template>