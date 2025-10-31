<script setup lang="ts">
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

defineProps({
  title: {
    type: String,
    default: 'default',
  },
  modelValue: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['update:modelValue']);
</script>

<template>
  <div class="mb-4">
    <label class="block mb-2 capitalize"
      >{{ t(title) }}
      <input
        :value="modelValue"
        @input="emit('update:modelValue', $event.target.value)"
        :name="title"
        :type="type"
        class="border p-2 w-full mt-2"
        :placeholder="t(title)"
      />
    </label>
  </div>
</template>
