import { mount, flushPromises } from '@vue/test-utils';
import viewRatingsModal from '~/components/modals/viewRatingsModal.vue';
import beerService from '@/services/BeerService/beerService';

// Mock Nuxt auto-import composables globally
globalThis.useRoute = () => ({ params: { id: '1' } });
globalThis.useFetch = async () => ({ data: { value: [] }, error: null, pending: false });
globalThis.onMounted = (fn: () => void) => fn();

describe('viewRatingsModal.vue', () => {
  const beer = { id: 1, name: 'Test Beer', brewery: 'Test Brewery', description: '', type: '' };

  // Helps initialize the modal
  const wrapperHelper = async () => {
    return await mount({
      template: '<Suspense><ViewRatingsModal :beer="beer" /></Suspense>',
      components: { ViewRatingsModal: viewRatingsModal },
      setup() {
        return { beer };
      }
    }, {
      global: {
        components: {
          RatingCircle: {
            template: '<div><slot></slot> {{ name }}</div>',
            props: ['name']
          }
        }
      }
    });
  };

  beforeEach(() => {
    // Reset all mocks before each test
    vi.resetAllMocks();
  });

  it('renders the modal', async () => {
    vi.spyOn(beerService.ratings, 'getAllRatingsForBeer').mockResolvedValue({
      data: { response: [] },
      error: null,
      pending: false
    });
    const wrapper = await wrapperHelper();
    await flushPromises();

    expect(wrapper.html()).toContain('No ratings available.');
    expect(wrapper.html()).toContain('Ratings for Test Beer');
  });

  it('shows loading state', async () => {
    vi.spyOn(beerService.ratings, 'getAllRatingsForBeer').mockResolvedValue({
      data: null,
      error: null,
      pending: true
    });

    const wrapper = await wrapperHelper();

    await flushPromises();

    expect(wrapper.text()).toContain('Loading ratings...');
  });

  it('shows error state', async () => {
    vi.spyOn(beerService.ratings, 'getAllRatingsForBeer').mockResolvedValue({
      data: null,
      error: { message: 'Failed to load' },
      pending: false
    });

    const wrapper = await wrapperHelper();

    await flushPromises();

    expect(wrapper.text()).toContain('Error loading ratings: Failed to load');
  });

  it('shows no ratings available', async () => {
    vi.spyOn(beerService.ratings, 'getAllRatingsForBeer').mockResolvedValue({
      data: { response: [] },
      error: null,
      pending: false
    });

    const wrapper = await wrapperHelper();

    await flushPromises();

    expect(wrapper.text()).toContain('No ratings available.');
  });

  it('shows ratings when available', async () => {
    vi.spyOn(beerService.ratings, 'getAllRatingsForBeer').mockResolvedValue({
      data: {
        response: [
          {
            id: 1,
            username: 'Alice',
            taste: 4,
            aftertaste: 3.5,
            smell: 4.5,
            design: 5,
            score: 4.7
          }
        ]
      },
      error: null,
      pending: false
    });

    const wrapper = await wrapperHelper();

    await flushPromises();

    expect(wrapper.text()).toContain('Alice');
    expect(wrapper.text()).toContain('Taste');
    expect(wrapper.text()).toContain('Score');
  });

  it('emits close event when close button is clicked', async () => {
    vi.spyOn(beerService.ratings, 'getAllRatingsForBeer').mockResolvedValue({
      data: { response: [] },
      error: null,
      pending: false
    });

    const wrapper = await wrapperHelper();

    await flushPromises();

    const modal = wrapper.findComponent(viewRatingsModal);
    const closeBtn = modal.find('button.closebtn');
    await closeBtn.trigger('click');
    expect(modal.emitted('close')).toBeTruthy();
  });
});
