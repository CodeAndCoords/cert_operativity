import numpy as np
from scipy.stats import chi2


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
