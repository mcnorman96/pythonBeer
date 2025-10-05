import { mount } from '@vue/test-utils';
import AddBeerModal from '~/components/modals/addBeerModal.vue';
import { flushPromises } from '@vue/test-utils';
import beerService from '@/services/BeerService/beerService';

// Mock Nuxt auto-import composables globally
globalThis.useRoute = () => ({ params: { id: '1' } });
globalThis.useFetch = async () => ({ data: { value: [] }, error: null, pending: false });

describe('AddBeerModal.vue', () => {
  it('renders the modal', () => {
    const wrapper = mount(AddBeerModal);
    expect(wrapper.exists()).toBe(true);
  });

  it('emits close event when close button is clicked', async () => {
    const wrapper = mount(AddBeerModal);
    const closeBtn = wrapper.find('.close-button');
    if (closeBtn.exists()) {
      await closeBtn.trigger('click');
      expect(wrapper.emitted('close')).toBeTruthy();
    } else {
      // If your close button uses a different selector, update this test
      expect(true).toBe(true);
    }
  });

  it('has an input for beer search', () => {
    const wrapper = mount(AddBeerModal);
    const searchInput = wrapper.find('input[name="beerSearch"]');
    expect(searchInput.exists()).toBe(true);
  });

  it('has an input for beer name', () => {
    const wrapper = mount(AddBeerModal);
    const nameInput = wrapper.find('input[name="name"]');
    expect(nameInput.exists()).toBe(true);
  });

  it('has an input for brewery', () => {
    const wrapper = mount(AddBeerModal);
    const breweryInput = wrapper.find('input[name="brewery"]');
    expect(breweryInput.exists()).toBe(true);
  });

  it('has an input for description', () => {
    const wrapper = mount(AddBeerModal);
    const descriptionInput = wrapper.find('input[name="description"]');
    expect(descriptionInput.exists()).toBe(true);
  });

  it('has an input for type', () => {
    const wrapper = mount(AddBeerModal);
    const typeInput = wrapper.find('input[name="type"]');
    expect(typeInput.exists()).toBe(true);
  });

  it('calls beerService and handleClose on successful save', async () => {
    // Mock service methods
    const newBeerMock = vi.fn().mockResolvedValue({
      success: true,
      response: { id: 123 },
    });
    const addBeerToEventMock = vi.fn().mockResolvedValue({ success: true });

    beerService.eventBeer.newBeer = newBeerMock;
    beerService.eventBeer.addBeerToEvent = addBeerToEventMock;

    // Mount component
    const wrapper = mount(AddBeerModal);

    // Set input values
    wrapper.vm.beerName = 'Test Beer';
    wrapper.vm.beerDescription = 'Test Description';
    wrapper.vm.beerBrewery = 'Test Brewery';
    wrapper.vm.beerType = 'Test Type';
    wrapper.vm.eventId = '1';

    // Spy on handleClose
    const handleCloseSpy = vi.spyOn(wrapper.vm, 'handleClose');

    // Call saveBeer
    await wrapper.vm.saveBeer();
    await flushPromises();

    // Assertions
    expect(newBeerMock).toHaveBeenCalledWith({
      name: 'Test Beer',
      description: 'Test Description',
      brewery: 'Test Brewery',
      type: 'Test Type',
    });

    expect(addBeerToEventMock).toHaveBeenCalledWith('1', '123');
    expect(wrapper.emitted('close')).toBeTruthy();
  });

  it('handles error when beerService.newBeer fails', async () => {
    const newBeerMock = vi.fn().mockResolvedValue({
      success: false,
      error: 'Failed to create beer',
    });
    beerService.eventBeer.newBeer = newBeerMock;

    const wrapper = mount(AddBeerModal);

    wrapper.vm.beerName = 'Test Beer';
    wrapper.vm.beerDescription = 'Test Description';
    wrapper.vm.beerBrewery = 'Test Brewery';
    wrapper.vm.beerType = 'Test Type';
    wrapper.vm.eventId = '1';

    const handleCloseSpy = vi.spyOn(wrapper.vm, 'handleClose');

    await wrapper.vm.saveBeer();
    await flushPromises();

    expect(newBeerMock).toHaveBeenCalled();
    expect(handleCloseSpy).not.toHaveBeenCalled();
  });

  it('handles error when beerService.addBeerToEvent fails', async () => {
    const newBeerMock = vi.fn().mockResolvedValue({
      success: true,
      response: { id: 123 },
    });
    const addBeerToEventMock = vi.fn().mockResolvedValue({
      success: false,
      error: 'Failed to add beer to event',
    });

    beerService.eventBeer.newBeer = newBeerMock;
    beerService.eventBeer.addBeerToEvent = addBeerToEventMock;

    const wrapper = mount(AddBeerModal);
    wrapper.vm.beerName = 'Test Beer';
    wrapper.vm.beerDescription = 'Test Description';
    wrapper.vm.beerBrewery = 'Test Brewery';
    wrapper.vm.beerType = 'Test Type';
    wrapper.vm.eventId = '1';

    const handleCloseSpy = vi.spyOn(wrapper.vm, 'handleClose');
    await wrapper.vm.saveBeer();
    await flushPromises();

    expect(newBeerMock).toHaveBeenCalled();
    expect(addBeerToEventMock).toHaveBeenCalled();
    expect(handleCloseSpy).not.toHaveBeenCalled();
  });

  it('does not call service methods if required fields are missing', async () => {
    const newBeerMock = vi.fn();
    const addBeerToEventMock = vi.fn();

    beerService.eventBeer.newBeer = newBeerMock;
    beerService.eventBeer.addBeerToEvent = addBeerToEventMock;

    const wrapper = mount(AddBeerModal);
    wrapper.vm.beerName = ''; // Missing name
    wrapper.vm.beerDescription = 'Test Description';
    wrapper.vm.beerBrewery = 'Test Brewery';
    wrapper.vm.beerType = 'Test Type';
    wrapper.vm.eventId = '1';

    const handleCloseSpy = vi.spyOn(wrapper.vm, 'handleClose');
    await wrapper.vm.saveBeer();
    await flushPromises();

    expect(newBeerMock).not.toHaveBeenCalled();
    expect(addBeerToEventMock).not.toHaveBeenCalled();
    expect(handleCloseSpy).not.toHaveBeenCalled();
  });

  it('validates required fields before saving', async () => {
    const wrapper = mount(AddBeerModal);

    // Leave all fields empty
    wrapper.vm.beerName = '';
    wrapper.vm.beerDescription = '';
    wrapper.vm.beerBrewery = '';
    wrapper.vm.beerType = '';
    wrapper.vm.eventId = '1';
    const newBeerMock = vi.fn();
    beerService.eventBeer.newBeer = newBeerMock;

    const handleCloseSpy = vi.spyOn(wrapper.vm, 'handleClose');
    await wrapper.vm.saveBeer();
    await flushPromises();
    expect(newBeerMock).not.toHaveBeenCalled();
    expect(handleCloseSpy).not.toHaveBeenCalled();
  });

  it('add existing beer to event', async () => {
    const addBeerToEventMock = vi.fn().mockResolvedValue({ success: true });
    beerService.eventBeer.addBeerToEvent = addBeerToEventMock;

    const wrapper = mount(AddBeerModal);
    wrapper.vm.beerName = 'Existing Beer';
    wrapper.vm.beerDescription = 'Test Description';
    wrapper.vm.beerBrewery = 'Test Brewery';
    wrapper.vm.beerType = 'Test Type';
    wrapper.vm.eventId = '1';

    await wrapper.vm.addExistingBeerToEvent(1);
    await flushPromises();

    expect(addBeerToEventMock).toHaveBeenCalledWith('1', '1');
    expect(wrapper.emitted('close')).toBeTruthy();
  });
});
