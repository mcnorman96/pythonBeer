import { mount } from '@vue/test-utils';
import addRatingModal from '~/components/modals/addRatingModal.vue';
import { flushPromises } from '@vue/test-utils';
import beerService from '@/services/BeerService/beerService';
import { vi } from 'vitest';

vi.mock('vue-router', () => ({
  useRoute: () => ({ params: { id: '1' } }),
}));

// Type declarations for Nuxt auto-import composables
globalThis.onMounted = (fn: () => void) => {};
globalThis.watch = (source: any, cb: (newValue: any, oldValue: any) => void) => {};

describe('addRatingModal.vue', () => {
  it('renders the modal', () => {
    // Mock service methods
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
    });
    expect(wrapper.exists()).toBe(true);
  });

  it('emits close event when close button is clicked', async () => {
    // Mock service methods
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
    });
    const closeBtn = wrapper.find('button'); // The close button is just <button>
    await closeBtn.trigger('click');
    expect(wrapper.emitted('close')).toBeTruthy();
  });

  it('has inputs for all rating fields', () => {
    // Mock service methods
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
    });
    expect(wrapper.find('input[placeholder="Taste"]').exists()).toBe(true);
    expect(wrapper.find('input[placeholder="Aftertaste"]').exists()).toBe(true);
    expect(wrapper.find('input[placeholder="Smell"]').exists()).toBe(true);
    expect(wrapper.find('input[placeholder="Design"]').exists()).toBe(true);
    expect(wrapper.find('input[placeholder="Total Score"]').exists()).toBe(true);
  });

  it('calls beerService and emits close on successful save', async () => {
    // Mock service methods
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
    });

    // Set input values
    await wrapper.find('input[placeholder="Taste"]').setValue(4.5);
    await wrapper.find('input[placeholder="Aftertaste"]').setValue(4.0);
    await wrapper.find('input[placeholder="Smell"]').setValue(3.5);
    await wrapper.find('input[placeholder="Design"]').setValue(5.0);
    await wrapper.find('input[placeholder="Total Score"]').setValue(4.8);

    // Trigger save
    await wrapper.find('button.savebtn').trigger('click');
    await flushPromises();

    // Assertions
    expect(addRatingMock).toHaveBeenCalledWith({
      event_id: '1',
      beer_id: 1,
      taste: 4.5,
      aftertaste: 4.0,
      smell: 3.5,
      design: 5.0,
      score: 4.8,
    });
    expect(wrapper.emitted('close')).toBeTruthy();
  });
});
