# URL Shortener 

Url shortener is an API written in Python using the FastAPI framework that can shorten a particular url. You execute a POST request to the API or you can 
use the home page to generate an 8 character shortened url from long url that you enter. The returned shortened url
will redirect the user to the original long url when the shortened url is used in a browser or in some other redirection mechanism.

## Running the project
The url shortener is an application that uses FastAPI and it is written in python. The simplest way to run it is if you use Docker and docker-compose.
You need to have Docker installed to be able to run it 
via docker-compose. Steps to get started are below.

### Clone the repo:
Clone the repo by typing
```
git clone https://github.com/cds-snc/url-shortener.git
```
And now change into the project directory
```
cd url-shortener
```

### Running using Docker Compose
Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application’s services. Then, with a single command, you create and start all the services from your configuration.

You can use Docker Compose to build an application container along with a Postgres database. It will map your local files into a Docker container and spin up a PostgreSQL database.
The app runs on port 8000, the database at port 5432 (u: user, p: password) and will be served at http://localhost:8000 or http://0.0.0.0:8000.

Spin up the app: 
```
docker-compose up -d --build
```
Initialize database and run migrations: 
```
docker-compose exec api alembic upgrade head
```
Get logs: 
```
docker-compose logs
```
Connect to the psql database: 
```
docker-compose exec db psql --username=dev --dbname=dev
```

### How to use the API

To get the webpage, you can simply run the project at http://localhost:8000 

To use the API, you can use [httpie](https://httpie.io/), [postman](https://www.postman.com/) or [curl](https://curl.se/)

#### Postman
Execute a POST request with 

```
http://localhost:8000/v1 
```
In the body pass the following:
```{
    "original_url": "http://blah_blah.com"
}
```

#### curl
```
curl -X POST -d '{"original_url": "https://google.com"}' -H "Content-Type: application/json" http://localhost:8000/v1

{"status":"OK","short_url":"xM_ElQWt"}
```

#### httpie
```
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
