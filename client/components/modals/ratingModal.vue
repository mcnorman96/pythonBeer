<script setup lang="ts">
import { ref } from 'vue';
const props = defineProps<{ beer: any }>();
const emit = defineEmits(['close', 'save']);

const taste = ref(0);
const aftertaste = ref(0);
const smell = ref(0);
const design = ref(0);
const total_score = ref(0);

const handleSave = () => {
  emit('save', {
    beerId: props.beer.id,
    taste: taste.value,
    aftertaste: aftertaste.value,
    smell: smell.value,
    design: design.value,
    score: total_score.value
  });
};

const handleClose = () => {
  emit('close');
};
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white p-6 rounded shadow-lg w-96">
      <h2 class="text-xl mb-4">Rate {{ props.beer.name }}</h2>
      <div class="mb-4">
        <label class="block mb-2">Taste</label>
        <input v-model="taste" type="number" min="0" max="10" class="border p-2 w-full mb-2" placeholder="Taste" />
        <label class="block mb-2">Aftertaste</label>
        <input v-model="aftertaste" type="number" min="0" max="10" class="border p-2 w-full mb-2" placeholder="Aftertaste" />
        <label class="block mb-2">Smell</label>
        <input v-model="smell" type="number" min="0" max="10" class="border p-2 w-full mb-2" placeholder="Smell" />
        <label class="block mb-2">Bottle Design</label>
        <input v-model="design" type="number" min="0" max="10" class="border p-2 w-full mb-2" placeholder="Bottle Design" />
        <label class="block mb-2">Total score</label>
        <input v-model="total_score" type="number" min="0" max="40" class="border p-2 w-full mb-2" placeholder="Total Score" />
      </div>
      <div class="flex justify-end space-x-2">
        <button @click="handleClose" class="px-4 py-2 bg-gray-300 rounded">Close</button>
        <button @click="handleSave" class="px-4 py-2 bg-blue-500 text-white rounded">Save</button>
      </div>
    </div>
  </div>
</template>