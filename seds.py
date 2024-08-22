import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargar los datos
mag = pd.read_csv("./SEDS/merged_data.csv")

# Definir los nombres de las columnas y las constantes
bands_I = ['abs_1_mag_0_I', 'abs_2_mag_0_I', 'abs_3_mag_0_I', 'abs_4_mag_0_I']
bands_W = ['abs_1_mag_0_W', 'abs_2_mag_0_W', 'abs_3_mag_0_W', 'abs_4_mag_0_W']

Lambda = np.array([3.6, 4.5, 5.8, 8.0, 3.35, 4.6, 11.6, 21.1, 23.68])
Fzero = np.array([6.48148e-8, 2.66222e-8, 1.02556e-8, 3.00609e-9, 8.17870e-8, 2.41500e-8, 6.51510e-10, 5.09010e-11, 3.73438e-11])

print(mag["abs_4_mag_0_I"])
# Crear un diccionario para almacenar los flujos calculados
fluxes = {}
fluxes["OBJECT_ID"] = mag["OBJECT_ID"]

# Iterar sobre las bandas y calcular los flujos
for i, band in enumerate(bands_I):
    fluxes[f'flux_{band}'] = Fzero[i] * 10**((-0.4)*mag[band].to_numpy())

for i, band in enumerate(bands_W):
    fluxes[f'flux_{band}'] = Fzero[i + 4] * 10**((-0.4)*mag[band].to_numpy())

fluxes['flux_abs_1_mag_0'] = Fzero[8] * 10**((-0.4)*mag['abs_1_mag_0'].to_numpy())

# Convertir el diccionario a un DataFrame para facilitar la manipulación
flux_df = pd.DataFrame(fluxes)

# Crear gráficos para cada estrella
for index, row in flux_df.iterrows():
    plt.figure(figsize=(10, 6))
    
    # Obtener los flujos para la estrella actual
    flux_values = np.array([
        row[f'flux_{band}'] for band in bands_I + bands_W
    ])
    flux_values = np.append(flux_values, row['flux_abs_1_mag_0'])  # Añadir el flujo del último valor

    # Calcular flujo multiplicado por la longitud de onda
    flux_lambda = flux_values * Lambda

    print(flux_lambda)

    # Ordenar los datos por el eje x
    sorted_indices = np.argsort(Lambda)
    Lambda_sorted = np.array(Lambda)[sorted_indices]
    flux_lambda_sorted = np.array(flux_lambda)[sorted_indices]

    # Graficar
    plt.scatter(np.log(Lambda_sorted), np.log(flux_lambda_sorted), color='red')
    plt.plot(np.log(Lambda_sorted), np.log(flux_lambda_sorted), linestyle='-', linewidth=2)
    plt.title(f"Flujo vs Longitud de Onda para Estrella {row['OBJECT_ID']}")
    plt.xlabel("Log(Longitud de Onda) (µm)")
    plt.ylabel("Log(Flujo x Longitud de Onda) (erg/s/cm²/Hz µm)")
    plt.grid(True)
    plt.savefig(f'./SEDS/seds_{index}.png')
    plt.close()  # Cerrar la figura para liberar memoria