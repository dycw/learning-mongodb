from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_404_NOT_FOUND,
)

from project.models import Book, BookUpdate


router = APIRouter()


@router.post(
    "/",
    response_description="Create a new book",
    status_code=HTTP_201_CREATED,
    response_model=Book,
)
def create_book(*, request: Request, book: Book = Body(...)) -> Book:
    book = jsonable_encoder(book)
    new_book = request.app.database["books"].insert_one(book)
    return request.app.database["books"].find_one(
        {"_id": new_book.inserted_id}
    )


@router.get(
    "/", response_description="List all books", response_model=list[Book]
)
def list_lists(*, request: Request) -> list[Book]:
    return list(request.app.database["books"].find(limit=100))


@router.get(
    "/{id}",
    response_description="Get a single book by id",
    response_model=Book,
)
def find_book(id: str, request: Request) -> Book:
    if (
        book := request.app.database["books"].find_one({"_id": id})
    ) is not None:
        return book
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail=f"Book with ID {id} not found",
    )


@router.put("/{id}", response_description="Update a book", response_model=Book)
def update_book(
    *, id: str, request: Request, book: BookUpdate = Body(...)
) -> Book:
    kwargs = {k: v for k, v in book.dict().items() if v is not None}
    if len(kwargs) >= 1:
        result = request.app.database["books"].update_one(
            {"$_id": id}, {"$set": book}
        )
        if result.modified_count == 0:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f"Book with ID {id} not found",
            )
    if (
        existing_book := request.app.database["books"].find_one({"_id": id})
    ) is not None:
        return existing_book
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail=f"Book with ID {id} not found",
    )


@router.delete("/{id}", response_description="Delete a book")
def delete_book(id: str, request: Request, response: Response):
    result = request.app.database["books"].delete_one({"_id": id})
    if result.deleted_count == 1:
        response.status_code = HTTP_204_NO_CONTENT
        return response
    raise HTTPException(
        status_code=HTTP_404_NOT_FOUND,
        detail=f"Book with ID {id} not found",
    )
