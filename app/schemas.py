from pydantic import BaseModel


class StatusIn(BaseModel):
    id_processo: str


class NLQ(BaseModel):
    question: str
