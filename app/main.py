from fastapi import FastAPI
from app.api import oauth

app = FastAPI()

app.include_router(oauth.router)