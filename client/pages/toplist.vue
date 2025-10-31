<script setup lang="ts">
import BeerCard from '~/components/beerCard.vue';
import List from '~/components/ui/List.vue';
import beerService from '~/services/BeerService/beerService';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const { data: event_beers, pending: beersPending } = await beerService.eventBeer.toplist();
</script>

<template>
  <h1 class="text-center">{{ t('toplist') }}</h1>
  <List
    :items="event_beers?.response || []"
    :pending="beersPending"
    loadingText="loading"
    emptyText="no.beers.rated"
    class="beerContainer"
  >
    <template #default="{ item }">
      <BeerCard :beer="item" :buttonsAvailable="false" />
    </template>
  </List>
</template>
