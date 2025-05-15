from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .app.models import base
from .app.api import auth, question, exam

base.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(question.router)
app.include_router(exam.router)


@app.get("/")
def read_root():
    return {"message": "AI Education Platform"}
