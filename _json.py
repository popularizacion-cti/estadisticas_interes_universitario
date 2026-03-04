import pandas as pd
import json
import os

from config import *
from procesamiento.sector import datos_sector

# ==============================
# CARGAR DATA
# ==============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_PARQUET = os.path.join(BASE_DIR, "data", "pf_postulantes.parquet")

df = pd.read_parquet(RUTA_PARQUET)

# ==============================
# ESTRUCTURA FINAL
# ==============================

estructura = {}

for clasificacion in ["Tradicional", "OCDE"]:
    estructura[clasificacion] = {}

    for nivel in orden_nivel:
        estructura[clasificacion][nivel] = {}

        datos = datos_sector(df, clasificacion, nivel, "Nacional")

        estructura[clasificacion][nivel]["Nacional"] = datos

# ==============================
# GUARDAR JSON
# ==============================

RUTA_JSON = os.path.join(BASE_DIR, "web", "data.json")

with open(RUTA_JSON, "w", encoding="utf-8") as f:
    json.dump(estructura, f, ensure_ascii=False)

print("JSON generado correctamente.")
