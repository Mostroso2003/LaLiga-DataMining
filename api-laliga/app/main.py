# app/main.py
import pandas as pd
import joblib
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import PredictionRequest, PredictionResponse
import os
from dotenv import load_dotenv

load_dotenv() # Carga las variables del archivo .env

# Inicializar la app de FastAPI
app = FastAPI(title="LaLiga Prediction API")

# Lee las URLs permitidas desde la variable de entorno
origins = os.getenv("CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Usa la lista de orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar los artefactos del modelo al iniciar la API
model = joblib.load('artifacts/best_model.joblib')
scaler = joblib.load('artifacts/scaler.joblib')
encoder = joblib.load('artifacts/label_encoder.joblib') # <-- AÑADIR ESTA LÍNEA
with open('artifacts/model_columns.json', 'r') as f:
    model_columns = json.load(f)

@app.get("/")
def read_root():
    """Endpoint raíz para verificar que la API está funcionando."""
    return {"status": "ok", "message": "LaLiga Prediction API is running!"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    """
    Endpoint para recibir datos de un partido y devolver una predicción.
    """
    # 1. Crear un DataFrame vacío con las columnas del modelo
    input_df = pd.DataFrame(columns=model_columns)
    input_df.loc[0] = 0 # Inicializamos la fila con ceros

    # 2. Establecer los valores recibidos en la solicitud
    home_team_col = f"HomeTeam_{request.home_team}"
    away_team_col = f"AwayTeam_{request.away_team}"

    # Se comprueba si la columna existe antes de asignarla para evitar errores
    if home_team_col in input_df.columns:
        input_df.loc[0, home_team_col] = 1
    if away_team_col in input_df.columns:
        input_df.loc[0, away_team_col] = 1

    # Asignar el resto de características
    input_df.loc[0, 'H_Forma_Goles_Anotados'] = request.h_form_goals
    input_df.loc[0, 'A_Forma_Goles_Anotados'] = request.a_form_goals
    input_df.loc[0, 'HST'] = request.h_shots_on_target
    input_df.loc[0, 'AST'] = request.a_shots_on_target
    
    # 3. Normalizar los datos numéricos
    numeric_cols = [col for col in scaler.get_feature_names_out() if col in input_df.columns]
    input_df[numeric_cols] = scaler.transform(input_df[numeric_cols])

    # 4. Realizar la predicción
    probabilities = model.predict_proba(input_df)[0]
    prediction_index = probabilities.argmax()
    
    # 5. Formatear la respuesta decodificando las etiquetas
    prediction_label = encoder.inverse_transform([prediction_index])[0]
    
    # Decodificar las clases para las claves del diccionario de probabilidades
    decoded_classes = encoder.inverse_transform(model.classes_)
    response_probs = {cls: float(prob) for cls, prob in zip(decoded_classes, probabilities)}

    return PredictionResponse(
        prediction=prediction_label,
        probabilities=response_probs
    )