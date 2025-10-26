/* global describe, it, cy, before, beforeEach, afterEach */
describe('Toplist page', () => {
  let LOCAL_STORAGE_MEMORY = {};

  before(() => {
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
    cy.visit('http://localhost:3000/toplist');
    cy.contains('Toplist');
  });
});
