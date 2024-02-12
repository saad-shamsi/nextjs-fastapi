from sqlmodel import Session, create_engine, SQLModel
from fastapi import FastAPI

connection_string = "postgresql://saadshamsi13:hrpGdD8As6IZ@ep-bitter-sunset-a1x6gnrg.ap-southeast-1.aws.neon.tech/todo?sslmode=require"

engine = create_engine(connection_string)


app = FastAPI()


def create_tables():
    SQLModel.metadata.create_all(engine)


def create_session():
    with Session(engine) as session:
        yield session
