<script setup lang="ts">
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

defineProps({
  error: {
    type: String,
  },
  success: {
    type: String,
  },
});
</script>

<template>
  <div v-if="error" class="text-red-500 mb-4">{{ t(error) }}</div>
  <div v-else-if="success" class="text-green-500 mb-4">{{ t(success) }}</div>
</template>
