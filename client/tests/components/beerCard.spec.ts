import { mount } from '@vue/test-utils';
import BeerCard from '~/components/BeerCard.vue';
import { createI18n } from 'vue-i18n';
import en from '~/i18n/locales/en.json';
const i18n = createI18n({
  locale: 'en',
  messages: { en },
});

// Custom stub for RatingCircle to show the name prop
const ratingCircleStub = {
  template: '<div>{{ name }}</div>',
  props: ['name'],
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
    average_score: 4.1,
  };

  it('renders beer details', () => {
    const wrapper = mount(BeerCard, {
      props: { beer, buttonsAvailable: true },
      global: {
        plugins: [i18n],
        stubs: { RatingCircle: ratingCircleStub },
      },
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
        plugins: [i18n],
        stubs: { RatingCircle: ratingCircleStub },
      },
    });
    expect(wrapper.text()).toContain('taste');
    expect(wrapper.text()).toContain('aftertaste');
    expect(wrapper.text()).toContain('smell');
    expect(wrapper.text()).toContain('design');
    expect(wrapper.text()).toContain('score');
  });

  it('emits view-ratings event when view ratings button is clicked', async () => {
    const wrapper = mount(BeerCard, {
      props: { beer, buttonsAvailable: true },
      global: {
        plugins: [i18n],
        stubs: { RatingCircle: ratingCircleStub },
      },
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
        plugins: [i18n],
        stubs: { RatingCircle: ratingCircleStub },
      },
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
        plugins: [i18n],
        stubs: { RatingCircle: ratingCircleStub },
      },
    });
    expect(wrapper.findAll('button').length).toBe(0);
  });
});
