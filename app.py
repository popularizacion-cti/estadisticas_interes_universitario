import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# CONFIGURACIÓN GLOBAL
# ==============================

orden_sectores = [
    'Ingenierías y Ciencias Aplicadas',
    'Ciencias de la Salud',
    'Disciplinas Logísticas',
    'Ciencias Sociales y Humanidades',
    'Ciencias Puras',
    'Artes'
]

orden_sectores_ocde = [
    'Ciencias Naturales',
    'Ingeniería y Tecnología',
    'Ciencias Médicas y de la Salud',
    'Ciencias Agrícolas',
    'Ciencias Sociales',
    'Humanidades'
]

orden_edad = [
    '[<15]',
    '[16-17]',
    '[18-20]',
    '[21-25]',
    '[26<]'
]

orden_edad_genero = [
    '[<15]-Femenino',
    '[<15]-Masculino',
    '[16-17]-Femenino',
    '[16-17]-Masculino',
    '[18-20]-Femenino',
    '[18-20]-Masculino',
    '[21-25]-Femenino',
    '[21-25]-Masculino',
    '[26<]-Femenino',
    '[26<]-Masculino'
]

colores_sectores = {
    'Ingenierías y Ciencias Aplicadas': '#1f77b4',  # Azul
    'Ciencias de la Salud': '#ff7f0e',              # Naranja
    'Disciplinas Logísticas': '#2ca02c',            # Verde
    'Ciencias Sociales y Humanidades': '#d62728',   # Rojo
    'Ciencias Puras': '#9467bd',                    # Púrpura
    'Artes': '#8c564b'                              # Marrón oscuro
}

colores_sectores_ocde = {
    'Ciencias Naturales': '#4C78A8',             # Azul medio
    'Ingeniería y Tecnología': '#F58518',        # Naranja fuerte
    'Ciencias Médicas y de la Salud': '#54A24B', # Verde
    'Ciencias Agrícolas': '#B279A2',             # Lila
    'Ciencias Sociales': '#E45756',              # Rojo coral
    'Humanidades': '#9D755D'                     # Marrón suave
}

colores_genero = {
    'Femenino': '#2A9D8F',
    'Masculino': '#E9C46A',
}

st.set_page_config(layout="wide")

# ==============================
# CARGA DE DATOS
# ==============================

@st.cache_data
def cargar_datos():
    return pd.read_parquet("df_postulantes.parquet")

df = cargar_datos()

df["Sector_postulacion"] = pd.Categorical(
    df["Sector_postulacion"],
    categories=orden_sectores,
    ordered=True
)

df["Sectorocde_postulacion"] = pd.Categorical(
    df["Sectorocde_postulacion"],
    categories=orden_sectores_ocde,
    ordered=True
)

# ==============================
# GRÁFICA 1
# ==============================

st.header("Evolución porcentual por sector")

# Selector de región
regiones = sorted(df["Region_entidad"].dropna().unique().tolist())
regiones = ["Nacional"] + regiones

region = st.selectbox("Seleccione región", regiones)

df_filtrado = df.copy()

if region != "Nacional":
    df_filtrado = df_filtrado[df_filtrado["Region_entidad"] == region]

if df_filtrado.empty:
    st.warning("No hay datos para la región seleccionada.")
    st.stop()    

# Agrupar porcentaje
df_grafica = (
    df_filtrado
    .groupby("Fecha_postulacion")["Sector_postulacion"]
    .value_counts(normalize=True)
    .unstack(fill_value=0)
    .mul(100)
    .round(1)
    .reset_index()
)

# Agrupar cantidades
df_counts = (
    df_filtrado
    .groupby("Fecha_postulacion")["Sector_postulacion"]
    .value_counts()
    .unstack(fill_value=0)
    .reset_index()
)

# Formato largo
df_melted = df_grafica.melt(
    id_vars="Fecha_postulacion",
    var_name="Sector_postulacion",
    value_name="Porcentaje"
)

df_counts_melted = df_counts.melt(
    id_vars="Fecha_postulacion",
    var_name="Sector_postulacion",
    value_name="Cantidad"
)

df_melted = df_melted.merge(
    df_counts_melted,
    on=["Fecha_postulacion", "Sector_postulacion"],
    how="left"
)

df_melted = df_melted.sort_values("Fecha_postulacion")
df_melted["Fecha_postulacion"] = df_melted["Fecha_postulacion"].astype(str)

# Título dinámico
if region == "Nacional":
    titulo = "Porcentaje de postulantes por sector"
else:
    titulo = f"Porcentaje de postulantes por sector - {region}"

# Crear figura
    
fig = px.line(
    df_melted,
    x="Fecha_postulacion",
    y="Porcentaje",
    color="Sector_postulacion",
    markers=True,
    title=titulo,
    color_discrete_map=colores_sectores,
    category_orders={
        "Sector_postulacion": orden_sectores,
        "Fecha_postulacion": sorted(df_melted["Fecha_postulacion"].unique())
    },
    labels={
        "Fecha_postulacion": "Año",
        "Porcentaje": "Porcentaje %",
        "Sector_postulacion": "Sector"
    },
    hover_data={"Porcentaje": ":.1f", "Cantidad": True}
)

fig.update_layout(
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor="black",
        tickmode="linear"
    ),
    yaxis=dict(
        showline=True,
        linewidth=1,
        linecolor="black"
    ),
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Arial", size=12),
    title_font=dict(size=20)
)

st.plotly_chart(fig, use_container_width=True)
