from app import models, note, jobs
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from fastapi_offline import FastAPIOffline

models.Base.metadata.create_all(bind=engine)

app = FastAPIOffline()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(note.router, tags=['Notes'], prefix='/api/notes')
app.include_router(jobs.router, tags=['Jobs'], prefix='/api/jobs')


@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}
