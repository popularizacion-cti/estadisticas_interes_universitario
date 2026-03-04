import pandas as pd
import json

df = pd.read_parquet("pf_postulantes.parquet")

# mismos filtros y agrupaciones que hacías
df_grafica = (
    df.groupby(["Fecha_postulacion", "Sector_postulacion"])
      .size()
      .reset_index(name="Cantidad")
)

df_grafica["Porcentaje"] = (
    df_grafica
    .groupby("Fecha_postulacion")["Cantidad"]
    .transform(lambda x: 100 * x / x.sum())
    .round(1)
)

df_grafica.to_json("data.json", orient="records")
