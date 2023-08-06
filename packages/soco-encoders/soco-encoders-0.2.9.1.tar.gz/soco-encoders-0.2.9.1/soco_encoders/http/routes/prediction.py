from fastapi import APIRouter
from starlette.requests import Request
from soco_encoders.http.schemas.payload import Payload
from soco_encoders.http.schemas.prediction import PredictionResult
from soco_encoders.http.services.model import MyModel
from time import time
router = APIRouter()


@router.post("/encode", response_model=PredictionResult, name="predict")
def predict(request: Request, body: Payload) -> PredictionResult:

    model: MyModel = request.app.state.model
    s_time = time()
    prediction = model.predict(body.model_id, body.text, body.batch_size,
                               body.mode, body.kwargs)
    return PredictionResult(result=prediction, took=time()-s_time)
