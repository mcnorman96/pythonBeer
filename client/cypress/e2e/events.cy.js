/* global describe, it, cy, beforeEach, Cypress, before, afterEach */
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

describe('Events page', () => {
  let eventName;
  let LOCAL_STORAGE_MEMORY = {};

  before(() => {
    eventName = 'Marcus new event';

    // Login
    cy.visit('http://localhost:3000/login');
    cy.wait(500);
    cy.get('input[name="username"]').type('alice');
    cy.get('input[name="password"]').type('password1');
    cy.get('button[type="submit"]').click();
    cy.wait(500);
  });

  beforeEach(() => {
    cy.window().then((win) => {
      Object.keys(LOCAL_STORAGE_MEMORY).forEach((key) => {
        win.localStorage.setItem(key, LOCAL_STORAGE_MEMORY[key]);
      });
    });

    cy.visit('http://localhost:3000/events');
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

  it('loads successfully', () => {
    cy.contains('Events');
    cy.contains('New Event');
  });

  it('New event modal opens', () => {
    cy.get('button[name="newEvent"]').click();
    cy.contains('Add New Event');
    cy.contains('Name');
    cy.contains('Description');
  });

  it('Adding new event', () => {
    cy.get('button[name="newEvent"]').click();
    cy.get('input[name=eventName]').type('Marcus new event');
    cy.get('input[name=eventDescription]').type('This is a new event');
    cy.get('button[name=saveEvent]').click();
    cy.wait(500);
    cy.contains('Marcus new event');
    cy.deleteEventByName(eventName);
  });

  it('Clicking on event brings you to the single event page', () => {
    cy.get('button[name="newEvent"]').click();
    cy.get('input[name=eventName]').type('Marcus new event');
    cy.get('input[name=eventDescription]').type('This is a new event');
    cy.get('button[name=saveEvent]').click();
    cy.wait(500);
    cy.contains('Marcus new event').click();
    cy.url().should('include', '/events/');
    cy.deleteEventByName(eventName);
  });
});
