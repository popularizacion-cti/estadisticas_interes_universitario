import os
import pandas as pd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUTA_PARQUET = os.path.join(BASE_DIR, "df_postulantes.parquet")

@st.cache_data
def cargar_datos():
    df = pd.read_parquet(RUTA_PARQUET)
    return df
