# Models

This package is the innermost layer of our application. It contains
our application models, which use either `dataclasses` or `attrs`
(for more advanced features like frozen models)

We consciously chose not to use `pydantic` which comes out of the box
with `FastAPI`.

Reasoning:

* `attrs` provides additional functionalities over `dataclasses` and 
  is slightly more flexible than pydantic
* `pydantic` does an automatic validation which always adds computational
  time. It's not model responsibility to validate its own data, and we
  prefer to opt-in for validation, rather than opt-out.
* `pydantic` does not work very well with `SQLAlchemy` ORM imperative
  configuration, and it would have been necessary to duplicate models
  rather than define mappings between models and database, creating
  undesired complexity
