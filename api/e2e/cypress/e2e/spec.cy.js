import 'cypress-axe'
const { registerCommand } = require('cypress-wait-for-stable-dom')
registerCommand()

// This is a custom command to log violations to the terminal for a11y testing
function terminalLog(violations) {
    cy.task(
        'log',
        `${violations.length} accessibility violation${violations.length === 1 ? '' : 's'
        } ${violations.length === 1 ? 'was' : 'were'} detected`
    )
    // pluck specific keys to keep the table readable
    const violationData = violations.map(
        ({ id, impact, description, nodes }) => ({
            id,
            impact,
            description,
            nodes: JSON.stringify(nodes),
        })
    )

    cy.task('table', violationData)
}

describe("Login page in English", () => {
    beforeEach(() => {
        cy.visit("/en/login");
        // cy.injectAxe();
        cy.waitForStableDOM({ pollInterval: 1000, timeout: 10000 })
    });

    it("has a login button", () => {
        cy.get("gcds-button").should("contain", "Login");
    });

    // it("has no detectable a11y violations on load", () => {
    //     cy.checkA11y(null, null, terminalLog)
    // })
});

describe("Login page in French", () => {
    beforeEach(() => {
        cy.visit("/fr/connexion");
        // cy.injectAxe();
        cy.waitForStableDOM({ pollInterval: 1000, timeout: 10000 })
    });

    it("has a login button", () => {
        cy.get("gcds-button").should("contain", "Connexion");
    });

    // it("has no detectable a11y violations on load", () => {
    //     cy.checkA11y(null, null, terminalLog)
    // })
});


describe("Redirect page", () => {
    beforeEach(() => {
        cy.visit("/foobar");
        // cy.injectAxe();
        cy.waitForStableDOM({ pollInterval: 1000, timeout: 10000 })
    });

    it("has two h1 elements", () => {
        cy.get("h1").should('have.length', 2)
    });

    it("has two link_container classes", () => {
        cy.get(".link_container").should('have.length', 2)
    });

    // it("has no detectable a11y violations on load", () => {
    //     cy.checkA11y(null, null, terminalLog)
    // })
});

describe("generate short URL page in English", () => {
    beforeEach(() => {
        cy.visit("/en");
        // cy.injectAxe();
        cy.waitForStableDOM({ pollInterval: 1000, timeout: 10000 })
    });

    it("has the correct H1 header", () => {
        cy.get("h1").should("contain", "Short and shareable URLs");
    });

    // it("has no detectable a11y violations on load", () => {
    //     cy.checkA11y(null, null, terminalLog)
    // })
});

describe("generate short URL page in French", () => {
    beforeEach(() => {
        cy.visit("/fr");
        // cy.injectAxe();
        cy.waitForStableDOM({ pollInterval: 1000, timeout: 10000 })
    });

    it("has the correct H1 header", () => {
        cy.get("h1").should("contain", "URLs courts et partageables");
    });

    // it("has no detectable a11y violations on load", () => {
    //     cy.checkA11y(null, null, terminalLog)
    // })
});