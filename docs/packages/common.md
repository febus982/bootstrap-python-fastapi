# Common

The `common` module contains logic that is shared among the external layer
(i.e. `http_app`, `celery_worker`, etc.).

It contains 3 submodules (and related responsibilities):

* `common.bootstrap`: The application initialisation logic (database, logging,
  celery tasks) necessary to run the domain logic. It uses `common.config` and
  `common.di_container` subpackages. It does not contain the specific HTTP
  framework initialisation (or other frameworks such as GRPC).
* `common.config`: The application config models, based on `BaseSettings`
  and `BaseModel` from `pydantic` package to get the values from
  environment variables.
* `common.di_container`: The dependency injection container configuration.
