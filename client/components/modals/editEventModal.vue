<script setup lang="ts">
import Button from '~/components/ui/Button.vue';
import beerService from '~/services/BeerService/beerService';
import { useRoute, useRouter } from 'vue-router';
import { ref } from 'vue';

const route = useRoute();
const eventId: string = route.params.id;
const emit = defineEmits<{ (e: 'close'): void; (e: 'save'): void }>();
const router = useRouter();

const eventName = ref<string>('');
const eventDescription = ref<string>('');
const error = ref<string>('');

const handleClose = () => {
  emit('close');
  eventName.value = '';
  eventDescription.value = '';
};

const updateEvent = async () => {
  const updateEvent = await beerService.events.updateEvent(eventId, {
    name: eventName.value,
    description: eventDescription.value,
  });

  if (!updateEvent.success) {
    error.value = updateEvent.error;
    return;
  }

  handleClose();
};

const deleteEvent = async () => {
  const deleteEvent = await beerService.events.deleteEvent(eventId);

  if (deleteEvent.success) {
    handleClose();
    router.push('/events');
  } else {
    error.value = deleteEvent.error || 'Failed to delete event';
  }
};
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white p-6 rounded shadow-lg w-96 relative m-2 max-h-[80vh] overflow-y-auto">
      <Button close @click="handleClose" :class="'rounded absolute top-2 right-2'"></Button>
      <h2 class="text-xl mb-4">Edit Event</h2>

      <div>
        <h3 class="font-semibold mb-2">Change Event Details</h3>
        <label class="block mb-2">Name</label>
        <input
          name="name"
          v-model="eventName"
          class="border p-2 w-full mb-2"
          placeholder="Event name"
        />
        <label class="block mb-2">Description</label>
        <input
          name="description"
          v-model="eventDescription"
          class="border p-2 w-full mb-2"
          placeholder="Description"
        />
        <Button
          name="updateEvent"
          @click="updateEvent"
          color="yellow"
          :class="'px-4 py-2 rounded w-full mb-2'"
          >Update Event</Button
        >
      </div>

      <Button name="deleteEvent" error @click="deleteEvent" :class="'w-full'">Delete Event</Button>
      <div v-if="error" class="text-red-500 mt-2">{{ error }}</div>
    </div>
  </div>
</template>
