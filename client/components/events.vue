<script setup lang="ts">
import type { EventInterface } from '~/types/types';
import Event from './event.vue';
import { ref } from 'vue';

const props = defineProps<{
  data: { response: Array<EventInterface> };
  error: any;
  pending: any;
}>();

const newEvent = () => {
  console.log('neew event')
}

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
        <button :on-click="newEvent">Nyt event</button>
      </div>
      <div class="eventbody pt-2">
        <div v-for="event in data.response" >
          <Event :event="event"/>
        </div>
      </div>
    </div>
  </div>
</template>