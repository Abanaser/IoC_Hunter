from fastapi import FastAPI
from engine.database_connector import dump_as_json

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/ioc/{collection}")
async def ioc(collection: str):
    return dump_as_json(collection)
