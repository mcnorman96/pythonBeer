<script setup lang="ts">
import baseModal from '~/layouts/BaseModal.vue';
import { ref, onMounted, watch } from 'vue';
import beerService from '~/services/BeerService/beerService';
import type { Beer, Rating } from '~/types/types';
import BaseButton from '~/components/ui/BaseButton.vue';
import BaseInput from '~/components/ui/BaseInput.vue';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const props = defineProps<{ beer: Beer }>();
const emit = defineEmits<{ (e: 'close'): void }>();
const route = useRoute();
const eventId = route.params.id;

const getRating = ref<Rating | null>(null);
const taste = ref<number | undefined>(undefined);
const aftertaste = ref<number | undefined>(undefined);
const smell = ref<number | undefined>(undefined);
const design = ref<number | undefined>(undefined);
const total_score = ref<number | undefined>(undefined);
const errorMsg = ref<string | null>(null);

const errors = ref<{ [key: string]: string }>({
  taste: '',
  aftertaste: '',
  smell: '',
  design: '',
  total_score: '',
});

onMounted(async () => {
  const rating: Response<Rating> = await beerService.ratings.getRating(
    eventId as string,
    props.beer.id
  );
  getRating.value = rating.response;
});

watch(
  getRating,
  (beerRated: Response<Rating>) => {
    if (beerRated && beerRated.response) {
      taste.value = beerRated.response.taste;
      aftertaste.value = beerRated.response.aftertaste;
      smell.value = beerRated.response.smell;
      design.value = beerRated.response.design;
      total_score.value = beerRated.response.score;
    }
  },
  { immediate: true }
);

const validate = () => {
  errors.value.taste =
    taste.value === undefined || taste.value < 0 || taste.value > 5 ? t('value.between.0.5') : '';
  errors.value.aftertaste =
    aftertaste.value === undefined || aftertaste.value < 0 || aftertaste.value > 5
      ? t('value.between.0.5')
      : '';
  errors.value.smell =
    smell.value === undefined || smell.value < 0 || smell.value > 5 ? t('value.between.0.5') : '';
  errors.value.design =
    design.value === undefined || design.value < 0 || design.value > 5
      ? t('value.between.0.5')
      : '';
  errors.value.total_score =
    total_score.value === undefined || total_score.value < 0 || total_score.value > 5
      ? t('value.between.0.5')
      : '';
  return Object.values(errors.value).every((e) => !e);
};

const handleSave = async () => {
  if (!validate()) {
    errorMsg.value = t('validation.error');
    return;
  }

  const saveRating = await beerService.ratings.addRating({
    event_id: eventId,
    beer_id: props.beer.id,
    taste: taste.value!,
    aftertaste: aftertaste.value!,
    smell: smell.value!,
    design: design.value!,
    score: total_score.value!,
  });

  if (saveRating.errorMsg) {
    errorMsg.value = saveRating.errorMsg;
    return;
  } else {
    errorMsg.value = null;
    emit('close');
  }
};

const handleClose = () => {
  emit('close');
};
</script>

<template>
  <baseModal :handleClose="handleClose">
    <h2 class="text-xl mb-4">{{ t('rate') }} {{ props.beer.name }}</h2>
    <div class="mb-4">
      <BaseInput v-model="taste" name="taste" title="taste" type="number" />
      <div v-if="errors.taste" class="text-red-500 text-xs mb-2">{{ errors.taste }}</div>

      <BaseInput v-model="aftertaste" name="aftertaste" title="aftertaste" type="number" />
      <div v-if="errors.aftertaste" class="text-red-500 text-xs mb-2">{{ errors.aftertaste }}</div>

      <BaseInput v-model="smell" name="smell" title="smell" type="number" />
      <div v-if="errors.smell" class="text-red-500 text-xs mb-2">{{ errors.smell }}</div>

      <BaseInput v-model="design" name="design" title="design" type="number" />
      <div v-if="errors.design" class="text-red-500 text-xs mb-2">{{ errors.design }}</div>

      <BaseInput v-model="total_score" name="score" title="score" type="number" />
      <div v-if="errors.total_score" class="text-red-500 text-xs mb-2">
        {{ errors.total_score }}
      </div>
    </div>
    <div class="flex justify-end space-x-2">
      <BaseButton name="saveRating" color="yellow" @click="handleSave" class="w-full savebtn">
        {{ t('save') }}
      </BaseButton>
    </div>
    <div v-if="errorMsg" class="mt-4 text-red-500">
      {{ errorMsg }}
    </div>
  </baseModal>
</template>
