import pandas as pd
from config import *


def datos_sector(df, clasificacion, nivel, region):

    # ==============================
    # FILTROS
    # ==============================

    df_filtrado = df.copy()

    if region != "Nacional":
        df_filtrado = df_filtrado[df_filtrado["Region_entidad"] == region]

    df_filtrado = df_filtrado[df_filtrado["Nivel_postulacion"] == nivel]

    if df_filtrado.empty:
        return []

    # ==============================
    # SELECCIÓN DE CLASIFICACIÓN
    # ==============================

    if clasificacion == "Tradicional":
        columna_sector = "Sector_postulacion"
        orden = orden_sectores
    else:
        columna_sector = "Sectorocde_postulacion"
        orden = orden_sectores_ocde

    # ==============================
    # AGRUPACIONES
    # ==============================

    df_grafica = (
        df_filtrado
        .groupby("Fecha_postulacion")[columna_sector]
        .value_counts(normalize=True)
        .unstack(fill_value=0)
        .mul(100)
        .round(1)
        .reset_index()
    )

    df_counts = (
        df_filtrado
        .groupby("Fecha_postulacion")[columna_sector]
        .value_counts()
        .unstack(fill_value=0)
        .reset_index()
    )

    df_melted = df_grafica.melt(
        id_vars="Fecha_postulacion",
        var_name="Sector",
        value_name="Porcentaje"
    )

    df_counts_melted = df_counts.melt(
        id_vars="Fecha_postulacion",
        var_name="Sector",
        value_name="Cantidad"
    )

    df_melted = df_melted.merge(
        df_counts_melted,
        on=["Fecha_postulacion", "Sector"],
        how="left"
    )

    df_melted = df_melted.sort_values("Fecha_postulacion")

    return df_melted.to_dict(orient="records")
