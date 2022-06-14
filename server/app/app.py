from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api import api_router
from .db import test_db

app = FastAPI()


@app.on_event("startup")
async def startup():
    test_db()


app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True
)
app.include_router(api_router, prefix="/api")
