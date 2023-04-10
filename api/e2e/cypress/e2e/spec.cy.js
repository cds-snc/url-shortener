import 'cypress-axe'

it("loads the login page to cache the assets", () => {
    cy.visit("/en/login");
});

it("loads the login page in English", () => {
    cy.visit("/en/login");
    cy.injectAxe();
    cy.get("gcds-button").should("contain", "Login");
    cy.checkA11y()
});

it("loads the login page in Fench", () => {
    cy.visit("/fr/login");
    cy.injectAxe();
    cy.get("gcds-button").should("contain", "Connexion");
    cy.checkA11y()
});
