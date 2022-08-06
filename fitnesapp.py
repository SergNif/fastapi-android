from unittest import result
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fitmodels import Fitness
from fitdatabase import engine
from sqlmodel import Session, select
from typing import Optional, List

app = FastAPI()

session = Session(bind=engine)


@app.get('/fits', response_model=List[Fitness],
         status_code=status.HTTP_200_OK)
async def get_all_fits():
    statement = select(Fitness)
    result = session.exec(statement).all()

    return result


@app.post('/fits', response_model=Fitness, status_code=status.HTTP_201_CREATED)
async def create_a_fit(fit: Fitness):
    new_fit = Fitness(title=fit.title, description=fit.description)
    session.add(new_fit)
    session.commit()
    return new_fit


@app.get('/fits/{fit_id}', response_model=Fitness)
async def get_all_fit(fit_id: int):
    statement = select(Fitness).where(Fitness.id == fit_id)
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return result


@app.put('/fit/{fit_id}', response_model=Fitness)
async def get_all_fits(fit_id: int, fit: Fitness):
    statement = select(Fitness).where(Fitness.id == fit_id)
    result = session.exec(statement).first()
    result.title = fit.title
    result.description = fit.description
    session.commit()
    return result


@app.delete('/fit/{fit_id}', status_code=status.HTTP_205_RESET_CONTENT)
async def delete_a_fit(fit_id:int):
    statement = select(Fitness).where(Fitness.id==fit_id)

    result = session.exec(statement).one_or_none()

    if result == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Resource Not Found")

    session.delete(result)

    return result

# @app.get('/books', response_model=List[Book],
#          status_code=status.HTTP_200_OK)
# async def get_all_books():
#     statement = select(Book)
#     result = session.exec(statement).all()

#     return result


# @app.post('/books', response_model=Book, status_code=status.HTTP_201_CREATED)
# async def create_a_book(book: Book):
#     new_book = Book(title=book.title, description=book.description)
#     session.add(new_book)
#     session.commit()
#     return new_book


# @app.get('/books/{book_id}', response_model=Book)
# async def get_all_book(book_id: int):
#     statement = select(Book).where(Book.id == book_id)
#     result = session.exec(statement).first()
#     if not result:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

#     return result


# @app.put('/book/{book_id}', response_model=Book)
# async def get_all_books(book_id: int, book: Book):
#     statement = select(Book).where(Book.id == book_id)
#     result = session.exec(statement).first()
#     result.title = book.title
#     result.description = book.description
#     session.commit()
#     return result


# @app.delete('/book/{book_id}', status_code=status.HTTP_205_RESET_CONTENT)
# async def delete_a_book(book_id:int):
#     statement = select(Book).where(Book.id==book_id)

#     result = session.exec(statement).one_or_none()

#     if result == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="Resource Not Found")

#     session.delete(result)

#     return result
