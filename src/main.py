import os
import sys

from helpers.setup_logger import initialize_logger

sys.path.append(os.path.dirname(__file__))
from fastapi import FastAPI
from routes import courses, login_signup, mentors, students

initialize_logger()

app = FastAPI()
app.include_router(courses.router)
app.include_router(login_signup.router)
app.include_router(mentors.router)
app.include_router(students.router)
