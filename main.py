import pandas as pd
import numpy as np
from scipy.stats import chi2
import matplotlib.pyplot as plt
from fpdf import FPDF
import os

def cargar_csv(nombre):
    print(f"Cargando archivo: {nombre}")
    return pd.read_csv(nombre)

def calcular_residuos(data, coord):
    media = data[coord].mean()
    data[f"residuo_{coord}"] = media - data[coord]
    data[f"R_{coord[0].upper()}2"] = data[f"residuo_{coord}"] ** 2
    return data[f"R_{coord[0].upper()}2"].sum()

def calcular_std_por_dimension(sum_r2, gl):
    return np.sqrt(sum_r2 / gl)

def calcular_umbral_iso(sigma_fabrica, gl, confianza=0.95):
    chi_val = chi2.ppf(confianza, gl)
    return sigma_fabrica * np.sqrt(chi_val / gl)

def generar_graficos_pdf_una_pagina(df1, df2, nserie, s_xy, sh, umbral_xy, umbral_z, aprobado, output_pdf="comparativo_PA01_PA02.pdf"):
    fig, axs = plt.subplots(6, 1, figsize=(6, 12), constrained_layout=True)
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
            ax.set_title(f"{nombre} - {titulos[i]}", fontname='Times New Roman', fontsize=12)
            ax.set_xlabel("Valor", fontname='Times New Roman', fontsize=10)
            ax.set_ylabel("Densidad", fontname='Times New Roman', fontsize=10)
            ax.legend(loc='upper right', fontsize=8)
            ax.grid(True, linestyle='--', linewidth=0.5)

    img_path = "comparativo_graficos.png"
    fig.savefig(img_path, dpi=200)
    plt.close(fig)

    pdf = FPDF()
    pdf.add_page()
    pdf.rect(x=5, y=5, w=200, h=287)
    pdf.rect(x=4, y=4, w=202, h=289)
    pdf.set_x(15)
    pdf.set_font("Times", "B", 15)
    pdf.cell(0, 10, f"Analisis ISO 17123-8 Modelo GNSS: X5R/RT  Numero de serie: {nserie}", ln=True)
    pdf.set_font("Times", "", 12)
    pdf.ln(2)
    pdf.set_x(30)
    pdf.cell(0, 10, f"Std_Horizontal ISO       = {s_xy:.5f} m", ln=True)
    pdf.set_x(30)
    pdf.cell(0, 10, f"Std_Vertical ISO       = {sh:.5f} m", ln=True)
    pdf.set_x(30)
    pdf.cell(0, 10, f"Umbral ISO XY: {umbral_xy:.5f} m", ln=True)
    pdf.set_x(30)
    pdf.cell(0, 10, f"Umbral ISO Z : {umbral_z:.5f} m", ln=True)
    pdf.ln(3)
    pdf.set_x(15)
    pdf.set_font("Times", "B", 12)
    if aprobado:
        pdf.cell(0, 10, "El equipo APRUEBA la certificación ISO 17123-8.", ln=True)
    else:
        pdf.cell(0, 10, "El equipo NO aprueba la certificación:", ln=True)
        if s_xy > umbral_xy:
            pdf.cell(0, 10, "Std_Horizontal ISO excede el umbral permitido.", ln=True)
        if sh > umbral_z:
            pdf.cell(0, 10, "Std_Vertical ISO excede el umbral permitido.", ln=True)

    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)
    pdf.image(img_path, x=50, y=pdf.get_y(), w=100)
    pdf.image("metta_logo_hd.png", x=13, y=275, w=40)
    pdf.image("Shabby stamp(bonus).png", x=170, y=250, w=40)
    pdf.output(output_pdf)
    os.remove(img_path)
    print(f"📄 PDF generado sin solapamientos: {output_pdf}")

def main():
    print("=== Evaluación ISO 17123-8 - Cálculo Manual ===")
    #Serie del equipo
    serie=input("Ingrese numero de serie del equipo: ")    
    nro_rovers = int(input("Cantidad de rovers: "))
    path_pa01 = input("Ruta al archivo CSV de PA01: ").strip('"')
    path_pa02 = input("Ruta al archivo CSV de PA02: ").strip('"')
    sigma_fab_xy = float(input("Precisión de fábrica horizontal (σ): "))
    sigma_fab_z = float(input("Precisión de fábrica vertical (σ): "))

    df1 = cargar_csv(path_pa01)
    df2 = cargar_csv(path_pa02)

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

    generar_graficos_pdf_una_pagina(df1, df2, serie, s_xy, sh, umbral_xy, umbral_z, aprobado, output_pdf="PA01_PA02_comparativo.pdf")

    print("\n--- RESULTADOS ---")
    print(f"Desviación estándar s_x  = {sx:.5f} m")
    print(f"Desviación estándar s_y  = {sy:.5f} m")
    print(f"Desviación estándar s_z  = {sh - 0.003:.5f} m (sin corrección)")
    print(f"Desviación estándar s_xy = {s_xy - 0.003:.5f} m (sin corrección)")
    print(f"s_xy + corrección        = {s_xy:.5f} m")
    print(f"s_z  + corrección        = {sh:.5f} m")

    print(f"Umbral ISO XY: {umbral_xy:.5f} m")
    print(f"Umbral ISO Z : {umbral_z:.5f} m")

    print("\n--- EVALUACIÓN ---")
    if aprobado:
        print("El equipo APRUEBA la certificación ISO 17123-8.")
    else:
        print("El equipo NO aprueba la certificación:")
        if s_xy > umbral_xy:
            print("  ⚠️ s_xy excede el umbral permitido.")
        if sh > umbral_z:
            print("  ⚠️ s_z excede el umbral permitido.")

if __name__ == "__main__":
    main()
