<script lang="ts" setup>
import BaseButton from '~/components/ui/BaseButton.vue';

defineProps<{
  handleClose: {
    type: void;
    default: null;
  };
}>();
</script>

<template>
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
    <div class="bg-white p-6 rounded shadow-lg w-96 relative m-2 max-h-[80vh] overflow-y-auto">
      <BaseButton close @click="handleClose" :class="'rounded absolute top-2 right-2'"></BaseButton>
      <slot />
    </div>
  </div>
</template>
