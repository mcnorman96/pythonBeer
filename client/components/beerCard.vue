<script setup lang="ts">
import { useI18n } from 'vue-i18n';
const { t } = useI18n();
import RatingCircle from '~/components/ui/RatingCircle.vue';
import { computed } from 'vue';
import type { Beer } from '~/types/types';
import Button from '~/components/ui/Button.vue';

const props = defineProps<{
  beer: Beer;
  buttonsAvailable: boolean | true;
}>();

const emit = defineEmits(['add-rating', 'view-ratings', 'edit-beer']);

const taste = computed(() => props.beer.average_taste || 0);
const aftertaste = computed(() => props.beer.average_aftertaste || 0);
const smell = computed(() => props.beer.average_smell || 0);
const bottle_design = computed(() => props.beer.average_design || 0);
const average_score = computed(() => props.beer.average_score || 0);
</script>

<template>
  <div
    class="flex flex-wrap justify-between mt-5 bg-white border-gray-400 border-solid shadow-md rounded-2xl p-6"
    style="border-width: 0.5px"
  >
    <div class="leftside">
      <div class="name text-large font-bold">
        {{ props.beer.name }}
      </div>
      <div class="brewery text-sm">
        {{ props.beer.brewery }}
      </div>
      <div class="type text-sm">
        {{ props.beer.type }}
      </div>
      <div class="description text-sm">
        {{ props.beer.description }}
      </div>
    </div>
    <div class="rightside w-full md:w-auto">
      <div class="flex justify-between mt-5 mr-auto ml-auto md:ml-0 md:mt-0 md:-mr-6">
        <RatingCircle :rating="taste" name="taste" />
        <RatingCircle :rating="aftertaste" name="aftertaste" />
        <RatingCircle :rating="smell" name="smell" />
        <RatingCircle :rating="bottle_design" name="design" />
        <RatingCircle :rating="average_score" name="score" />
      </div>
      <div v-if="props.buttonsAvailable" class="flex md:w-max ml-auto mt-5">
        <Button
          edit
          name="editBeer"
          @click="emit('edit-beer', props.beer)"
          class="edit-beer w-1/2 md:w-auto"
          >{{ t('edit.beer') }}</Button
        >
        <Button
          name="viewRatings"
          @click="emit('view-ratings', props.beer)"
          :class="'view-ratings ml-5 w-1/2 md:w-auto'"
          >{{ t('view.ratings') }}</Button
        >
        <Button
          name="addRating"
          @click="emit('add-rating', props.beer)"
          color="yellow"
          :class="'add-rating ml-5 w-1/2 md:w-auto'"
          >{{ t('add.rating') }}</Button
        >
      </div>
    </div>
  </div>
</template>
