import streamlit as st
from src.load_file import cargar_csv, validar_dataframes
from src.statistics import calcular_estadisticas
from src.plots import generar_graficos, mostrar_resultados
from PIL import Image
import os
#===============================================================

def main():
    st.set_page_config(page_title="Evaluación ISO 17123-8", layout= "centered")
    st.title("Evaluación ISO 17123-8 para equipos GNSS")
    
    with st.sidebar:
        st.header("Parámetros de entrada")
        serie = st.text_input("Número de serie del equipo", placeholder="PEX5-...")
        nro_rovers = st.number_input("Cantidad de rovers", min_value=1)
        sigma_fab_xy = st.number_input("Precisión de fábrica horizontal", value=0.007,
                              step=0.001,
                              format="%.3f")
        sigma_fab_z = st.number_input("Precisión de fábrica vertical", value=0.012,
                              step=0.001,
                              format="%.3f")
        
        st.header("Carga de archivos")
        archivo_pa01 = st.file_uploader("Archivo CSV de PA01", type="csv")
        archivo_pa02 = st.file_uploader("Archivo CSV de PA02", type="csv")
    
    if archivo_pa01 and archivo_pa02:
        df1 = cargar_csv(archivo_pa01)
        df2 = cargar_csv(archivo_pa02)
        
        if validar_dataframes(df1, df2):
            resultados = calcular_estadisticas(df1, df2, sigma_fab_xy, sigma_fab_z, nro_rovers)
            
            st.divider()
            mostrar_resultados(resultados, serie)
            
            st.divider()
            generar_graficos(df1,df2)

if __name__ == "__main__":
    main()

#===============================================================
# Insert logos

col1, col2 = st.columns(2,vertical_alignment="bottom" )

with col1:
    imagen_izq = Image.open("files/metta_logo_hd.png") 
    st.logo(
    imagen_izq, size="large")
        
with col2:
    imagen_der = Image.open("files/Shabby stamp(bonus).png")
    st.image(imagen_der,
            width=170)

