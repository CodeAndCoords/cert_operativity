import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

def generar_graficos(df1, df2):
    """Genera gráficos comparativos para los dos datasets"""
    fig, axs = plt.subplots(6, 1, figsize=(9, 15))
    datasets = [(df1, "PA01"), (df2, "PA02")]
    coords = ['easting', 'northing', 'altitude']
    titulos = ['Easting', 'Northing', 'Altitude']

    for row, (df, nombre) in enumerate(datasets):
        for i, coord in enumerate(coords):
            datos = df[coord]
            mu = np.mean(datos)
            std = np.std(datos, ddof=1)
            ax = axs[row * 3 + i]
            ax.hist(datos, bins=30, density=True, alpha=0.6, color='skyblue', label="Histograma")
            x = np.linspace(min(datos), max(datos), 200)
            p = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / std) ** 2)
            ax.plot(x, p, 'r', linewidth=2, label=f"Curva de Gauss (σ = {std:.4f} m)")
            ax.set_title(f"{nombre} - {titulos[i]}")
            ax.set_xlabel("Valor")
            ax.set_ylabel("Densidad")
            ax.legend()
            ax.grid(True, linestyle='--', linewidth=0.5)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def mostrar_resultados(resultados, serie):
    """Muestra los resultados de la evaluación en Streamlit"""
    st.subheader(f"📊 Resultados para equipo {serie}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Grados de libertad", resultados['gl'])
        st.metric("Desviación estándar s_xy", f"{resultados['s_xy']:.5f} m")
        st.metric("Desviación estándar s_z", f"{resultados['sh_corregido']:.5f} m")
    
    with col2:
        st.metric("Umbral ISO XY", f"{resultados['umbral_xy']:.5f} m")
        st.metric("Umbral ISO Z", f"{resultados['umbral_z']:.5f} m")
    
    if resultados['aprobado']:
        st.success("✅ El equipo APRUEBA la certificación ISO 17123-8.")
    else:
        st.error("❌ El equipo NO aprueba la certificación:")
        if resultados['s_xy'] > resultados['umbral_xy']:
            st.error("⚠️ Std_Horizontal ISO excede el umbral permitido.")
        if resultados['sh_corregido'] > resultados['umbral_z']:
            st.error("⚠️ Std_Vertical ISO excede el umbral permitido.")