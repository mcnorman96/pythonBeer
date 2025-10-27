/* global describe, it, cy */
describe('Login page', () => {
  it('loads successfully', () => {
    cy.visit('http://localhost:3000/register');
    cy.contains('Register');
    cy.contains('Username');
    cy.contains('Password');
    cy.contains('Email');
  });

  it('shows validation errors for empty fields', () => {
    cy.visit('http://localhost:3000/register');
    cy.wait(500);
    cy.get('button[type="submit"]').click();
    cy.wait(1500);
    cy.contains('Username, Password and Email is required');
  });

  // it('Registered successfully', () => {
  //   cy.visit('http://localhost:3000/register');
  //   cy.wait(500);
  //   cy.get('input[name="username"]').type('user');
  //   cy.get('input[name="password"]').type('pass');
  //   cy.get('input[name="email"]').type('newone@gmail.com');
  //   cy.get('button[type="submit"]').click();
  //   cy.wait(500);
  //   cy.contains('Registration successful! You can now log in.');
  // });
});
