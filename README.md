# hubster

**hubster** is a simple, concurrent, prototype, command-line Github api scraper for downloading repositories based off of user accounts.

## Quick Start

1. Copy .env.example to .env and fill in your Github username and password. If your account has 2FA enabled, you will have to use a Personal Access Token as your password.
2. In a terminal, change to the root directory of the project, and run `docker-compose build`. (If you don't have `docker` or `docker-compose`, start here: <https://docs.docker.com/compose/>)
3. Next, run:

```sh
docker-compose run --rm hubster /bin/sh -c "./manage.py migrate"
```

> This should create your initial database schema based off of the Django models.

4. Next, let's scrape some data. First we'll try the defaults:

```sh
docker-compose run --rm hubster /bin/sh -c "./scraper.py"
```

> If you'd like to see all the options available for `scraper.py`, add the flag `--help`

5. We can navigate to it now, if we start our server:

```sh
docker-compose up
```

6. Navigate to `http://localhost:8000/repos` or send a GET request with `Content-Type: application/json` to that URL.

   > By default, the API will return the first 25 results

7. Using the Django query syntax, we have powerful queries out of the box. Let's find all the repos currently scraped who have been forked more than 10 times:

```sh
GET localhost:8000/repos?forks_count__gt=10
```

# scraper.py

## --help

```sh
usage: scraper.py [-h] [-c CONCURRENCY] [-q QUANTITY] [-s START_ID]

Hubster Github scraper

optional arguments:
  -h, --help            show this help message and exit
  -c CONCURRENCY, --concurrency CONCURRENCY
                        Number of concurrent connections to scrape with
  -q QUANTITY, --quantity QUANTITY
                        Total number of users to scrape before quitting
  -s START_ID, --start START_ID
                        User ID to start scraping repos from (exclusive),
                        e.g., 46 will start scraping at 47. By default, it
                        will start from the max ID in the database.
```

Since `scraper.py` is oriented around users, you can limit the number of users by setting the `-q QUANTITY` flag. This will pull all the repos associated with that user. This allows the scraper to easily pick up from the next User for continuous scraping.

# API Features

## Filter Syntax

The API supports [Django's `filter` syntax](https://docs.djangoproject.com/en/2.2/ref/models/querysets/) by means of passing in query parameters.

For example,

1. Simple equivalency test:

```sh
repos?has_wiki=False
```

2. Joins (these appear as sub-objects in the JSON):

```sh
repos?owner__hireable=True
```

3. Greater/Less than:

```sh
repos?forks_count__gt=10
```

## Sorting syntax

The API supports [Django's `order_by` syntax](https://docs.djangoproject.com/en/2.2/ref/models/querysets/) by means of passing in a list of `order_by` fields.

1. Simple order by ASC:

```sh
repos?order_by=stargazers_count
```

2. Simple order by DESC:

```sh
repos?order_by=-stargazers_count
```

3. Multiple order bys not available at this time
