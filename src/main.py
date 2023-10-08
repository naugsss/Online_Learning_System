import os
import sys

sys.path.append(os.path.dirname(__file__))
from fastapi import FastAPI
from routes import courses, login_signup, mentors, students

# from src.routes.login_signup import login

app = FastAPI()

# we are including the auth.py file as a route
app.include_router(courses.router)
app.include_router(login_signup.router)
app.include_router(mentors.router)
app.include_router(students.router)
