from typing import List, Union, Dict
from pydantic import BaseModel


class Payload(BaseModel):
    model_id: str
    text: Union[str, List[str]]
    batch_size: int=10
    mode: str = 'default'
    kwargs: Dict = None
