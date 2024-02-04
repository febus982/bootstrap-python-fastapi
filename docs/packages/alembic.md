# Alembic

[Alembic](https://alembic.sqlalchemy.org/en/latest/) setup is super-easy but 
we implement some extra features on top of the default configuration:

* Support for both sync and async SQLAlchemy engines at the same time
* Grabs the database information from the `SQLAlchemyBindManager` configuration
  in the application, so we won't have duplicate configuration.
* `alembic.ini` (not technically part of the python package) is setup to
  prepend migration files with the generation datetime for natural file ordering.
