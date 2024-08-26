import pandas as pd
import numpy as np
import matplotlib.pylab as plt


# Lee el archivo de IRAC y WISE
I = pd.read_csv('./IRAC_output/Table_B35.csv')
##### WISE
W = pd.read_csv('./WISE_output/Table_0857p090_ac51.csv')
##### MIPS
M = pd.read_csv('./MIPS_output/Table_B35.csv')


# Crea un diccionario donde las claves son los nombres de las columnas y los valores son las columnas como arrays
I_array = {col: I[col].to_numpy() for col in I.columns}
W_array = {col: W[col].to_numpy() for col in W.columns}
M_array = {col: M[col].to_numpy() for col in M.columns}

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

M1_error_pct = np.abs(M_array[mag1_error] / M_array[mag1]) * 100
## M2_error_pct = np.abs(M_array[mag2_error] / M_array[mag2]) * 100

# Filtrar índices donde el error porcentual es <= 20%
I_valid_indices = (I1_error_pct <= 20) & (I2_error_pct <= 20) & (I3_error_pct <= 20) & (I4_error_pct <= 20) 
W_valid_indices = (W1_error_pct <= 20) & (W2_error_pct <= 20) & (W3_error_pct <= 20) & (W4_error_pct <= 20)
M_valid_indices = (M1_error_pct <= 20)  
## & (M2_error_pct <= 20)


# Aplicar el filtro a todos los arrays
I_filtered_array = {col: I_array[col][I_valid_indices] for col in I.columns}
W_filtered_array = {col: W_array[col][W_valid_indices] for col in W.columns}
M_filtered_array = {col: M_array[col][M_valid_indices] for col in M.columns}


# Crear DataFrame filtrado
I_filtered = pd.DataFrame(I_filtered_array)
W_filtered = pd.DataFrame(W_filtered_array)
M_filtered = pd.DataFrame(M_filtered_array)

print(I_filtered["OBJECT_ID"])

###### Cálculo magnitud absoluta con extinción 

# Lee el archivo de paralaje, seleccionando las columnas 3 y 4 (identificador y paralaje)
Gaia_data_I = pd.read_csv('./Input/I1_filtrado.txt', delimiter=' ', header=None, usecols=[2, 3, 4, 5, 6], names=['identifier', 'parallax', 'parallax_err', 'Gmag', 'Gmag_err'])
Gaia_data_W = pd.read_csv('./Input/w1_filtrado.txt', delimiter=' ', header=None, usecols=[2, 3, 4, 5, 6], names=['identifier', 'parallax', 'parallax_err', 'Gmag', 'Gmag_err'])
Gaia_data_M = pd.read_csv('./Input/M1_filtrado.txt', delimiter=' ', header=None, usecols=[2, 3, 4, 5, 6], names=['identifier', 'parallax', 'parallax_err', 'Gmag', 'Gmag_err'])

# Filtrar datos de paralaje inválidos
Gaia_data_I = Gaia_data_I[Gaia_data_I['parallax'] > 0]
Gaia_data_W = Gaia_data_W[Gaia_data_W['parallax'] > 0]
Gaia_data_M = Gaia_data_M[Gaia_data_M['parallax'] > 0]
Gaia_data_I = Gaia_data_I[(Gaia_data_I['parallax_err']/ Gaia_data_I['parallax']) <= 20]
Gaia_data_W = Gaia_data_W[(Gaia_data_W['parallax_err']/ Gaia_data_W['parallax']) <= 20]
Gaia_data_M = Gaia_data_M[(Gaia_data_M['parallax_err']/ Gaia_data_M['parallax']) <= 20]


# Fusionar los datos del paralaje con los datos filtrados
merged_data_I = I_filtered.merge(Gaia_data_I, left_on='OBJECT_ID', right_on='identifier')
merged_data_W = W_filtered.merge(Gaia_data_W, left_on='OBJECT_ID', right_on='identifier')
merged_data_M = M_filtered.merge(Gaia_data_I, left_on='OBJECT_ID', right_on='identifier')

