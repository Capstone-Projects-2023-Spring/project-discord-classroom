import datetime
from typing import List, Any
from pydantic import BaseModel


class Quiz(BaseModel):
    title: str
    points: float
    start: str
    due: str
    time: int
    questions: str
    sections: List[str]


class Question(BaseModel):
    question: str
    answer: str
    wrong: List[str]
    points: float
