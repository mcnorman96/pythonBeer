<script setup lang="ts">
import baseModal from '~/layouts/BaseModal.vue';
import beerService from '~/services/BeerService/beerService';
import type { Beer, Rating } from '~/types/types';
import List from '~/components/ui/List.vue';
import { useRoute } from 'vue-router';
import RatingCircle from '~/components/ui/RatingCircle.vue';
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const props = defineProps<{ beer: Beer }>();
const emit = defineEmits<{ (e: 'close'): void }>();
const route = useRoute();
const eventId = route.params.id;

const beer_ratings = ref<Rating[]>([]);
const ratings_pending = ref<Rating>(false);

onMounted(async () => {
  ratings_pending.value = true;

  const { data: ratings } = await beerService.ratings.getAllRatingsForBeer(
    eventId as string,
    props.beer.id
  );

  if (ratings?.value?.response) {
    beer_ratings.value = ratings.value.response;
  } else {
    console.error('No ratings fetched');
  }

  ratings_pending.value = false;
});

const handleClose = () => {
  emit('close');
};
</script>

<template>
  <baseModal :handleClose="handleClose">
    <h2 class="text-xl mb-4">{{ t('ratings.for') }} {{ props.beer.name }}</h2>
    <List
      :items="beer_ratings || []"
      :pending="ratings_pending"
      loadingText="loading"
      emptyText="no.ratings"
      class="mb-5"
    >
      <template #default="{ item }">
        <div v-if="item" class="flex justify-between py-5 border-t border-t-black">
          <div class="name mr-3 capitalize">
            {{ item.username }}
          </div>
          <div class="rightside">
            <div class="flex -mr-3 md:-mr-6">
              <RatingCircle :rating="item.taste" name="taste" />
              <RatingCircle :rating="item.aftertaste" name="aftertaste" />
              <RatingCircle :rating="item.smell" name="smell" />
              <RatingCircle :rating="item.design" name="design" />
              <RatingCircle :rating="item.score" name="score" />
            </div>
          </div>
        </div>
      </template>
    </List>
  </baseModal>
</template>
