from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient


config = dotenv_values(".env")


app = FastAPI()


@app.on_event("startup")
def startup_db_client() -> None:
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAMe"]]


@app.on_event("shutdown")
async def root() -> None:
    app.mongodb_client.close()
