# train.py (Versión Final: Optimización y Competición de Máximo Rendimiento)
import pandas as pd
import numpy as np
import joblib
import json
import os
import warnings

# Algoritmos y herramientas
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.utils.class_weight import compute_sample_weight

warnings.filterwarnings("ignore", category=UserWarning)

print("Iniciando proceso de OPTIMIZACIÓN Y SELECCIÓN del mejor modelo...")
print("ADVERTENCIA: Este proceso puede tardar varios minutos...")

# 1. Cargar y Preparar los Datos
df = pd.read_csv('datos_liga_procesados.csv')
X = df.drop(columns=['Resultado'])
y_categorical = df['Resultado']

X_train, X_test, y_train_cat, y_test_cat = train_test_split(
    X, y_categorical, test_size=0.2, random_state=42, shuffle=False
)

encoder = LabelEncoder()
y_train = encoder.fit_transform(y_train_cat)
y_test = encoder.transform(y_test_cat)

scaler = StandardScaler()
numeric_cols = X_train.select_dtypes(include=np.number).columns
X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])

# 2. Definir Modelos y Espacios de Búsqueda
models_to_tune = [
    {
        "name": "RandomForest",
        "estimator": RandomForestClassifier(random_state=42, n_jobs=-1),
        "params": {
            'n_estimators': [100, 200, 300],
            'max_depth': [5, 10, 15],
            'min_samples_leaf': [2, 4, 6],
            'class_weight': ['balanced']
        }
    },
    {
        "name": "XGBoost",
        "estimator": xgb.XGBClassifier(objective='multi:softprob', eval_metric='mlogloss', use_label_encoder=False, random_state=42),
        "params": {
            'max_depth': [3, 4, 5, 6],
            'learning_rate': [0.01, 0.05, 0.1, 0.2],
            'n_estimators': [100, 200, 300],
            'subsample': [0.7, 0.8, 0.9, 1.0],
            'colsample_bytree': [0.7, 0.8, 0.9, 1.0]
        }
    }
]

best_score = 0
best_model_name = ""
best_model = None

# 3. Optimizar, Entrenar y Comparar
for model_config in models_to_tune:
    print(f"\n--- Optimizando: {model_config['name']} ---")
    
    random_search = RandomizedSearchCV(
        estimator=model_config['estimator'],
        param_distributions=model_config['params'],
        # --- CAMBIOS CLAVE ---
        n_iter=50,             # Volvemos a la búsqueda exhaustiva
        scoring='f1_macro',    # Volvemos a la métrica ideal para desbalance
        # ---------------------
        n_jobs=-1,
        cv=3,
        random_state=42
    )

    if model_config['name'] == "XGBoost":
        sample_weights = compute_sample_weight(class_weight='balanced', y=y_train)
        random_search.fit(X_train, y_train, sample_weight=sample_weights)
    else:
        random_search.fit(X_train, y_train)
        
    print(f"Mejor F1-Score (macro) encontrado para {model_config['name']}: {random_search.best_score_:.4f}")
    
    # Evaluar el mejor modelo de la búsqueda en el set de prueba
    best_estimator_from_search = random_search.best_estimator_
    y_pred = best_estimator_from_search.predict(X_test)
    current_accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Accuracy en el set de prueba para {model_config['name']}: {current_accuracy:.2%}")

    if current_accuracy > best_score:
        best_score = current_accuracy
        best_model_name = model_config['name']
        best_model = best_estimator_from_search

# 4. Guardar el Mejor Modelo
print("\n--- Proceso de selección finalizado ---")
print(f"🏆 El mejor modelo es: {best_model_name} con un Accuracy en el set de prueba de {best_score:.2%}")

os.makedirs('artifacts', exist_ok=True)
joblib.dump(best_model, 'artifacts/best_model.joblib')
joblib.dump(scaler, 'artifacts/scaler.joblib')
joblib.dump(encoder, 'artifacts/label_encoder.joblib')
with open('artifacts/model_columns.json', 'w') as f:
    json.dump(X_train.columns.tolist(), f)

print("✅ Artefactos del mejor modelo guardados en la carpeta /artifacts.")