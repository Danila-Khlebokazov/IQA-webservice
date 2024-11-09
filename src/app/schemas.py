from pydantic import BaseModel

__all__ = ("ScoreOutSchema",)


class ScoreOutSchema(BaseModel):
    score: float
