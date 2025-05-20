import pandas as pd
import numpy as np
from scipy.stats import chi2
import matplotlib.pyplot as plt

def cargar_csv(nombre):
    print(f"Cargando archivo: {nombre}")
    return pd.read_csv(nombre)
