import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# Lee el archivo de IRAC y WISE
I = pd.read_csv('./IRAC_output/Table_NGC2264_4.csv')
#W = pd.read_csv('./WISE_output/Table_0857p090_ac51.csv')

# Crea un diccionario donde las claves son los nombres de las columnas y los valores son las columnas como arrays
I_array = {col: I[col].to_numpy() for col in I.columns}
#W_array = {col: W[col].to_numpy() for col in W.columns}


mag1, mag2, mag3, mag4 = '1_mag_0', '2_mag_0', '3_mag_0', '4_mag_0' 
mag1_error, mag2_error, mag3_error, mag4_error = '1_mag_err_0', '2_mag_err_0', '3_mag_err_0', '4_mag_err_0' 
 

# Calcular el error porcentual
I1_error_pct = np.abs(I_array[mag1_error] / I_array[mag1]) * 100
I2_error_pct = np.abs(I_array[mag2_error] / I_array[mag2]) * 100
I3_error_pct = np.abs(I_array[mag3_error] / I_array[mag3]) * 100
I4_error_pct = np.abs(I_array[mag4_error] / I_array[mag4]) * 100

#W1_error_pct = np.abs(W_array[mag1_error] / W_array[mag1]) * 100
#W2_error_pct = np.abs(W_array[mag2_error] / W_array[mag2]) * 100
#W3_error_pct = np.abs(W_array[mag3_error] / W_array[mag3]) * 100
#W4_error_pct = np.abs(W_array[mag4_error] / W_array[mag4]) * 100

# Filtrar índices donde el error porcentual es <= 20%
I_valid_indices = (I1_error_pct <= 20) & (I2_error_pct <= 20) & (I3_error_pct <= 20) & (I4_error_pct <= 20) 
#W_valid_indices = (W1_error_pct <= 20) & (W2_error_pct <= 20) & (W3_error_pct <= 20) & (W4_error_pct <= 20)

# Aplicar el filtro a todos los arrays
I_filtered_array = {col: I_array[col][I_valid_indices] for col in I.columns}
#W_filtered_array = {col: W_array[col][W_valid_indices] for col in W.columns}

###### Cálculo magnitud absoluta con extinción 

# Lee el archivo de paralaje, seleccionando las columnas 3 y 4 (identificador y paralaje)
parallax_data = pd.read_csv('./Input/I1_filtrado.txt', delimiter=' ', header=None, usecols=[2, 3], names=['identifier', 'parallax'])

# Filtrar datos de paralaje inválidos
parallax_data = parallax_data[parallax_data['parallax'] > 0]

# Crear DataFrame filtrado
I_filtered = pd.DataFrame(I_filtered_array)

# Fusionar los datos del paralaje con los datos filtrados
merged_data = I_filtered.merge(parallax_data, left_on='OBJECT_ID', right_on='identifier')

# Convertir el paralaje de milisegundos de arco a segundos de arco
merged_data['parallax_arcsec'] = merged_data['parallax'] / 1000.0

# Calcular la distancia en parsecs
merged_data['distance_pc'] = 1000.0 / merged_data['parallax_arcsec']

# Calcular la magnitud absoluta usando la fórmula M = m - 5 log10(d) + 5
for mag in [mag1, mag2, mag3, mag4]:
    merged_data[f'abs_{mag}'] = merged_data[mag] - 5 * np.log10(merged_data['distance_pc']) + 5

# Imprimir los resultados
print(merged_data[['OBJECT_ID', mag1, f'abs_{mag1}', mag2, f'abs_{mag2}', mag3, f'abs_{mag3}', mag4, f'abs_{mag4}']])

# Calcular los colores [3.6-4.5] y [5.8-8.0]
merged_data['color1'] = merged_data[mag1] - merged_data[mag2]
merged_data['color2'] = merged_data[mag3] - merged_data[mag4]

# Crear el diagrama color-color
plt.figure(figsize=(10, 6))
plt.scatter(merged_data['color1'], merged_data['color2'], alpha=0.5)
plt.xlabel('[3.6 - 4.5]')
plt.ylabel('[5.8 - 8.0]')
plt.title('Diagrama Color-Color desenrojecido')
plt.grid(True)
plt.savefig('./Figuras/[3.6-4.5]_[5.8 - 8.0].png')