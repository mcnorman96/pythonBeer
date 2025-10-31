/* global describe, it, cy, beforeEach, afterEach, before, after, Cypress */
Cypress.Commands.add('deleteEventByName', (eventName) => {
  cy.request('GET', 'http://localhost:8000/events').then((resp) => {
    const event = resp.body.response.find((e) => e.name === eventName);
    if (event) {
      cy.request({
        method: 'DELETE',
        url: `http://localhost:8000/events/${event.id}`,
        headers: {
          Authorization: `Bearer ${window.localStorage.getItem('token')}`,
        },
      });
    }
  });
});

describe('Events Id page', () => {
  let eventName;
  let eventDescription;
  let LOCAL_STORAGE_MEMORY = {};
  const editButton = 'button[name=editEvent]';
  const addBeerButton = 'button[name=addBeer]';
  const editBeerButton = 'button[name=editBeer]';
  const viewRatingsButton = 'button[name=viewRatings]';
  const addRatingButton = 'button[name=addRating]';

  // const testBeer = {
  //   name: 'Test Beer',
  //   description: 'Fresh taste',
  //   brewery: 'To øl',
  //   type: 'IPA'
  // }

  before(() => {
    eventName = 'Marcus new event';
    eventDescription = 'This is a test event';

    // Login
    cy.visit('http://localhost:3000/login');
    cy.wait(500);
    cy.get('input[name="username"]').type('alice');
    cy.get('input[name="password"]').type('password1');
    cy.get('button[type="submit"]').click();
    cy.wait(500);

    // Creating test event
    cy.visit('http://localhost:3000/events');
    cy.wait(500);
    cy.get('button[name="newEvent"]').click();
    cy.get('input[name=eventName]').type(eventName);
    cy.get('input[name=eventDescription]').type(eventDescription);
    cy.get('button[name=saveEvent]').click();
  });

  beforeEach(() => {
    cy.window().then((win) => {
      Object.keys(LOCAL_STORAGE_MEMORY).forEach((key) => {
        win.localStorage.setItem(key, LOCAL_STORAGE_MEMORY[key]);
      });
    });

    cy.visit('http://localhost:3000/events');
    cy.wait(500);
    cy.contains(eventName).click();
    cy.wait(500);
  });

  afterEach(() => {
    cy.window().then((win) => {
      LOCAL_STORAGE_MEMORY = {};
      for (let i = 0; i < win.localStorage.length; i++) {
        const key = win.localStorage.key(i);
        LOCAL_STORAGE_MEMORY[key] = win.localStorage.getItem(key);
      }
    });
  });

  after(() => {
    cy.deleteEventByName(eventName);
  });

  it('loads successfully', () => {
    cy.contains(eventName);
    cy.get(editButton);
    cy.get(addBeerButton);
  });

  it('New event name and description', () => {
    eventName = 'Anton new event';
    eventDescription = 'This is a newer description';

    cy.get(editButton).click();
    cy.get('input[name=name]').type(eventName);
    cy.get('input[name=description]').type(eventDescription);
    cy.get('button[name=updateEvent]').click();
    cy.wait(500);

    cy.contains(eventName);
    cy.contains(eventDescription);
  });

  // it('Add new beer to event', () => {
  //   cy.get(addBeerButton).click();

  //   cy.get('input[name=name]').type(testBeer.name);
  //   cy.get('input[name=description]').type(testBeer.description);
  //   cy.get('input[name=brewery]').type(testBeer.brewery);
  //   cy.get('input[name=type]').type(testBeer.type);
  //   cy.get('button[name=saveBeer]').click();
  //   cy.wait(500);

  //   cy.contains(testBeer.name);
  //   cy.contains(testBeer.description);
  //   cy.contains(testBeer.brewery);
  //   cy.contains(testBeer.type);
  // })

  it('Add existing beer to event', () => {
    cy.get(addBeerButton).click();

    cy.get('input[name=beerSearch]').type('dark st');
    cy.contains('Dark Stout').click();
    cy.wait(500);

    cy.contains('Dark Stout');
    cy.contains('Brewery B');
    cy.contains('Stout');
    cy.contains('Rich and creamy');
  });

  it('Add new rating', () => {
    cy.get(addRatingButton).click();
    cy.get('input[name=taste]').clear().type(5);
    cy.get('input[name=aftertaste]').clear().type(5);
    cy.get('input[name=smell]').clear().type(5);
    cy.get('input[name=design]').clear().type(5);
    cy.get('input[name=score]').clear().type(5);
    cy.get('button[name=saveRating]').click();
    cy.wait(500);

    cy.get('text[name=taste]').should('contain', '5');
    cy.get('text[name=aftertaste]').should('contain', '5');
    cy.get('text[name=smell]').should('contain', '5');
    cy.get('text[name=design]').should('contain', '5');
    cy.get('text[name=score]').should('contain', '5');
  });

  it('View ratings', () => {
    cy.get(viewRatingsButton).click();
    cy.wait(500);

    cy.contains('alice');
    cy.get('text[name=taste]').should('contain', '5');
    cy.get('text[name=aftertaste]').should('contain', '5');
    cy.get('text[name=smell]').should('contain', '5');
    cy.get('text[name=design]').should('contain', '5');
    cy.get('text[name=score]').should('contain', '5');
  });

  it('Edit beer info', () => {
    cy.get(editBeerButton).click();
    cy.get('input[name=name]').clear().type('Dark Stouts');
    cy.get('input[name=description]').clear().type('Brewery Bs');
    cy.get('input[name=brewery]').clear().type('Stouts');
    cy.get('input[name=type]').clear().type('Rich and creamys');
    cy.get('button[name=updateBeer]').click();
    cy.wait(500);

    cy.contains('Dark Stouts');
    cy.contains('Brewery Bs');
    cy.contains('Stouts');
    cy.contains('Rich and creamys');

    cy.get(editBeerButton).click();
    cy.get('input[name=name]').clear().type('Dark Stout');
    cy.get('input[name=description]').clear().type('Brewery B');
    cy.get('input[name=brewery]').clear().type('Stout');
    cy.get('input[name=type]').clear().type('Rich and creamy');
    cy.get('button[name=updateBeer]').click();
    cy.wait(500);

    cy.contains('Dark Stout');
    cy.contains('Brewery B');
    cy.contains('Stout');
    cy.contains('Rich and creamy');
  });

  it('Delete beer from event', () => {
    cy.get(editBeerButton).click();
    cy.get('button[name=deleteBeer]').click();
    cy.wait(500);

    // cy.contains('Dark Stout').should('not.exist');
  });
});
