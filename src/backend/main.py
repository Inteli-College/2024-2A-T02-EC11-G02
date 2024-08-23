from fastapi import FastAPI
from .routers import pullArrayBytes, modelVersion, S3Router

app = FastAPI()

app.include_router(pullArrayBytes.router)
app.include_router(modelVersion.router)
app.include_router(S3Router.router)