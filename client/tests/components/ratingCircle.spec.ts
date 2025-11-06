import { mount } from '@vue/test-utils';
import RatingCircle from '@/components/ui/RatingCircle.vue';
import { createI18n } from 'vue-i18n';
import en from '@/i18n/locales/en.json';
const i18n = createI18n({
  locale: 'en',
  messages: { en },
});

describe('RatingCircle.vue', () => {
  it('renders the name prop', () => {
    const wrapper = mount(RatingCircle, {
      props: { name: 'Test Beer', rating: 4 },
      global: {
        plugins: [i18n],
      },
    });
    expect(wrapper.text()).toContain('Test Beer');
  });

  it('renders the rating prop as text', () => {
    const wrapper = mount(RatingCircle, {
      props: { name: 'Test Beer', rating: 4 },
      global: {
        plugins: [i18n],
      },
    });
    const percentageText = wrapper.find('text.percentage');
    expect(percentageText.exists()).toBe(true);
    expect(percentageText.text()).toBe('4');
  });

  it('sets the correct stroke-dasharray for the rating', () => {
    const wrapper = mount(RatingCircle, {
      props: { name: 'Test Beer', rating: 3 },
      global: {
        plugins: [i18n],
      },
    });
    const circle = wrapper.find('path.circle');
    expect(circle.exists()).toBe(true);
    expect(circle.attributes('stroke-dasharray')).toBe('60, 100'); // 3 * 20 = 60
  });

  it('renders SVG and classes correctly', () => {
    const wrapper = mount(RatingCircle, {
      props: { name: 'Test Beer', rating: 5 },
      global: {
        plugins: [i18n],
      },
    });
    expect(wrapper.find('svg').exists()).toBe(true);
    expect(wrapper.find('path.circle-bg').exists()).toBe(true);
    expect(wrapper.find('path.circle').exists()).toBe(true);
    expect(wrapper.find('text.percentage').exists()).toBe(true);
  });

  it('handles rating 0 correctly', () => {
    const wrapper = mount(RatingCircle, {
      props: { name: 'Zero Beer', rating: 0 },
      global: {
        plugins: [i18n],
      },
    });
    const circle = wrapper.find('path.circle');
    expect(circle.attributes('stroke-dasharray')).toBe('0, 100');
    expect(wrapper.find('text.percentage').text()).toBe('0');
  });
});
