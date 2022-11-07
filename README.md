# FastAPI + Supertokens template

A simple starting point for your [FastAPI](https://fastapi.tiangolo.com) application that uses
[Supertokens](https://supertokens.com) for user auth.

## About

The template includes the following to help you to get started:
1. Makefile for dependency management with `pip-tools`
2. Dockerfile and compose files for local development
3. SQLAlchemy for ORM (uses async engine) and Alembic for database migrations
4. Simple authentication for docs page
5. CRUD operations generic class with pagination
6. Support for API versioning (`https://api.yourdomain.com/v1/`)

TDB:
- Tests

## How to use

Make sure to mark the `app/` folder as source in your IDE otherwise you'll get import errors.
And since all your code (except tests) lives inside `app/` folder, you should import modules like this:
```python
from core.config import settings
```

and NOT like this:
```python
# this will throw an error!
from app.core.config import settings
```

### Start coding

Just click on that green `Use this template` button to start coding. There is [a dummy app](app/api/v1/blog_post.py) that
is already implemented for you so that you can quickly learn how to use the [CRUD factory](app/db/crud/base.py).

### Local setup

The following command will start a Postgres database and a Supertokens core locally in Docker:
```shell
docker compose -f docker-compose-local.yml up -d
```

If you want to run your app containerized you can run the other compose file:
```shell
docker compose -f docker-compose-test.yml up -d
```

If you run the command above without changing the code, you can find the
[documentation page here](http://localhost:8001/docs). The default username is `docs_user`
and the password is `simple_password`.
