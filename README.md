# MedHub FastAPI template

A simple starting point for your [FastAPI](https://fastapi.tiangolo.com) application that uses
[Supertokens](https://supertokens.com) for user auth.


## About

The template includes some helper scripts to help you get started:
1. Makefile for dependency management with `pip-tools`
2. Dockerfile and compose files for local development
3. SQLAlchemy for ORM (uses async engine) and Alembic for database migrations
4. Simple authentication for docs page
5. CRUD operations generic class with pagination
6. Support for API versioning (`https://api.yourdomain.com/v1/`)

TDB:
- Tests

Make sure to mark the `app/` folder as source in your IDE otherwise you'll get import errors.

## How to use

Just click on "Use this template" button to start coding. You'll find [a dummy app](app/api/v1/blog_post.py) that
demonstrates how to use [CRUD factory](app/db/crud/base.py).

### Local setup

The following command will start a Postgres database and a Supertokens core locally in Docker:
```shell
docker compose -f docker-compose-local.yml up -d
```

If you want to run your app containerized you can run the other compose file:
```shell
docker compose -f docker-compose-test.yml up -d
```
