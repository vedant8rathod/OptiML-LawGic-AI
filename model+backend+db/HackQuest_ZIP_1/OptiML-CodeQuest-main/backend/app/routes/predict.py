from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.model_loader import predict

router = APIRouter(prefix="/api/predict", tags=["Prediction"])

class PredictRequest(BaseModel):
    text: str

@router.post("/")
def get_prediction(req: PredictRequest):
    return {"input": req.text, "prediction": predict(req.text)}
from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.model_loader import predict

router = APIRouter(prefix="/api/predict", tags=["Prediction"])

class PredictRequest(BaseModel):
    text: str

@router.post("/")
def get_prediction(req: PredictRequest):
    return {"input": req.text, "prediction": predict(req.text)}