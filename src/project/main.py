from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to the PyMongo tutorial!"}