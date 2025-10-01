import { mount, flushPromises } from '@vue/test-utils';
import viewRatingsModal from '~/components/modals/viewRatingsModal.vue';
import beerService from '@/services/BeerService/beerService';

// Mock Nuxt auto-import composables globally
globalThis.useRoute = () => ({ params: { id: '1' } });
globalThis.useFetch = async () => ({ data: { value: [] }, error: null, pending: false });
globalThis.onMounted = (fn: () => void) => fn();

describe('viewRatingsModal.vue', () => {
	const beer = { id: 1, name: 'Test Beer', brewery: 'Test Brewery', description: '', type: '' };

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
		const wrapper = await mount(viewRatingsModal, {
			props: { beer }
		});
		expect(wrapper.exists()).toBe(true);
		expect(wrapper.text()).toContain('No ratings available');
	});

	// it('shows loading state', async () => {
	// 	vi.spyOn(beerService.ratings, 'getAllRatingsForBeer').mockResolvedValue({
	// 		data: null,
	// 		error: null,
	// 		pending: true
	// 	});
	// 	const wrapper = await mount(viewRatingsModal, {
	// 		props: { beer }
	// 	});
	// 	expect(wrapper.text()).toContain('Loading ratings...');
	// });

	// it('shows error state', async () => {
	// 	vi.spyOn(beerService.ratings, 'getAllRatingsForBeer').mockResolvedValue({
	// 		data: null,
	// 		error: { message: 'Failed to load' },
	// 		pending: false
	// 	});
	// 	const wrapper = await mount(viewRatingsModal, {
	// 		props: { beer }
	// 	});
	// 	expect(wrapper.text()).toContain('Error loading ratings: Failed to load');
	// });

	// it('shows no ratings available', async () => {
	// 	vi.spyOn(beerService.ratings, 'getAllRatingsForBeer').mockResolvedValue({
	// 		data: { response: [] },
	// 		error: null,
	// 		pending: false
	// 	});
	// 	const wrapper = await mount(viewRatingsModal, {
	// 		props: { beer }
	// 	});
	// 	expect(wrapper.text()).toContain('No ratings available.');
	// });

	// it('shows ratings when available', async () => {
	// 	vi.spyOn(beerService.ratings, 'getAllRatingsForBeer').mockResolvedValue({
	// 		data: {
	// 			response: [
	// 				{
	// 					id: 1,
	// 					username: 'Alice',
	// 					taste: 4,
	// 					aftertaste: 3.5,
	// 					smell: 4.5,
	// 					design: 5,
	// 					score: 4.7
	// 				}
	// 			]
	// 		},
	// 		error: null,
	// 		pending: false
	// 	});
	// 	const wrapper = await mount(viewRatingsModal, {
	// 		props: { beer }
	// 	});
	// 	expect(wrapper.text()).toContain('Alice');
	// 	expect(wrapper.text()).toContain('Taste');
	// 	expect(wrapper.text()).toContain('Score');
	// });

	// it('emits close event when close button is clicked', async () => {
	// 	vi.spyOn(beerService.ratings, 'getAllRatingsForBeer').mockResolvedValue({
	// 		data: { response: [] },
	// 		error: null,
	// 		pending: false
	// 	});
	// 	const wrapper = await mount(viewRatingsModal, {
	// 		props: { beer }
	// 	});
	// 	const closeBtn = wrapper.find('button');
	// 	await closeBtn.trigger('click');
	// 	expect(wrapper.emitted('close')).toBeTruthy();
	// });
});
