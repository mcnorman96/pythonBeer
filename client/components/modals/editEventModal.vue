<script setup lang="ts">
import baseModal from '~/layouts/BaseModal.vue';
import BaseButton from '~/components/ui/BaseButton.vue';
import TextInput from '~/components/ui/TextInput.vue';
import beerService from '~/services/BeerService/beerService';
import { useRoute, useRouter } from 'vue-router';
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

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
  <baseModal :handleClose="handleClose">
    <h2 class="text-xl mb-4">{{ t('edit.event') }}</h2>
    <TextInput v-model="eventName" name="name" title="name" />
    <TextInput v-model="eventDescription" name="description" title="description" />
    <BaseButton
      name="updateEvent"
      @click="updateEvent"
      color="yellow"
      :class="'px-4 py-2 rounded w-full mb-2'"
      >{{ t('update.event') }}</BaseButton
    >
    <BaseButton name="deleteEvent" error @click="deleteEvent" :class="'w-full'">{{
      t('delete.event')
    }}</BaseButton>
    <div v-if="error" class="text-red-500 mt-2">{{ error }}</div>
  </baseModal>
</template>
