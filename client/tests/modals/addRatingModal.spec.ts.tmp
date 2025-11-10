import { mount } from '@vue/test-utils';
import addRatingModal from '@/components/modals/AddRatingModal.vue';
import { flushPromises } from '@vue/test-utils';
import beerService from '@/services/BeerService/beerService';
import { vi } from 'vitest';
import { createI18n } from 'vue-i18n';
import en from '@/i18n/locales/en.json';
const i18n = createI18n({
  locale: 'en',
  messages: { en },
});

vi.mock('vue-router', () => ({
  useRoute: () => ({ params: { id: '1' } }),
}));

globalThis.onMounted = (fn: () => void) => {};
globalThis.watch = (source: any, cb: (newValue: any, oldValue: any) => void) => {};

describe('addRatingModal.vue', () => {
  it('renders the modal', () => {
    const mockGetRating = vi.fn().mockResolvedValue({
      success: true,
      response: {
        taste: 0,
        aftertaste: 0,
        smell: 0,
        design: 0,
        score: 0,
      },
    });

    beerService.ratings.getRating = mockGetRating;

    const wrapper = mount(addRatingModal, {
      props: {
        beer: { id: 1, name: 'Test Beer', brewery: 'Test Brewery', description: '', type: '' },
      },
      global: {
        plugins: [i18n],
      },
    });
    expect(wrapper.exists()).toBe(true);
  });

  it('emits close event when close button is clicked', async () => {
    const mockGetRating = vi.fn().mockResolvedValue({
      success: true,
      response: {
        taste: 0,
        aftertaste: 0,
        smell: 0,
        design: 0,
        score: 0,
      },
    });

    beerService.ratings.getRating = mockGetRating;

    const wrapper = mount(addRatingModal, {
      props: {
        beer: { id: 1, name: 'Test Beer', brewery: 'Test Brewery', description: '', type: '' },
      },
      global: {
        plugins: [i18n],
      },
    });
    const closeBtn = wrapper.find('button');
    await closeBtn.trigger('click');
    expect(wrapper.emitted('close')).toBeTruthy();
  });

  it('has inputs for all rating fields', () => {
    const mockGetRating = vi.fn().mockResolvedValue({
      success: true,
      response: {
        taste: 0,
        aftertaste: 0,
        smell: 0,
        design: 0,
        score: 0,
      },
    });

    beerService.ratings.getRating = mockGetRating;

    const wrapper = mount(addRatingModal, {
      props: {
        beer: { id: 1, name: 'Test Beer', brewery: 'Test Brewery', description: '', type: '' },
      },
      global: {
        plugins: [i18n],
      },
    });
    expect(wrapper.find('input[placeholder="Taste"]').exists()).toBe(true);
    expect(wrapper.find('input[placeholder="Aftertaste"]').exists()).toBe(true);
    expect(wrapper.find('input[placeholder="Smell"]').exists()).toBe(true);
    expect(wrapper.find('input[placeholder="Design"]').exists()).toBe(true);
    expect(wrapper.find('input[placeholder="Score"]').exists()).toBe(true);
  });

  it('calls beerService and emits close on successful save', async () => {
    const mockGetRating = vi.fn().mockResolvedValue({
      success: true,
      response: {
        taste: 0,
        aftertaste: 0,
        smell: 0,
        design: 0,
        score: 0,
      },
    });

    const addRatingMock = vi.fn().mockResolvedValue({
      success: true,
      response: {},
      error: null,
    });
    beerService.ratings.addRating = addRatingMock;
    beerService.ratings.getRating = mockGetRating;

    const wrapper = mount(addRatingModal, {
      props: {
        beer: { id: 1, name: 'Test Beer', brewery: 'Test Brewery', description: '', type: '' },
      },
      global: {
        plugins: [i18n],
      },
    });

    await wrapper.find('input[placeholder="Taste"]').setValue(4.5);
    await wrapper.find('input[placeholder="Aftertaste"]').setValue(4.1);
    await wrapper.find('input[placeholder="Smell"]').setValue(3.5);
    await wrapper.find('input[placeholder="Design"]').setValue(4.9);
    await wrapper.find('input[placeholder="Score"]').setValue(4.8);

    await wrapper.find('button.savebtn').trigger('click');
    await flushPromises();

    expect(addRatingMock).toHaveBeenCalledWith({
      event_id: '1',
      beer_id: 1,
      taste: '4.5',
      aftertaste: '4.1',
      smell: '3.5',
      design: '4.9',
      score: '4.8',
    });
    expect(wrapper.emitted('close')).toBeTruthy();
  });
});
