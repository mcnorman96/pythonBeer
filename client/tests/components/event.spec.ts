import { mount, flushPromises } from '@vue/test-utils';
import EventCard from '~/components/Event.vue';
import beerService from '@/services/BeerService/beerService';
import { ref, onMounted } from 'vue';
import { createI18n } from 'vue-i18n';
import en from '~/i18n/locales/en.json';
const i18n = createI18n({
  locale: 'en',
  messages: { en },
});
(globalThis as any).ref = ref;
(globalThis as any).onMounted = onMounted;

describe('Event.vue', () => {
  const event = {
    id: '1',
    name: 'Test Event',
    start_date: '2025-10-01T00:00:00.000Z',
    end_date: '2025-10-10T00:00:00.000Z',
    description: 'An awesome event',
  };

  const beers = [
    { id: 1, name: 'Beer One' },
    { id: 2, name: 'Beer Two' },
    { id: 3, name: 'Beer Three' },
  ];

  const wrapperHelper = async (customEvent = event) => {
    const wrapper = mount(EventCard, {
      props: { event: customEvent },
      global: {
        plugins: [i18n],
        stubs: {
          NuxtLink: {
            name: 'NuxtLink',
            props: ['to'],
            template: '<a :href="to"><slot></slot></a>',
          },
        },
      },
    });

    await flushPromises();

    return wrapper;
  };

  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('renders event details', async () => {
    vi.spyOn(beerService.eventBeer, 'toplistBeersInEvent').mockResolvedValue({
      success: true,
      response: beers,
    });

    const wrapper = await wrapperHelper();

    const link = wrapper.find('a');
    expect(link.text()).toContain('Test Event');
    expect(link.text()).toContain('An awesome event');
    expect(link.text()).toContain('Ended');

    const expectedDate = new Date(event.start_date).toLocaleDateString();
    expect(link.text()).toContain(expectedDate);
  });

  it('shows top 3 beers with trophy images', async () => {
    vi.spyOn(beerService.eventBeer, 'toplistBeersInEvent').mockResolvedValue({
      success: true,
      response: beers,
    });

    const wrapper = await wrapperHelper();

    beers.forEach((b) => {
      expect(wrapper.text()).toContain(b.name);
    });

    const trophyImgs = wrapper.findAll('img');
    expect(trophyImgs.length).toBe(3);
    expect(trophyImgs[0].attributes('src')).toContain('gold.svg');
    expect(trophyImgs[1].attributes('src')).toContain('silver.svg');
    expect(trophyImgs[2].attributes('src')).toContain('bronze.svg');
  });

  it('shows Ended status if event is over', async () => {
    const endedEvent = { ...event, end_date: '2020-01-01T00:00:00.000Z' };
    vi.spyOn(beerService.eventBeer, 'toplistBeersInEvent').mockResolvedValue({
      success: true,
      response: beers,
    });

    const wrapper = await wrapperHelper(endedEvent);
    expect(wrapper.text()).toContain('Ended');
  });

  it('links to the correct event page', async () => {
    vi.spyOn(beerService.eventBeer, 'toplistBeersInEvent').mockResolvedValue({
      success: true,
      response: beers,
    });

    const wrapper = await wrapperHelper();
    const link = wrapper.findComponent({ name: 'NuxtLink' });

    expect(link.exists()).toBe(true);

    expect(link.props('to')).toEqual('/events/1');
  });
});
