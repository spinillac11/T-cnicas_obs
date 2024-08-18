import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# Lee el archivo de IRAC y WISE
I = pd.read_csv('./IRAC_output/Table_B35.csv')
##### Es WISE
W = pd.read_csv('./WISE_output/Table_0857p090_ac51.csv')

# Crea un diccionario donde las claves son los nombres de las columnas y los valores son las columnas como arrays
I_array = {col: I[col].to_numpy() for col in I.columns}
W_array = {col: W[col].to_numpy() for col in W.columns}


mag1, mag2, mag3, mag4 = '1_mag_0', '2_mag_0', '3_mag_0', '4_mag_0' 
mag1_error, mag2_error, mag3_error, mag4_error = '1_mag_err_0', '2_mag_err_0', '3_mag_err_0', '4_mag_err_0' 
 

# Calcular el error porcentual
I1_error_pct = np.abs(I_array[mag1_error] / I_array[mag1]) * 100
I2_error_pct = np.abs(I_array[mag2_error] / I_array[mag2]) * 100
I3_error_pct = np.abs(I_array[mag3_error] / I_array[mag3]) * 100
I4_error_pct = np.abs(I_array[mag4_error] / I_array[mag4]) * 100

W1_error_pct = np.abs(W_array[mag1_error] / W_array[mag1]) * 100
W2_error_pct = np.abs(W_array[mag2_error] / W_array[mag2]) * 100
W3_error_pct = np.abs(W_array[mag3_error] / W_array[mag3]) * 100
W4_error_pct = np.abs(W_array[mag4_error] / W_array[mag4]) * 100

# Filtrar índices donde el error porcentual es <= 20%
I_valid_indices = (I1_error_pct <= 20) & (I2_error_pct <= 20) & (I3_error_pct <= 20) & (I4_error_pct <= 20) 
W_valid_indices = (W1_error_pct <= 20) & (W2_error_pct <= 20) & (W3_error_pct <= 20) & (W4_error_pct <= 20)

# Aplicar el filtro a todos los arrays
I_filtered_array = {col: I_array[col][I_valid_indices] for col in I.columns}
W_filtered_array = {col: W_array[col][W_valid_indices] for col in W.columns}

###### Cálculo magnitud absoluta con extinción 

# Lee el archivo de paralaje, seleccionando las columnas 3 y 4 (identificador y paralaje)
Gaia_data = pd.read_csv('./Input/I1_filtrado.txt', delimiter=' ', header=None, usecols=[2, 3, 4, 5, 6], names=['identifier', 'parallax', 'parallax_err', 'Gmag', 'Gmag_err'])

# Filtrar datos de paralaje inválidos
Gaia_data = Gaia_data[Gaia_data['parallax'] > 0]
Gaia_data = Gaia_data[(Gaia_data['parallax_err']/ Gaia_data['parallax']) <= 20]

# Crear DataFrame filtrado
I_filtered = pd.DataFrame(I_filtered_array)
W_filtered = pd.DataFrame(W_filtered_array)

# Fusionar los datos del paralaje con los datos filtrados
merged_data_I = I_filtered.merge(Gaia_data, left_on='OBJECT_ID', right_on='identifier')
merged_data_W = W_filtered.merge(Gaia_data, left_on='OBJECT_ID', right_on='identifier')

# Calcular la distancia en parsecs
merged_data_I['distance_pc'] = 1000.0 / merged_data_I['parallax']
merged_data_W['distance_pc'] = 1000.0 / merged_data_W['parallax']

# Calcular la magnitud absoluta usando la fórmula M = m - 5 log10(d) + 5
for mag in [mag1, mag2, mag3, mag4, 'Gmag']:
    merged_data_I[f'abs_{mag}'] = merged_data_I[mag] - 5 * np.log10(merged_data_I['distance_pc']) + 5
    merged_data_W[f'abs_{mag}'] = merged_data_W[mag] - 5 * np.log10(merged_data_W['distance_pc']) + 5

# Imprimir los resultados
print(merged_data_I[['OBJECT_ID', mag1, f'abs_{mag1}', mag2, f'abs_{mag2}', mag3, f'abs_{mag3}', mag4, f'abs_{mag4}', 'abs_Gmag', 'parallax', 'parallax_err']])

# Calcular los colores [3.6-4.5] y [5.8-8.0]
merged_data_I['3.6-4.5'] = merged_data_I[f'abs_{mag1}'] - merged_data_I[f'abs_{mag2}']
merged_data_I['5.8-8.0'] = merged_data_I[f'abs_{mag3}'] - merged_data_I[f'abs_{mag4}']

# Calcular los colores [3.6-4.5] y [5.8-8.0]
merged_data_I['Gmag-3.6'] = merged_data_I['abs_Gmag'] - merged_data_I[f'abs_{mag1}']
merged_data_I['4.5-22'] = merged_data_I[f'abs_{mag1}'] - merged_data_W[f'abs_{mag4}']

# Crear el diagrama color-color
plt.figure(figsize=(10, 6))
plt.scatter(merged_data_I['5.8-8.0'], merged_data_I['3.6-4.5'], alpha=0.5)
plt.xlabel('[5.8 - 8.0]')
plt.ylabel('[3.6 - 4.5]')
plt.title('Diagrama Color-Color desenrojecido')
plt.grid(True)
plt.savefig('./Figuras/[3.6-4.5]_[5.8 - 8.0].png')

# Crear el diagrama color-color
plt.figure(figsize=(10, 6))
plt.scatter(merged_data_I['4.5-22'], merged_data_I['Gmag-3.6'], alpha=0.5)
plt.xlabel('[4.5-22]')
plt.ylabel('[Gmag-3.6]')
plt.title('Diagrama Color-Color desenrojecido')
plt.grid(True)
plt.savefig('./Figuras/[Gmag-3.6]_[4.5-22].png')