import pandas as pd
import os

# Nombre del archivos de entrada
input_file1 = './Input/I1.tsv'  
#input_file2 = './Input/w1.tsv' 
#input_file3 = './Input/I1.tsv'  

# Extrae el nombre del archivo sin la extensión
base_name1 = os.path.splitext(input_file1)[0]
#base_name2 = os.path.splitext(input_file2)[0]
#base_name3 = os.path.splitext(input_file3)[0]

# Define el nombre del archivo de salida con el sufijo '_filtrado'
output_file1 = f'{base_name1}_filtrado.txt'
#output_file2 = f'{base_name2}_filtrado.txt'
#output_file3 = f'{base_name1}_filtrado.txt'

# Lee el archivo TSV y omite el header
df1 = pd.read_csv(input_file1, sep='\t', skiprows=0)
#df2 = pd.read_csv(input_file2, sep='\t', skiprows=0)
#df3 = pd.read_csv(input_file3, sep='\t', skiprows=0)

# Selecciona las columnas AR, DEJ, ID, Plx, Plx_E, Gmag y e_Gmag
df1_filtered = df1.iloc[:, [0, 1, 6, 7, 8, 16, 17]]
#df2_filtered = df2.iloc[:, [0, 1, 6, 7, 8, 16, 17]]
#df3_filtered = df3.iloc[:, [0, 1, 6, 7, 8, 16, 17]]

# Guarda el nuevo archivo .txt 
df1_filtered.to_csv(output_file1, sep=' ', index=False, header=False)
#df2_filtered.to_csv(output_file2, sep=' ', index=False, header=False)
#df3_filtered.to_csv(output_file2, sep=' ', index=False, header=False)

print(f'Archivo procesado y guardado como {output_file1}')
#print(f'Archivo procesado y guardado como {output_file2}')
#print(f'Archivo procesado y guardado como {output_file3}')