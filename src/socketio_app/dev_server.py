import uvicorn

if __name__ == "__main__":
    uvicorn.run("socketio_app:create_app", factory=True, host="0.0.0.0", port=8000, reload=True)
