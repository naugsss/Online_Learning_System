from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import courses, login_signup, mentors, students
from src.helpers.setup_logger import initialize_logger


initialize_logger()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    expose_headers=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(courses.router)
app.include_router(login_signup.router)
app.include_router(mentors.router)
app.include_router(students.router)
