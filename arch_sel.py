import pandas as pd
import os

# Nombre del archivo de entrada
input_file = './Input/w1.tsv'  # Reemplaza con el nombre de tu archivo

# Extrae el nombre del archivo sin la extensión
base_name = os.path.splitext(input_file)[0]

# Define el nombre del archivo de salida con el sufijo '_filtrado'
output_file = f'{base_name}_filtrado.txt'

# Lee el archivo TSV y omite la primera fila (usando skiprows)
df = pd.read_csv(input_file, sep='\t', skiprows=1)

# Selecciona solo las columnas 1, 2 y 7 (pandas usa indexación basada en 0)
df_filtered = df.iloc[:, [0, 1, 6]]

# Guarda el nuevo archivo .txt con columnas separadas por un espacio
df_filtered.to_csv(output_file, sep=' ', index=False, header=False)

print(f'Archivo procesado y guardado como {output_file}')