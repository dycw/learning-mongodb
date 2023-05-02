from fastapi import FastAPI
from project import routes
from dotenv import dotenv_values
from loguru import logger
from pymongo import MongoClient


config = dotenv_values(".env")


app = FastAPI()


@app.on_event("startup")
async def startup_db_client() -> None:
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    logger.info("Connected to the MongoDB database!")


@app.on_event("shutdown")
async def root() -> None:
    app.mongodb_client.close()


app.include_router(routes.router)