# Calcular la distancia en parsecs
merged_data_I['distance_pc'] = 1000.0 / merged_data_I['parallax']
merged_data_W['distance_pc'] = 1000.0 / merged_data_W['parallax']
merged_data_M['distance_pc'] = 1000.0 / merged_data_M['parallax']


# Calcular la magnitud absoluta usando la fórmula M = m - 5 log10(d) + 5
#for mag in [mag1, mag2, mag3, mag4, 'Gmag']:
    #merged_data_I[f'abs_{mag}'] = merged_data_I[mag] - 5 * np.log10(merged_data_I['distance_pc']) + 5
    #merged_data_W[f'abs_{mag}'] = merged_data_W[mag] - 5 * np.log10(merged_data_W['distance_pc']) + 5

# Array con los valores A_lambda / A_v de WEBDA
#                           J	    H	    Ks	   IRAC_3.6	IRAC_4.5 IRAC_5.8 IRAC_8.0 MIPS_24  MIPS_70	 MIPS_160	W1	      W2	   W3	    W4
WebdaValues = np.array([0.28665, 0.18082, 0.11675, 0.05228,	0.03574, 0.02459, 0.01433, 0.00245, 0.00041, 0.00012, 0.05688, 0.03427, 0.00707, 0.00274])

# Calcula la magnitud absoluta y corrige por extinsión usando la fórmula M = m - 5 log10(d) + 5 - A_channel
# A_lambda = 3.1 * ReddeningLambdaOrionis * WebdaValue
# A_lambda = 3.1 * 0.103 * WebdaValue
# IRAC
merged_data_I[f'abs_{mag1}'] = merged_data_I[mag1] - 5 * np.log10(merged_data_I['distance_pc']) + 5 - 3.1 * 0.103 * WebdaValues[3]
merged_data_I[f'abs_{mag2}'] = merged_data_I[mag2] - 5 * np.log10(merged_data_I['distance_pc']) + 5 - 3.1 * 0.103 * WebdaValues[4]
merged_data_I[f'abs_{mag3}'] = merged_data_I[mag3] - 5 * np.log10(merged_data_I['distance_pc']) + 5 - 3.1 * 0.103 * WebdaValues[5]
merged_data_I[f'abs_{mag4}'] = merged_data_I[mag4] - 5 * np.log10(merged_data_I['distance_pc']) + 5 - 3.1 * 0.103 * WebdaValues[6]
merged_data_I[f'abs_Gmag'] = merged_data_I['Gmag'] - 5 * np.log10(merged_data_I['distance_pc']) + 5 - 3.1 * 0.103
# WISE
merged_data_W[f'abs_{mag1}'] = merged_data_W[mag1] - 5 * np.log10(merged_data_W['distance_pc']) + 5 - 3.1 * 0.103 * WebdaValues[10]
merged_data_W[f'abs_{mag2}'] = merged_data_W[mag2] - 5 * np.log10(merged_data_W['distance_pc']) + 5 - 3.1 * 0.103 * WebdaValues[11]
merged_data_W[f'abs_{mag3}'] = merged_data_W[mag3] - 5 * np.log10(merged_data_W['distance_pc']) + 5 - 3.1 * 0.103 * WebdaValues[12]
merged_data_W[f'abs_{mag4}'] = merged_data_W[mag4] - 5 * np.log10(merged_data_W['distance_pc']) + 5 - 3.1 * 0.103 * WebdaValues[13]
merged_data_W[f'abs_Gmag'] = merged_data_W['Gmag'] - 5 * np.log10(merged_data_W['distance_pc']) + 5 - 3.1 * 0.103
#MIPS
merged_data_M[f'abs_{mag1}'] = merged_data_M[mag1] - 5 * np.log10(merged_data_M['distance_pc']) + 5 - 3.1 * 0.103 * WebdaValues[7]
## merged_data_M[f'abs_{mag2}'] = merged_data_M[mag2] - 5 * np.log10(merged_data_M['distance_pc']) + 5 - 3.1 * 0.103 * WebdaValues[8]
merged_data_M[f'abs_Gmag'] = merged_data_M['Gmag'] - 5 * np.log10(merged_data_M['distance_pc']) + 5 - 3.1 * 0.103

