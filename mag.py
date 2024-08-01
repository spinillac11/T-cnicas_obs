import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# Lee el archivo de IRAC y WISE
I = pd.read_csv('./IRAC_output/Table_B35.csv')
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

###### Todo bien hasta este punto

I3_6 = I_filtered_array[mag1]
W4_5 = W_filtered_array[mag2]

# Obtener los identificadores
I_ids = I_filtered_array["OBJECT_ID"]
W_ids = W_filtered_array["OBJECT_ID"]

# Encontrar identificadores comunes
common_ids = np.intersect1d(I_ids, W_ids)

# Filtrar I_filtered_array y W_array para que solo contengan identificadores comunes
I_common_indices = np.isin(I_filtered_array["OBJECT_ID"], common_ids)
W_common_indices = np.isin(W_filtered_array["OBJECT_ID"], common_ids)

I_final_filtered_array = {col: I_filtered_array[col][I_common_indices] for col in I.columns}
W_final_filtered_array = {col: W_filtered_array[col][W_common_indices] for col in W.columns}


print(I_final_filtered_array["OBJECT_ID"])
print(W_final_filtered_array["OBJECT_ID"])


#mag = I_array["1_mag_0"]
#print(mag)

