import { mount } from '@vue/test-utils';
import BeerCard from '~/components/beerCard.vue';

// Custom stub for RatingCircle to show the name prop
const ratingCircleStub = {
  template: '<div>{{ name }}</div>',
  props: ['name']
};

describe('BeerCard.vue', () => {
  const beer = {
    id: 1,
    name: 'Test Beer',
    brewery: 'Test Brewery',
    type: 'Lager',
    description: 'A crisp lager',
    average_taste: 4.2,
    average_aftertaste: 3.8,
    average_smell: 4.0,
    average_design: 4.5,
    average_score: 4.1
  };

  it('renders beer details', () => {
    const wrapper = mount(BeerCard, {
      props: { beer, buttonsAvailable: true },
      global: {
        stubs: { RatingCircle: ratingCircleStub }
      }
    });
    expect(wrapper.text()).toContain('Test Beer');
    expect(wrapper.text()).toContain('Test Brewery');
    expect(wrapper.text()).toContain('Lager');
    expect(wrapper.text()).toContain('A crisp lager');
  });

  it('renders rating circles with correct labels', () => {
    const wrapper = mount(BeerCard, {
      props: { beer, buttonsAvailable: true },
      global: {
        stubs: { RatingCircle: ratingCircleStub }
      }
    });
    expect(wrapper.text()).toContain('Taste');
    expect(wrapper.text()).toContain('Aftertaste');
    expect(wrapper.text()).toContain('Smell');
    expect(wrapper.text()).toContain('Design');
    expect(wrapper.text()).toContain('Score');
  });

  it('emits view-ratings event when view ratings button is clicked', async () => {
    const wrapper = mount(BeerCard, {
      props: { beer, buttonsAvailable: true },
      global: {
        stubs: { RatingCircle: ratingCircleStub }
      }
    });
    const viewBtn = wrapper.find('button.view-ratings');
    await viewBtn.trigger('click');
    expect(wrapper.emitted('view-ratings')).toBeTruthy();
    expect(wrapper.emitted('view-ratings')[0][0]).toEqual(beer);
  });

  it('emits add-rating event when add rating button is clicked', async () => {
    const wrapper = mount(BeerCard, {
      props: { beer, buttonsAvailable: true },
      global: {
        stubs: { RatingCircle: ratingCircleStub }
      }
    });
    const addBtn = wrapper.find('button.add-rating');
    await addBtn.trigger('click');
    expect(wrapper.emitted('add-rating')).toBeTruthy();
    expect(wrapper.emitted('add-rating')[0][0]).toEqual(beer);
  });

  it('does not render buttons if buttonsAvailable is false', () => {
    const wrapper = mount(BeerCard, {
      props: { beer, buttonsAvailable: false },
      global: {
        stubs: { RatingCircle: ratingCircleStub }
      }
    });
    expect(wrapper.findAll('button').length).toBe(0);
  });
});
