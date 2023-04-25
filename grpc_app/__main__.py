if __name__ == "__main__":  # pragma: no cover
    from asyncio import get_event_loop

    from grpc_app import main

    loop = get_event_loop()
    if loop.is_running():
        loop.create_task(main())
    else:
        loop.run_until_complete(main())
