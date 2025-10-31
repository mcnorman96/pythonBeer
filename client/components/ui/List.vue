<script setup lang="ts">
import { useI18n } from 'vue-i18n';
const { t } = useI18n();
import type { Event, Beer } from '~/types/types';

defineProps<{
  items: Array<Event | Beer>;
  pending?: boolean;
  loadingText?: string;
  emptyText?: string;
}>();

const itemKey = (item: Event | Beer) => {
  // Default key: item.id or item.name or index
  return item.id ?? item.name ?? JSON.stringify(item);
};
</script>

<template>
  <div class="max-w-3xl m-auto">
    <slot name="sorting" />
    <div v-if="pending">{{ t(loadingText) }}</div>
    <div v-else-if="!items || items.length < 1">{{ t(emptyText) }}</div>
    <div v-else>
      <div v-for="item in items" :key="itemKey(item)">
        <slot :item="item" />
      </div>
    </div>
    <slot name="extra" />
  </div>
</template>
