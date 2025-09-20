<script setup>
import { ref } from 'vue';

const props = defineProps({
  rating: {
    type: Number,
    required: true,
    validator: (value) => value >= 0 && value <= 100
  },
  name: {
    type: String,
    required: true
  }
});
</script>

<template>
  <div class="text-center w-20">
    <div class="name text-xs mb-1">
      {{ props.name }}
    </div>
    <div class="rating-circle m-auto">
      <svg viewBox="0 0 36 36">
        <path
          class="circle-bg"
          d="M18 2.0845
            a 15.9155 15.9155 0 0 1 0 31.831
            a 15.9155 15.9155 0 0 1 0 -31.831"
        />
        <path
          class="circle"
          :stroke-dasharray="`${props.rating * 10}, 100`"
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
.rating-circle {
  width: 30px;
  height: 30px;
  position: relative;
}

.rating-circle svg {
  width: 100%;
  height: 100%;
}

.circle-bg {
  fill: none;
  stroke: #eee;
  stroke-width: 3.8;
}

.circle {
  fill: none;
  stroke-width: 3.8;
  stroke-linecap: round;
  stroke: #FECB23;
  transition: stroke-dasharray 0.35s;
}

.percentage {
  fill: #000000;
  font-size: 0.8em;
  text-anchor: middle;
  dominant-baseline: middle;
}
</style>