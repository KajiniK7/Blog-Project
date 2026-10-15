import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main_app:asgi_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
