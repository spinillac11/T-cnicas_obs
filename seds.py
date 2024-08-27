import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargar los datos
mag = pd.read_csv("./SEDS/merged_data.csv")

# Definir los nombres de las columnas y las constantes
bands_I = ['abs_1_mag_0_I', 'abs_2_mag_0_I', 'abs_3_mag_0_I', 'abs_4_mag_0_I']
bands_W = ['abs_1_mag_0_W', 'abs_3_mag_0_W', 'abs_4_mag_0_W']

bands_I_err = ['abs_1_mag_err_0_I', 'abs_2_mag_err_0_I', 'abs_3_mag_err_0_I', 'abs_4_mag_err_0_I']
bands_W_err = ['abs_1_mag_err_0_W', 'abs_3_mag_err_0_W', 'abs_4_mag_err_0_W']

Lambda = np.array([3.6, 4.5, 5.8, 8.0, 3.35, 11.6, 21.1, 23.68])
###                   I1         I2           I3          I4          W1            W3         W4           M1           J         H        K
Fzero = np.array([6.48148e-8, 2.66222e-8, 1.02556e-8, 3.00609e-9, 8.17870e-8, 6.51510e-10, 5.09010e-11, 3.73438e-11, 3.129e-6, 1.133e-6, 4.283e-7])

# Iterar sobre las bandas y calcular los flujos
for i, band in enumerate(bands_I):
    mag[f'flux_{band}'] = Fzero[i] * 10**((-0.4)*mag[band].to_numpy())
    mag[f'flux_{bands_I_err[i]}'] = Fzero[i] * (0.4*np.log(10)) * 10**((-0.4)*mag[band].to_numpy()) * mag[bands_I_err[i]].to_numpy()

for i, band in enumerate(bands_W):
    mag[f'flux_{band}'] = Fzero[i + 4] * 10**((-0.4)*mag[band].to_numpy())
    mag[f'flux_{bands_W_err[i]}'] = Fzero[i + 4] * (0.4*np.log(10)) * 10**((-0.4)*mag[band].to_numpy()) * mag[bands_W_err[i]].to_numpy()

mag['flux_abs_1_mag_0'] = Fzero[7] * 10**((-0.4)*mag['abs_1_mag_0'].to_numpy())
mag[f'flux_abs_1_mag_err_0'] = Fzero[7] * (0.4*np.log(10)) * 10**((-0.4)*mag['abs_1_mag_0'].to_numpy()) * mag['abs_1_mag_err_0'].to_numpy()


# Convertir el diccionario a un DataFrame para facilitar la manipulación
mag_df = pd.DataFrame(mag)

# Crear gráficos para cada estrella
for index, row in mag_df.iterrows():
    plt.figure(figsize=(10, 6))
    
    # Obtener los flujos para la estrella actual
    flux_values = np.array([
        row[f'flux_{band}'] for band in bands_I + bands_W
    ])
    flux_values = np.append(flux_values, row['flux_abs_1_mag_0'])  # Añadir el flujo del último valor

    # Error en los flujos
    flux_values_err = np.array([
        row[f'flux_{band}'] for band in bands_I_err + bands_W_err
    ])
    flux_values_err = np.append(flux_values_err, row['flux_abs_1_mag_0'])

    # Ordenar los datos por el eje x
    sorted_indices = np.argsort(Lambda)
    Lambda_sorted = np.array(Lambda)[sorted_indices]
    flux_sorted = np.array(flux_values)[sorted_indices]
    flux_err_sorted = np.array(flux_values_err)[sorted_indices]


    print(index, int(row['OBJECT_ID']), flux_values, "\t")

    # Graficar
    plt.errorbar(np.log10(Lambda_sorted), np.log10(flux_sorted * Lambda_sorted), yerr=flux_err_sorted/(np.log(10)*flux_sorted), fmt='o', ecolor='green', capsize=5, linestyle='-', color='royalblue', markerfacecolor='red', markeredgewidth=0)
    plt.title(f"Flujo vs Longitud de Onda para Estrella ID={int(row['OBJECT_ID'])}")
    plt.xlabel("Log(Longitud de Onda) (µm)")
    plt.ylabel("Log(Flujo x Longitud de Onda) (erg/s/cm²/Hz µm)")
    plt.grid(True)
    plt.savefig(f'./SEDS/seds_{index}.png')
    plt.close()  # Cerrar la figura para liberar memoria

    if int(row['OBJECT_ID']) == 3336110521410475904:
        plt.figure(figsize=(10, 6))
        
        magJ =  12.329 - 5 * np.log10(row['distance_pc']) + 5 - 3.1 * 0.103 * 0.28665
        magH =  11.658 - 5 * np.log10(row['distance_pc']) + 5 - 3.1 * 0.103 * 0.18082
        magK =  11.327 - 5 * np.log10(row['distance_pc']) + 5 - 3.1 * 0.103 * 0.11675
        fluxJ = Fzero[8] * 10**((-0.4)*magJ)
        fluxH = Fzero[9] * 10**((-0.4)*magH)
        fluxK = Fzero[10] * 10**((-0.4)*magK)

        Lambda_sorted = np.insert(Lambda_sorted, 0, 2.159)
        Lambda_sorted = np.insert(Lambda_sorted, 0, 1.662)
        Lambda_sorted = np.insert(Lambda_sorted, 0, 1.235)

        flux_sorted = np.insert(flux_sorted, 0, fluxK)
        flux_sorted = np.insert(flux_sorted, 0, fluxH)
        flux_sorted = np.insert(flux_sorted, 0, fluxJ)

        # Graficar
        plt.plot(np.log10(Lambda_sorted), np.log10(Lambda_sorted*flux_sorted))
        plt.title(f"Flujo vs Longitud de Onda para Estrella ID={int(row['OBJECT_ID'])}")
        plt.xlabel("Log(Longitud de Onda) (µm)")
        plt.ylabel("Log(Flujo x Longitud de Onda) (erg/s/cm²/Hz µm)")
        plt.grid(True)
        plt.savefig(f'./SEDS/seds_{index}_JHK.png')
        plt.close()  # Cerrar la figura para liberar memoria
        
