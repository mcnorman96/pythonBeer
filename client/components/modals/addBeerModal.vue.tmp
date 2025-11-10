<script setup lang="ts">
import { ref, watch } from 'vue';
import type { Beer } from '~/types/types';
import beerService from '~/services/BeerService/beerService';
import BaseButton from '~/components/ui/BaseButton.vue';
import baseModal from '~/layouts/BaseModal.vue';
import BaseInput from '~/components/ui/BaseInput.vue';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
const { t } = useI18n();

const route = useRoute();
const eventId: string | string[] = route.params.id;
const emit = defineEmits<{ (e: 'close'): void; (e: 'save'): void }>();

const beerName = ref<string>('');
const beerDescription = ref<string>('');
const beerBrewery = ref<string>('');
const beerType = ref<string>('');

const filteredBeers = ref<Beer[]>([]);
const selectedBeerId = ref<Beer | null>(null);
const beerSearch = ref<string>('');
const showDropdown = ref<boolean>(false);
const error = ref<string | null>(null);

watch(beerSearch, async (val: string) => {
  if (val.length < 3) {
    filteredBeers.value = [];
    showDropdown.value = false;
    return;
  }
  const { data: searchedBeers }: Beer[] = await beerService.eventBeer.searchBeer(val);

  filteredBeers.value = searchedBeers.value?.response || [];
  showDropdown.value = filteredBeers.value.length > 0;
});

const handleClose = () => {
  emit('close');
  beerName.value = '';
  beerDescription.value = '';
  beerBrewery.value = '';
  beerType.value = '';
  selectedBeerId.value = null;
  beerSearch.value = '';
  showDropdown.value = false;
  filteredBeers.value = [];
};

const saveBeer = async () => {
  try {
    if (!beerName.value || !beerDescription.value || !beerBrewery.value || !beerType.value) {
      error.value = t('all.fields.required.create.beer');
      console.error('All fields are required to create a new beer.');
      return;
    }

    const createBeer: Response = await beerService.eventBeer.newBeer({
      name: beerName.value,
      description: beerDescription.value,
      brewery: beerBrewery.value,
      type: beerType.value,
    });

    if (!createBeer.success || !createBeer.response) {
      error.value = t('error.create.beer');
      console.error('Failed to create beer:', createBeer.error);
      return;
    }

    const beerIdString: string = createBeer.response.id.toString();
    const addBeerToEvent: Response = await beerService.eventBeer.addBeerToEvent(
      eventId as string,
      beerIdString
    );

    if (!addBeerToEvent.success) {
      error.value = t('error.adding.beer.to.event');
      console.error(addBeerToEvent.error);
    }
  } catch (error) {
    error.value = t('error.create.beer');
    console.error('Error creating or adding beer:', error);
  }

  handleClose();
};

const addExistingBeerToEvent = async (beerId: number) => {
  const beerIdString = beerId.toString();
  const addBeerToEvent = await beerService.eventBeer.addBeerToEvent(
    eventId as string,
    beerIdString
  );

  if (!addBeerToEvent.success) {
    error.value = addBeerToEvent.error;
    return;
  }
  handleClose();
};

const handleBlur = () => {
  setTimeout(() => {
    showDropdown.value = false;
  }, 200);
};
</script>

<template>
  <baseModal :handleClose="handleClose">
    <h2 class="text-xl mb-4">{{ t('add.beer.to.event') }}</h2>
    <div class="mb-6 relative">
      <h3 class="font-semibold mb-2">{{ t('add.existing.beer') }}</h3>
      <input
        name="beerSearch"
        v-model="beerSearch"
        class="border p-2 w-full mb-2"
        :placeholder="t('search.beer')"
        @focus="showDropdown = filteredBeers.length > 0"
        @blur="handleBlur"
      />
      <ul
        v-if="showDropdown"
        class="absolute left-0 right-0 bg-white border rounded shadow z-10 max-h-48 overflow-auto"
      >
        <li
          v-for="beer in filteredBeers"
          :key="beer.id"
          @mousedown.prevent="addExistingBeerToEvent(beer.id)"
          class="px-4 py-2 cursor-pointer hover:bg-gray-100"
        >
          {{ beer.name }}
        </li>
      </ul>
    </div>

    <div>
      <h3 class="font-semibold mb-2">{{ t('add.new.beer') }}</h3>
      <BaseInput v-model="beerName" name="name" title="name" />
      <BaseInput v-model="beerDescription" name="description" title="description" />
      <BaseInput v-model="beerBrewery" name="brewery" title="brewery" />
      <BaseInput v-model="beerType" name="type" title="type" />
      <BaseButton
        name="saveBeer"
        @click="saveBeer"
        color="yellow"
        :class="'px-4 py-2 rounded w-full mb-2'"
        >{{ t('save.new.beer') }}</BaseButton
      >
    </div>
    <div v-if="error" class="text-red-500 mt-2">{{ error }}</div>
  </baseModal>
</template>
