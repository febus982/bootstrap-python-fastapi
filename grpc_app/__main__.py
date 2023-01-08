import logging
import time

from grpc_app import create_server

# TODO: Double-check this if statement, without it check pytest hangs.
if __name__ == "__main__":  # pragma: no cover
    _ONE_DAY_IN_SECONDS = 60 * 60 * 24

    server = create_server()
    server.start()
    logging.info("GRPC started")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        logging.debug("GRPC stop")
        server.stop(0)
