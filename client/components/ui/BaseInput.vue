<script setup lang="ts">
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

defineProps({
  title: String,
  modelValue: [String, Number],
  name: String,
  type: {
    type: String,
    default: 'text',
  },
  min: {
    type: Number,
    default: 0,
  },
  max: {
    type: Number,
    default: 5,
  },
  step: {
    type: Number,
    default: 0.1,
  },
});

const emit = defineEmits(['update:modelValue']);
</script>

<template>
  <label class="block mb-4 capitalize">
    {{ t(title) }}
    <input
      v-if="type === 'number'"
      class="border p-2 w-full mt-2"
      :placeholder="t(title)"
      :name="name"
      :type="type"
      :value="modelValue"
      :min="min"
      :max="max"
      :step="step"
      @input="emit('update:modelValue', $event.target.value)"
    />
    <input
      v-else
      class="border p-2 w-full mt-2"
      :placeholder="t(title)"
      :name="name"
      :type="type"
      :value="modelValue"
      @input="emit('update:modelValue', $event.target.value)"
    />
  </label>
</template>
