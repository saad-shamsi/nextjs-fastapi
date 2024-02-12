from fastapi import FastAPI, HTTPException, Depends
from models import Todo, UpdateTodo
from typing import Annotated, List
from sqlmodel import Session, select
from database import create_tables, create_session
from database import app


@app.on_event("startup")
async def on_startup():
    create_tables()


@app.get("/todo/{todo_id}")
def get_todo_by_id(todo_id: int, session: Annotated[Session, Depends(create_session)]):

    todo = session.get(Todo, todo_id)
    if todo:
        return todo
    else:
        raise HTTPException(
            status_code=404, detail="404 bad request todo does not exists")


@app.get("/todos", response_model=List[Todo])
def read_todos(session: Annotated[Session, Depends(create_session)]):
    todos = session.exec(select(Todo)).all()
    return todos


@app.post("/todo", response_model=Todo)
def create_todo(todo: Todo, session: Annotated[Session, Depends(create_session)]):

    todo_to_insert = Todo.model_validate(todo)
    session.add(todo_to_insert)
    session.commit()
    session.refresh(todo_to_insert)
    return todo_to_insert


@app.patch("/todo/{todo_id}", response_model=UpdateTodo)
def update_todo(todo_id: int, todo: UpdateTodo, session: Annotated[Session, Depends(create_session)]):
    todo_to_update = session.get(Todo, todo_id)
    if not todo_to_update:
        raise HTTPException(
            status_code=404, detail="bad request no todo found!")

    todo_to_update = todo.model_dump(exclude_unset=True)
    for key, value in todo_to_update.items():
        setattr(todo_to_update, key, value)
    session.add(todo_to_update)
    session.commit()
    session.refresh(todo_to_update)
    return todo_to_update


@app.delete("/todo/{todo_id}")
def delete_todo(todo_id: int, session: Annotated[Session, Depends(create_session)]):
    todo = session.get(Todo, todo_id)
    if todo:
        session.delete(todo)
        session.commit()

        return {"message": "Your todo has been successfully deleted"}
    else:
        raise HTTPException(
            status_code=404, detail="bad request no todo found!")
