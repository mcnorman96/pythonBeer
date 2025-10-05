<script setup lang="ts">
const props = defineProps<{
  rating: number;
  name: string;
}>();
</script>

<template>
  <div class="text-center w-12 md:w-20">
    <div class="name text-xs md:text-sm mb-2">
      {{ props.name }}
    </div>
    <div class="rating-circle m-auto relative w-7 h-7 md:w-10 md:h-10">
      <svg viewBox="0 0 36 36" class="w-full h-full">
        <path
          class="circle-bg"
          d="M18 2.0845
            a 15.9155 15.9155 0 0 1 0 31.831
            a 15.9155 15.9155 0 0 1 0 -31.831"
        />
        <path
          class="circle"
          :stroke-dasharray="`${props.rating * 20}, 100`"
          d="M18 2.0845
            a 15.9155 15.9155 0 0 1 0 31.831
            a 15.9155 15.9155 0 0 1 0 -31.831"
        />
        <text x="18" y="20.35" class="percentage">{{ props.rating }}</text>
      </svg>
    </div>
  </div>
</template>

<style scoped>
.circle-bg {
  fill: none;
  stroke: #eee;
  stroke-width: 3.8;
}

.circle {
  fill: none;
  stroke-width: 3.8;
  stroke-linecap: round;
  stroke: #fecb23;
  transition: stroke-dasharray 0.35s;
}

.percentage {
  fill: #000000;
  font-size: 0.8em;
  text-anchor: middle;
  dominant-baseline: middle;
}
</style>
