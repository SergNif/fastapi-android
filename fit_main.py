import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        # "app:app",
        "app_fit_db:app",
        host='0.0.0.0',
        port=8085,
        reload=True
    )