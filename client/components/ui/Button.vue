<script setup lang="ts">
  import { computed, toRefs } from 'vue';

  const props = defineProps({
    color: {
      type: String,
      default: 'default', // 'default', 'yellow', 'close', etc.
    },
    edit: {
      type: Boolean,
      default: false,
    },
    close: {
      type: Boolean,
      default: false,
    },
    type: {
      type: String,
      default: 'button',
    },
    class: {
      type: [String, Array, Object],
      default: '',
    },
  });

  const { color, close, type, class: extraClass } = toRefs(props);

  const btnCss = 'px-3 py-2 rounded transition focus:outline-none hover:opacity-65';

  const buttonClasses = computed(() => {
    let base;
    if (close.value) {
      base = `${btnCss}`;
    } else if (color.value === 'yellow') {
      base = `${btnCss} bg-yellow-400 text-black `;
    } else {
      base = `${btnCss} bg-zinc-800 text-white`;
    }

    return [base, extraClass.value].filter(Boolean).join(' ');
  });

</script>

<template>
  <button
    :class="buttonClasses"
    :type="type"
  >
    <template v-if="close">
      <img src="/img/close.svg" alt="Close" class="w-7 h-7 inline-block align-middle" />
    </template>
    <template v-if="edit">
      <slot />
      <img src="/img/edit-white.svg" alt="Edit" class="w-5 h-5 inline-block align-middle ml-1 pb-1" />
    </template>
    <template v-else>
      <slot />
    </template>
  </button>
</template>

<style>
  button {
    font-family: "Oswald", sans-serif;
    font-optical-sizing: auto;
    font-weight: normal;
    font-style: normal;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  button.yellow {
    background-color: #FECB23;
    color: #000;
  }
</style>