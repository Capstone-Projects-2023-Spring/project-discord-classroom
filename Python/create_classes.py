from typing import List, Any
from pydantic import BaseModel


class Quiz(BaseModel):
    title: str
    points: float
    start: str
    due: str
    time: int
    questions: str
    classroom: str
    channel: str


class Question(BaseModel):
    question: str
    answer: str
    wrong: List[str]
    points: float


class Discussion(BaseModel):
    title: str
    start: str
    due: str
    points: int
    channel: str

class Assignment(BaseModel):
    title: str
    start: str
    due: str
    points: int
    classroom: str
    channel: str


class Grade(BaseModel):
    graderId: int
    taskId: int
    studentId: int
    score: int