<script setup lang="ts">
import baseModal from '~/layouts/BaseModal.vue';
import { ref, onMounted } from 'vue';
import type { Beer } from '~/types/types';
import beerService from '~/services/BeerService/beerService';
import BaseButton from '~/components/ui/BaseButton.vue';
import BaseInput from '~/components/ui/BaseInput.vue';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const props = defineProps<{ beer: Beer }>();
const route = useRoute();
const eventId: string = route.params.id;
const emit = defineEmits<{ (e: 'close'): void }>();

const beerName = ref<string>('');
const beerDescription = ref<string>('');
const beerBrewery = ref<string>('');
const beerType = ref<string>('');

const error = ref<string | null>(null);

const handleClose = () => {
  emit('close');
  beerName.value = '';
  beerDescription.value = '';
  beerBrewery.value = '';
  beerType.value = '';
};

onMounted(() => {
  if (props.beer) {
    beerName.value = props.beer.name;
    beerDescription.value = props.beer.description;
    beerBrewery.value = props.beer.brewery;
    beerType.value = props.beer.type;
  }
});

const updateBeer = async () => {
  const BeerObj: Beer = {
    id: props.beer.id,
    name: beerName.value,
    description: beerDescription.value,
    brewery: beerBrewery.value,
    type: beerType.value,
  };

  const updateBeer = await beerService.eventBeer.updateBeer(BeerObj);

  if (!updateBeer.success) {
    error.value = updateBeer.error;
    return;
  }
  handleClose();
};

const handleDeleteBeerFromEvent = () => {
  const deleteBeerFromEvent = beerService.eventBeer.deleteBeerFromEvent(props.beer.id, eventId);

  if (!deleteBeerFromEvent) {
    error.value = deleteBeerFromEvent.error;
    return;
  }

  handleClose();
};
</script>

<template>
  <baseModal :handleClose="handleClose">
    <h2 class="text-xl mb-4">{{ t('update.beer') }}</h2>

    <BaseInput v-model="beerName" name="name" title="name" />
    <BaseInput v-model="beerDescription" name="description" title="description" />
    <BaseInput v-model="beerBrewery" name="brewery" title="brewery" />
    <BaseInput v-model="beerType" name="type" title="type" />

    <BaseButton name="updateBeer" @click="updateBeer" color="yellow" :class="'w-full mb-2'">{{
      t('update.beer')
    }}</BaseButton>
    <BaseButton name="deleteBeer" delete @click="handleDeleteBeerFromEvent" class="w-full">{{
      t('remove.beer.from.event')
    }}</BaseButton>
    <div v-if="error" class="text-red-500 mt-2">{{ error }}</div>
  </baseModal>
</template>
