# URL Shortener :scissors:

URL Shortener is an API written in Python using the FastAPI framework that can shorten a particular URL.
You execute a `POST` request to the API or you can use the home page to generate an 8 character shortened URL from the URL that you enter.
The returned shortened URL will redirect the user to the original long URL when the shortened URL is used in a browser or in some other redirection mechanism.

## Shortening Algorithm

The shortened URL has the following design goals and constraints:
- Shortened URL MUST be deterministic
   - Given the same input, the same shortened URL must be produced as an output.
- Shortened URL MUST have a shorter length (8)
   - The length SHOULD be configurable
- Shortened URL's character set MUST be: `A-Za-z0-9`
- Shortened URL SHOULD not be easily guessed
   - This reduces the surface area of a threat

[Shake 256](https://en.wikipedia.org/wiki/SHA-3#Instances:~:text=d%2C128) is used as the hashing algorithm.
SHAKE is an extendable-output functions (XOFs), i.e. it can produce a variable length deterministic output.
The default output character set is hex digits: `a-z0-9`

See also:
- https://github.com/cds-snc/url-shortener/issues/87
- https://medium.com/asecuritysite-when-bob-met-alice/shake-stirs-up-crypto-7d87f3cf39f4

### Clone the repo:
Clone the repo by typing
```bash
git clone https://github.com/cds-snc/url-shortener.git
```
And now change into the project directory
```bash
cd url-shortener
```
## Running the project

The URL shortener is an application that uses FastAPI and it is written in python.

There are a few ways to run the app:
- GitHub Codespaces
- VSCode and Devcontainers

### Running using GitHub Codespaces
Once the Codespace is finished building, spin up the app: 
```bash
cd api
make dev
```
Logs go to stdout.

### Running using VSCode and Devcontainers
Once you have the [Devcontainers prerequisites installed](https://code.visualstudio.com/docs/devcontainers/tutorial), open the project in the provided devcontainer. When it is finished building, you will need to create a `api/.env` file:
```bash
cp api/.env.example api/.env
```
Next, provide values for the environment variables in the `api/.env` file and then start the app:
```bash
cd api
make dev
```

### How to use the API

To get the webpage, you can simply run the project at http://localhost:8000 

To test the API, you can use [curl](https://curl.se/) or any other HTTP client.  You will need to provide a valid `Authorization` header with a `Bearer` token:

#### cURL
```bash
curl -X POST http://localhost:8000/v1 \
-H "Authorization: Bearer auth_token_app" \
-H "Content-Type: application/json" \
-d '{"original_url": "https://digital.canada.ca"}'

{"short_url":"http://127.0.0.1:8000/IcWuXU64","original_url":"https://digital.canada.ca","status":"OK"}
```


### Running end-to-end and accessbility tests using Cypress

You can run end-to-end tests by doing the following:

1. Start the dev server locally, ex: `make e2e-dev` in the `./api` folder.
2. Run `make e2e` to start a docker container that has cypress installed as well as the `cypress-axe` extension for the `axe-core` package.

Videos and screenshots of the test runs can be found in `./api/e2e/cypress/screenshots|videos` folder.