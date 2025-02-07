import socketio


class ChatNamespace(socketio.AsyncNamespace):
    def on_connect(self, sid, environ):
        pass

    def on_disconnect(self, sid, reason):
        pass

    async def on_echo_message(self, sid, data):
        await self.emit("echo_response", data)
