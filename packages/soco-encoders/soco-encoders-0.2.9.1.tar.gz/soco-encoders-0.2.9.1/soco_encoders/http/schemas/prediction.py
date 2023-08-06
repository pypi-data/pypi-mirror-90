from pydantic import BaseModel
from typing import Any

class PredictionResult(BaseModel):
    took: int
    result: Any
