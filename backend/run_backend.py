if __name__ == "__main__":
    from backend.main import app

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)