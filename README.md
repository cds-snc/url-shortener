# URL Shortener 

Url shortener is an API written in Python using the FastAPI framework that can shorten a particular url
You execute a POST request to the API or you can use the home page to generate an 8 character shortened url from long url that you enter
The returned shortened url will redirect the user to the original long url when the shortened url is used in a browser or in some other redirection mechanism.

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

The url shortener is an application that uses FastAPI and it is written in python.

There are two ways to run the app:
- Codespaces
- Docker Compose

### Running using Codespaces
Since we are using codespaces as a dev environment, we won't actually be using docker-compose to spin up the app.
Otherwise, you will run into issues with container within a container.

Spin up the app: 
```bash
cd api
make install-dev
make dev
```
Logs go to stdout.

### Running using Docker Compose
Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application’s services. Then, with a single command, you create and start all the services from your configuration.

You can use Docker Compose to build an application container along with a Postgres database. It will map your local files into a Docker container and spin up a PostgreSQL database.
The app runs on port 8000, the database at port 5432 (u: user, p: password) and will be served at http://localhost:8000 or http://0.0.0.0:8000.

Spin up the app: 
```bash
docker-compose up -d --build
```
Initialize database and run migrations: 
```bash
docker-compose exec api alembic upgrade head
```
Get logs: 
```bash
docker-compose logs
```
Connect to the psql database: 
```bash
docker-compose exec db psql --username=dev --dbname=dev
```

### How to use the API

To get the webpage, you can simply run the project at http://localhost:8000 

To use the API, you can use [httpie](https://httpie.io/), [postman](https://www.postman.com/) or [curl](https://curl.se/)

#### Postman
Execute a POST request with 

```bash
http://localhost:8000/v1 
```
In the body pass the following:
```json
{
    "original_url": "http://blah_blah.com"
}
```

#### curl
```bash
curl -X POST -d '{"original_url": "https://google.com"}' -H "Content-Type: application/json" http://localhost:8000/v1

{"status":"OK","short_url":"xM_ElQWt"}
```

#### httpie
```bash
http POST localhost:8000/v1 original_url=http://www.google.com

HTTP/1.1 200 OK
content-length: 38
content-type: application/json
date: Thu, 27 Jan 2022 23:44:15 GMT
server: uvicorn

{
    "short_url": "lo0KxaCb",
    "status": "OK"
}
```
