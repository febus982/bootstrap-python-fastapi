import logging

import socketio

from common.telemetry import trace_function


class ChatNamespace(socketio.AsyncNamespace):
    def on_connect(self, sid, environ):
        pass

    def on_disconnect(self, sid, reason):
        pass

    @trace_function()
    async def on_echo_message(self, sid, data):
        # Note: this log line is only used to verify opentelemetry instrumentation works
        logging.info("received message")
        await self.emit("echo_response", data)
