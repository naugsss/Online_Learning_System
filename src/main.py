import os
import sys

sys.path.append(os.path.dirname(__file__))
import logging
from fastapi import FastAPI
from routes import courses, login_signup, mentors, students

logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)


app = FastAPI()
app.include_router(courses.router)
app.include_router(login_signup.router)
app.include_router(mentors.router)
app.include_router(students.router)
