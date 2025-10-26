/* global describe, it, cy */
describe('Login page', () => {
  it('loads successfully', () => {
    cy.visit('http://localhost:3000/login');
    cy.contains('Login');
    cy.contains('Username');
    cy.contains('Password');
  });

  it('shows validation errors for empty fields', () => {
    cy.visit('http://localhost:3000/login');
    cy.wait(500);
    cy.get('button[type="submit"]').click();
    cy.wait(1500);
    cy.contains('Username and password is required');
  });

  it('shows error for invalid credentials', () => {
    cy.visit('http://localhost:3000/login');
    cy.wait(500);
    cy.get('input[name="username"]').type('wronguser');
    cy.get('input[name="password"]').type('wrongpass');
    cy.get('button[type="submit"]').click();
    cy.wait(500);
    cy.contains('Login failed');
  });

  it('logs in with valid credentials', () => {
    cy.visit('http://localhost:3000/login');
    cy.wait(500);
    cy.get('input[name="username"]').type('alice');
    cy.get('input[name="password"]').type('password1');
    cy.get('button[type="submit"]').click();
    cy.wait(500);
    cy.url().should('not.include', '/login');
  });
});
