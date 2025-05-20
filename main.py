import streamlit as st 
import pandas as pd
import numpy as np
from scipy.stats import chi2
import matplotlib.pyplot as plt
import os

from src.statics import calcular_residuos, calcular_std_por_dimension, calcular_umbral_iso

# Configuración de la página
st.set_page_config(page_title="Reporte Operatividad", page_icon="🛠️", layout="wide")
st.title("Reporte de Operatividad - Mettatec")

#======================================================================================
def main():
    st.subheader("Evaluación ISO 17123-8")
    #Serie del equipo
    serie=st.number_input("Ingrese número de serie del equipo:") 
    nro_rovers = st.number_input("Ingrese la cantidad de rovers: ")

    point01 = st.file_uploader("Ingrese el archivo .csv del Punto 1")
    df1 = pd.read_csv(point01)
    st.write(df1)

    point02 = st.file_uploader("Ingrese el archivo .csv del Punto 2")
    df2 = pd.read_csv(point02)
    st.write(df2)

    sigma_fab_xy = st.number_input("Precisión de fábrica horizontal (σ): ")
    sigma_fab_z = st.number_input("Precisión de fábrica vertical (σ): ")

    n_series = df1['description'].nunique()
    n_obs_por_serie = df1['description'].value_counts().iloc[0]
    gl = (n_series * n_obs_por_serie - 1) * nro_rovers
    print(f"Grados de libertad: {gl}")

    sum_RE2 = calcular_residuos(df1, 'easting') + calcular_residuos(df2, 'easting')
    sum_RN2 = calcular_residuos(df1, 'northing') + calcular_residuos(df2, 'northing')
    sum_Rh2 = calcular_residuos(df1, 'altitude') + calcular_residuos(df2, 'altitude')

    sx = calcular_std_por_dimension(sum_RE2, gl)
    sy = calcular_std_por_dimension(sum_RN2, gl)
    sh = calcular_std_por_dimension(sum_Rh2, gl)

    s_xy = np.sqrt(sx**2 + sy**2)
    s_xy += 0.003
    sh += 0.003

    umbral_xy = calcular_umbral_iso(sigma_fab_xy, gl)
    umbral_z = calcular_umbral_iso(sigma_fab_z, gl)

    aprobado = s_xy <= umbral_xy and sh <= umbral_z

#=========================================================================
    st.subheader(("=== Evaluación ISO 17123-8 - Cálculo Manual ==="))
    st.write(f"Desviación estándar s_x  = {sx:.5f} m")
    st.write(f"Desviación estándar s_y  = {sy:.5f} m")
    st.write(f"Desviación estándar s_z  = {sh - 0.003:.5f} m (sin corrección)")
    st.write(f"Desviación estándar s_xy = {s_xy - 0.003:.5f} m (sin corrección)")
    st.write(f"s_xy + corrección        = {s_xy:.5f} m")
    st.write(f"s_z  + corrección        = {sh:.5f} m")

    st.write(f"Umbral ISO XY: {umbral_xy:.5f} m")
    st.write(f"Umbral ISO Z : {umbral_z:.5f} m")

    st.subheader("\n--- EVALUACIÓN ---")
    if aprobado:
        st.write("El equipo APRUEBA la certificación ISO 17123-8.")
    else:
        st.write("El equipo NO aprueba la certificación:")
        if s_xy > umbral_xy:
            st.write(" s_xy excede el umbral permitido.")
        if sh > umbral_z:
            st.write("s_z excede el umbral permitido.")

#===================================================================================
if __name__ == "__main__":
    main()
