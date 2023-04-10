import 'cypress-axe'

it("loads the login page", () => {
    cy.visit("/login");
    cy.injectAxe();
    cy.get("gcds-button").should("contain", "Login");
    cy.checkA11y()
});