# Imprimir los resultados
#print(merged_data_I[['OBJECT_ID', mag1, f'abs_{mag1}', mag2, f'abs_{mag2}', mag3, f'abs_{mag3}', mag4, f'abs_{mag4}', 'abs_Gmag', 'parallax', 'parallax_err']])
print(merged_data_W[['OBJECT_ID', mag1, f'abs_{mag1}', mag2, f'abs_{mag2}', mag3, f'abs_{mag3}', mag4, f'abs_{mag4}', 'abs_Gmag', 'parallax', 'parallax_err']])
#print(merged_data_M[['OBJECT_ID', mag1, f'abs_{mag1}', mag2, f'abs_{mag2}', 'abs_Gmag', 'parallax', 'parallax_err']])

# Calcular los colores [3.6-4.5] y [5.8-8.0]
merged_data_I['3.6-4.5'] = merged_data_I[f'abs_{mag1}'] - merged_data_I[f'abs_{mag2}']
merged_data_I['5.8-8.0'] = merged_data_I[f'abs_{mag3}'] - merged_data_I[f'abs_{mag4}']

# Primero hacemos el merge de los primeros dos DataFrames (merged_data_I y merged_data_W)
merged_IW = pd.merge(merged_data_I, merged_data_W, on='OBJECT_ID', suffixes=('_I', '_W'))

# Luego hacemos el merge del resultado anterior con el tercer DataFrame (merged_data_M)
merged_IM = pd.merge(merged_data_I, merged_data_M, on='OBJECT_ID', suffixes=('_I', '_M'))

# Calcular los colores [Gmag-3.6] y [4.5-22]
merged_IW['Gmag-3.6'] = merged_IW['abs_Gmag_I'] - merged_IW[f'abs_{mag1}_I']
merged_IW['4.5-22'] = merged_IW[f'abs_{mag2}_I'] - merged_IW[f'abs_{mag4}_W']

#Colores [Gmag-3.6] y [4.5-24]
merged_IM['Gmag-3.6'] = merged_IM['abs_Gmag_I'] - merged_IM[f'abs_{mag1}_I']
#merged_IM['4.5-24'] = merged_IM[f'abs_{mag2}_I'] - merged_IM[f'abs_{mag1}_M']

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
plt.scatter(merged_IW['4.5-22'], merged_IW['Gmag-3.6'], alpha=0.5)
plt.xlabel('[4.5-22]')
plt.ylabel('[Gmag-3.6]')
plt.title('Diagrama Color-Color desenrojecido')
plt.grid(True)
plt.savefig('./Figuras/[Gmag-3.6]_[4.5-22].png')

# Crear el diagrama color-color
##plt.figure(figsize=(10, 6))
##plt.scatter(merged_IM['4.5-24'], merged_IM['Gmag-3.6'], alpha=0.5)
##plt.xlabel('[4.5-24]')
##plt.ylabel('[Gmag-3.6]')
##plt.title('Diagrama Color-Color desenrojecido')
##plt.grid(True)
##plt.savefig('./Figuras/[Gmag-3.6]_[4.5-24].png')

################# SEDS ##############

final_merge = pd.merge(merged_IW, merged_data_M, on='OBJECT_ID', suffixes=('', '_M'))

final_merge['3.6-4.5'] = final_merge[f'abs_{mag1}_I'] - final_merge[f'abs_{mag2}_I']
final_merge['5.8-8.0'] = final_merge[f'abs_{mag3}_I'] - final_merge[f'abs_{mag4}_I']

plt.figure(figsize=(10, 6))
plt.scatter(final_merge['5.8-8.0'], final_merge['3.6-4.5'], alpha=0.5)
plt.xlabel('[5.8 - 8.0]')
plt.ylabel('[3.6 - 4.5]')
plt.title('Diagrama Color-Color desenrojecido')
plt.grid(True)
plt.savefig('./Figuras/final_[3.6-4.5]_[5.8 - 8.0].png')

final_merge.to_csv("./SEDS/merged_data.csv", index=False)