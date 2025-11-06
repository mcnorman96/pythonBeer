<script setup lang="ts">
import beerService from '~/services/BeerService/beerService';
import { ref, onMounted, onUnmounted } from 'vue';
import Event from '~/components/Event.vue';
import BaseButton from '~/components/ui/BaseButton.vue';
import { socket } from '~/services/vars.ts';
import List from '~/components/ui/List.vue';
import BaseInput from '~/components/ui/BaseInput.vue';
import StatusMessage from '~/components/ui/StatusMessage.vue';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

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
  <h1 class="text-center">{{ t('events') }}</h1>
  <BaseButton color="yellow" name="newEvent" class="text-center m-auto block" @click="openModal">
    {{ t('new.event') }}
  </BaseButton>

  <List
    :items="events || []"
    :pending="pending"
    loadingText="loading"
    emptyText="no.events.to.show"
    class="eventbody pt-5"
  >
    <template #default="{ item }">
      <Event :event="item" />
    </template>
  </List>

  <div
    v-if="showModal"
    class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50"
  >
    <form @submit.prevent="saveEvent" class="bg-white p-6 rounded shadow-lg w-96 relative">
      <BaseButton close @click="closeModal" class="absolute top-2 right-2"></BaseButton>
      <h2 class="text-xl mb-4">{{ t('add.new.event') }}</h2>
      <BaseInput v-model="eventName" name="eventName" title="event.name" />
      <BaseInput v-model="eventDescription" name="eventDescription" title="event.description" />
      <div class="flex justify-end space-x-2">
        <BaseButton type="submit" name="saveEvent" color="yellow" class="w-full">
          {{ t('save.event') }}
        </BaseButton>
      </div>
      <StatusMessage :error="errorMsg" />
    </form>
  </div>
</template>
