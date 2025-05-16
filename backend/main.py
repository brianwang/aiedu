import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
# print(sys.path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from app.models.base import Base
from app.api import auth, question, exam

Base.metadata.create_all(bind=engine)

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


# app.run()
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
