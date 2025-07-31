from fastapi import FastAPI

from src.router import router

app = FastAPI(debug=True)

app.include_router(router)
