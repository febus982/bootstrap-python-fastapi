# Books

The app should always import only classes available from
`app.domains.books` and _never_ import anything from the
nested modules (e.g. `app.domains.books.local`)

We will use an IoC container to do dependency injection
using the interface class. In this way we achieve:

* Interface segregation principle
* Dependency inversion principle

The only internal classes that can be imported directly
are the repository interfaces and the models. We'll need
them to implement the concrete classes to achieve the
same aforementioned principles.
