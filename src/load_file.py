import pandas as pd
import streamlit as st

def cargar_csv(nombre_archivo):
    """Carga un archivo CSV y muestra información básica"""
    try:
        df = pd.read_csv(nombre_archivo)
        st.success(f"Archivo {nombre_archivo.name} cargado correctamente")
        st.write(f"Registros cargados: {len(df)}")
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {str(e)}")
        return None

def validar_dataframes(df1, df2):
    """Valida que los dataframes tengan la estructura esperada"""
    columnas_requeridas = ['easting', 'northing', 'altitude', 'description']
    
    if df1 is None or df2 is None:
        return False
    
    for df in [df1, df2]:
        if not all(col in df.columns for col in columnas_requeridas):
            st.error("Los archivos deben contener las columnas: easting, northing, altitude y description")
            return False
    
    return True