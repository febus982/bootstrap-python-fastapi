from grpc.aio import Server


async def test_factory_returns_server(testserver: Server):
    assert isinstance(testserver, Server)
