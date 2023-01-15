from grpc import Server


def test_factory_returns_server(testserver: Server):
    assert isinstance(testserver, Server)
