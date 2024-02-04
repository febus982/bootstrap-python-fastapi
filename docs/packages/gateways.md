# Gateways

The `gateways` package contains the implementations of the drivers
handling communication with external services (i.e. database repositories,
event producers, HTTP clients).

The `domains` package, has access to this package only using the
[Inversion of Control](../inversion-of-control.md).
