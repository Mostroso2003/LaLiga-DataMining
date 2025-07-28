# train.py con Optimización de Hiperparámetros
import pandas as pd

import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.utils.class_weight import compute_sample_weight
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import json
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


print("Iniciando la OPTIMIZACIÓN DE HIPERPARÁMETROS con RandomizedSearchCV...")
print("Este proceso puede tardar varios minutos...")


# Cargar datos
df = pd.read_csv('datos_liga_procesados.csv')
X = df.drop(columns=['Resultado'])
y_categorical = df['Resultado']

# Codificar etiquetas
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y_categorical)


# Calcular pesos de las clases
sample_weights = compute_sample_weight(class_weight='balanced', y=y_encoded)

# Separar train/test para entrenamiento real
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)




# Definir el modelo base para XGBoost
model = xgb.XGBClassifier(
    objective='multi:softprob',
    eval_metric='mlogloss',
    use_label_encoder=False,
    random_state=42
)

# Definir el espacio de búsqueda de hiperparámetros
params = {
    'max_depth': [3, 4, 5, 6],
    'learning_rate': [0.01, 0.05, 0.1, 0.2],
    'n_estimators': [100, 200, 300],
    'subsample': [0.7, 0.8, 0.9, 1.0],
    'colsample_bytree': [0.7, 0.8, 0.9, 1.0],
}

# Configurar la búsqueda aleatoria
# n_iter: número de combinaciones a probar
# cv: número de validaciones cruzadas
# scoring: métrica a optimizar (f1_macro es ideal para desbalance)
random_search = RandomizedSearchCV(
    model,
    param_distributions=params,
    n_iter=50, # Puedes aumentar este número para una búsqueda más exhaustiva (tardará más)
    scoring='f1_macro',
    n_jobs=-1, # Usa todos los procesadores
    cv=3,
    random_state=42
)



# Ejecutar la búsqueda SOLO con train
random_search.fit(X_train, y_train, sample_weight=sample_weights[:len(y_train)])


# Imprimir los mejores resultados
print("\nBúsqueda finalizada.")
print(f"Mejor F1-Score (macro avg) encontrado: {random_search.best_score_:.4f}")
print("Mejores hiperparámetros encontrados:")
print(random_search.best_params_)




# Guardar el mejor modelo encontrado (XGBoost)
best_model = random_search.best_estimator_

# Entrenar y guardar RandomForest SOLO con train
rf = RandomForestClassifier(class_weight='balanced', random_state=42)
rf.fit(X_train, y_train)

print("\nModelos entrenados exitosamente.")
os.makedirs('artifacts', exist_ok=True)
joblib.dump(best_model, 'artifacts/xgboost_model.joblib')
joblib.dump(rf, 'artifacts/random_forest_model.joblib')
joblib.dump(encoder, 'artifacts/label_encoder.joblib')
print("Modelos guardados en la carpeta /artifacts.")