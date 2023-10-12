from fastapi import FastAPI
from src.routes import courses, login_signup, mentors, students
from src.helpers.setup_logger import initialize_logger


initialize_logger()

app = FastAPI()
app.include_router(courses.router)
app.include_router(login_signup.router)
app.include_router(mentors.router)
app.include_router(students.router)
