# Bootstrap

The `bootstrap` package contains logic that is shared among the external layer
(i.e. `http_app`, `celery_worker`, etc.).

It contains the following submodules and packages (and related responsibilities):

* `bootstrap.bootstrap`: The application initialisation logic (database, logging,
  celery tasks) necessary to run the domain logic. It uses `bootstrap.config` and
  `bootstrap.di_container` subpackages. It does not contain the specific HTTP
  framework initialisation (or other frameworks such as GRPC).
* `bootstrap.config`: The application config models, based on `BaseSettings`
  and `BaseModel` from `pydantic` package to get the values from
  environment variables.
* `bootstrap.di_container`: The dependency injection container configuration.
* `bootstrap.storage`: The storage configuration (SQLAlchemy). This setup uses
  [Imperative Mapping](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#imperative-mapping)
  so that our models remains simple classes.

/// warning | Note about SQLAlchemy ORM Imperative Mapping

Even if the code for models appears to remain simple classes, imperative mapping
transforms them behind the scenes. However, the code in our application should not
rely on such specific capabilities otherwise we would bind our code to SQLAlchemy.

To handle database operations we use a repository class that is aware of SQLAlchemy.
In this way, should we need to change our storage implementation (e.g. switch to MongoDB),
we'll only need to change the repository class, without having to change anything in
our application logic.
///
