import streamlit as st
from src.load_file import cargar_csv, validar_dataframes
from src.statistics import calcular_estadisticas
from src.plots import generar_graficos, mostrar_resultados

def main():
    st.set_page_config(page_title="Evaluación ISO 17123-8")
    st.title("📡 Evaluación ISO 17123-8 para equipos GNSS")
    
    with st.sidebar:
        st.header("Parámetros de entrada")
        serie = st.text_input("Número de serie del equipo")
        nro_rovers = st.number_input("Cantidad de rovers", min_value=1, value=1)
        sigma_fab_xy = st.number_input("Precisión de fábrica horizontal (σ)", value=0.01)
        sigma_fab_z = st.number_input("Precisión de fábrica vertical (σ)", value=0.015)
        
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
            st.subheader("📈 Distribución de mediciones")
            generar_graficos(df1, df2)

if __name__ == "__main__":
    main()