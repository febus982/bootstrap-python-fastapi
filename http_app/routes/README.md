# Routes

This package contains only the HTTP routes. They are responsible for:

* HTTP Request validation (FastAPI should take care of this automatically)
* Data transformation between Pydantic models (schemas) and
  application models (from models package)
* HTTP Response preparation