import { ref } from 'vue';
import type { Beer } from '~/types/types';

type ModalType = null | 'addBeer' | 'editEvent' | 'addRating' | 'viewRatings' | 'editBeer';

export function useModalManager() {
  const modalState = ref<{ type: ModalType; beer: Beer | null }>({
    type: null,
    beer: null,
  });

  function openModal(type: ModalType, beer: Beer | null = null) {
    modalState.value = { type, beer };
  }

  function closeModal() {
    modalState.value = { type: null, beer: null };
  }

  return {
    modalState,
    openModal,
    closeModal,
  };
}
