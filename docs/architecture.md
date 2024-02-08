# Application architecture

This application is structured following the principles of Clean Architecture.
Higher level layers can import directly lower level layers. An inversion of control
pattern has to be used for lower level layers to use higher level ones.

In this way our components are loosely coupled and the application logic
(the domains package) is completely independent of the chosen framework
and the persistence layer.

This is a high level list of the packages in this application template:

* `alembic` (database migration manager)
* `celery_worker` (async tasks runner)
* `common` (some common boilerplate initialisation shared by all applications )
* `http_app` (http presentation layer)
* `gateways` (database connection manager, repository implementation, event emitter, etc.)
* `domains` (services, repository interfaces)

Each domain inside the `domains` packages has its own layers, depending on the complexity but
it is usually composed by at least 2 layers:

* Boundary layer (domain logic, DTO, data access interfaces): This layer is the only one that
  should be ever used directly by actors not belonging to the domain (i.e. HTTP routes, other domains)
* Domain Logic (this can be multiple layers, depending on the complexity)
* Entity layer (domain models): No one except the domain should ever use directly the domain models.

This is a high level representation of the nested layers in the application:

```mermaid
flowchart TD
    subgraph "Framework & Drivers + Interface Adapters" 
        alembic
        celery_worker
        http_app
        gateways
        subgraph domains.books["Use Cases"]
            subgraph boundary["Domain Boundary (domains.books)"]
                BookRepositoryInterface
                Book
                BookService
                subgraph tasks["Domain logic"]
                    BookTask
                    subgraph entities["Books Entities"]
                        direction LR
                        BookModel
                        BookCreatedV1
                    end
                end
            end
        end
    end
    
    alembic ~~~ domains.books
    celery_worker ~~~ domains.books
    http_app ~~~ domains.books
    gateways ~~~ domains.books
    
    
    BookCreatedV1 ~~~ BookModel
    Book ~~~ tasks
    BookService ~~~ tasks
    BookRepositoryInterface ~~~ tasks
```

## Class dependency schema

A more detailed view showing the class dependencies and the absence of cyclical dependencies.

```mermaid
flowchart TD
    celery_worker
    http_app
    subgraph gateways
      SQLAlchemyRepository
      NullEventGateway
    end

    subgraph domains
      subgraph books
        subgraph domain_boundary
            BookService
        end
        subgraph domain_logic
            BookTask
        end
        subgraph dto
            Book
        end

        subgraph data_access_interfaces
          BookEventGatewayInterface
          BookRepositoryInterface
        end
        subgraph entities
          BookEvent
          BookModel
        end
      end
    end

    celery_worker-->domain_boundary
    celery_worker-->dto
    http_app-->domain_boundary
    http_app-->dto
    domain_boundary-->domain_logic
    domain_boundary-->dto
    domain_boundary-->data_access_interfaces
    domain_logic-->entities
    domain_logic-->dto
    domain_logic-->data_access_interfaces
    gateways-...->|Implement| data_access_interfaces
    data_access_interfaces-->entities
```
