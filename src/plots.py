import pandas as pd
import numpy as np
from scipy.stats import chi2
import matplotlib.pyplot as plt

def generar_graficos(df1, df2):
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
