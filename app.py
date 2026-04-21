from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import pickle
import numpy as np
import pandas as pd
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "model/model.pkl")
preprocess_path = os.path.join(BASE_DIR, "model/preprocessing.pkl")
data_path = os.path.join(BASE_DIR, "diabetes.csv")

# Load model & preprocessing
model = pickle.load(open(model_path, "rb"))
means = pickle.load(open(preprocess_path, "rb"))

# Templates & static
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


class PatientData(BaseModel):
    pregnancies: float
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    bmi: float
    dpf: float
    age: float


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
async def predict(data: PatientData):

    features_list = [
        data.pregnancies,
        data.glucose,
        data.blood_pressure,
        data.skin_thickness,
        data.insulin,
        data.bmi,
        data.dpf,
        data.age
    ]

    cols = ["pregnancies","glucose","blood_pressure","skin_thickness","insulin","bmi","dpf","age"]

    # Replace 0 with mean
    for i, col in enumerate(cols):
        if features_list[i] == 0 and col in means:
            features_list[i] = means[col]

    features = np.array([features_list])

    prediction = model.predict(features)[0]
    prob = model.predict_proba(features)[0][1]

    return {
        "prediction": int(prediction),
        "result": "Diabetic" if prediction == 1 else "Not Diabetic",
        "confidence": float(prob)
    }


@app.get("/analytics")
def analytics():
    df = pd.read_csv(data_path)

    return {
        "diabetic": int(df["Outcome"].sum()),
        "non_diabetic": int(len(df) - df["Outcome"].sum()),
        "avg_glucose": float(df["Glucose"].mean()),
        "avg_bmi": float(df["BMI"].mean())
    }