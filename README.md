# Babylon programming task
Simple URL shortener service in Python using Flask and minimal DB storage.

The technologies used for the implementation have been the following:
* Flask
* PostgreSQL
* psycopg2
* SQLAlchemy
* Flask_SQLAlchemy
* Alembic
* validators
* gunicorn (for prod deploy)

## Purpose
The implemented system is a URL shortener that simply accepts an input URL to then provide a short version for it, and another endpoint that, when accessing a short url, redirects to the original one. The service has been thought with the following restrictions and evolution steps in mind:
* This system has been a quick implementation that allows pushing the solution to production with the complete intended complete functionality, but leaving some more complex concepts for future iterations.
* This should be treated as an MVP. We can see how it behaves and how it is used, and then act according to how the product needs to evolve.
* The solution has a basic structure for a small server, but with keeping a minimum separation of concerns, allowing easy readability and extension in case the product needs to grow.
* The work for future iterations has been thought through in a posterior section, and the solution is designed so that it is relatively easy to know when to start moving to the more complete version.

## Current version
This URL shortener has been implemented the following way:
* A POST query can create a new short URL for a given URL. When provided with the same URL, the system will continue to generate new short URLs. This allows in future iterations to track exactly how each short URL behaves. So for example, if user authentication were included, it would be possible to easily track how each URL for each user is accessed, even if the same links have been previously entered into the system.
```
POST /shorten_url
request:
{
    "url": "http://www.google.com"
}
response:
{
    "shortened_url": "http://www.myservice.com/aI89Mn"
}
```
* A GET query trying to retrieve a short URL will reply with a redirect to the original page, which every browser will automatically follow. It also avoids some overhead against returning the complete original content, which we don't want to add to the system right now.
```
GET /aI89Mn
response:
    302 REDIRECT http://www.google.com
```

## Current implementation
The previous stack has been used the following way:
* Flask is the framework that allows serving the API.
  * It should be launched with gunicorn in production, as it allows "parallel" processing while I/O is being produced in the system (for example, accessing DB).
* PostgreSQL is the DB to store the short URLs and their original ones.
  * psycopg2 is used as a driver.
  * It contains a ShortURL model with an ID (primary key), original URL and short URL (unique). It also contains a trigger that automatically generates a random unique short URL for every newly inserted record.
  * The models are mapped from Python using SQLAlchemy and Flask_SQLAlchemy for easier setup.
  * Alembic is used to generate DB migrations when we want to include modifications in the DB models. For instance, if we were to include a counter for each shortened URL, we could generate a migration and then apply it in production.
* validators is a library used to properly validate the input URLs.
* Some tests have been implemented using pytest.

## How to run the service
The system simply needs a running PostgreSQL instance to work. The steps to execute it would be the following:
* Not needed but recommended. Create a virtual environment for the project with virtualenv.
* Add an environment variable DATABASE_URL that points to the PostgreSQL instance. For example, `postgres:///babylon` or `postgres://myuser:mypass@localhost:5432/babylon`. In the virtualenv it can be added at the end of the bin/activate file as a typical bash export.
* Install the dependencies with `pip install -r requirements.txt`.
* Run the server with `./run.py`. It will be accessible at `http://127.0.0.1:5000`.

## How to run tests
* Install the dependencies with `pip install -r requirements-test.txt`.
* Execute the tests with `pytest tests/`

## Potential improvements
* For an initial basic scaling, the gunicorn settings could be tweaked to spawn more server instances. If this were not enough, more servers could be included, as the URL generation is centralised in the DB, which would be in charge of avoiding short URL clashes.
* Currently the short URLs are generated using a trigger in the database. This works when the load is relatively low, but as it grows it might start giving trouble with the integrity, as it is configured as a unique field. This can be monitored in the logs, and if a service as NewRelic is used, alerts can be configured to send an email when a certain amount of logs/exceptions are caught.
* The system has very basic logging. For the moment it is simply used to track the previous issue, but its usage should be extended to the whole service by applying the correct levels of severity.
* The general operation of the system has been tested with integration tests and serialization with unit tests. Still, some more unit tests should be added for the individual functions, such as the finders or the storage through repositories.
* For the moment the only input in the system is a URL to shorten. It is very simply validated with a couple of checks, but a more generic solution should be adopted if the system grew and more validation was required. A library as Cerberus should be considered, which could wrap each endpoint and check all its input before it even arrives to the actual endpoint code.

## Scaling
As explained before, this is a functional MVP of the system, so we can check how it works, but also some issues have been identified. To solve them, the following steps are proposed:
* Include a worker server, which will be in charge of generating new short URLs.
* Add a Redis instance, which will contain a set of short URLs to be used from the API.
* Add a RabbitMQ instance, which will be used to exchange messages between the API and the new worker.
* Add the Celery library, to be able to create scheduled tasks in the worker server and easily handle exchange.

With this new structure, the system would work the following way:
* The Redis instance will contain a pool of X short URLs. The exact amount can be calculated based on an analysis of the usage of the platform.
* Each time a POST is issued to shorten a URL, the server will simply take a random string from the Redis pool, store it in the database and issue a message through Celery to RabbitMQ.
* The worker will be listening to messages through Celery. When received, it will create new random short URLs based on the current pool and the values in the database, and will add them to Redis. How many of them to generate each time can also be based on an analysis of the system and its usage.

This new architecture provides a much more flexible and more scalable environment than the MVP.
* The database is not a bottleneck to generate short URLs anymore. There is always a pool available to get new ones.
* The Redis instance is quick enough to almost instantly return a valid short URL, making the endpoint much quicker.
* If this were not enough, say the server cannot handle the amount of requests, the gunicorn settings can be tweaked to spawn more server instances. Or new servers can also be included, as they would be sharing the Redis instance, which would be consistent among servers, and the GETs to the database would produce no conflicts.
* Likewise with the workers, if short URLs have to be produced quicker, Celery can be tweaked to spawn more workers, or more worker servers can be included, as they can work in parallel.
