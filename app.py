import os
import shutil
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
import bisect

def seleccionar_ruta():
  root = tk.Tk()
  root.withdraw()  # Oculta la ventana principal de Tkinter
  ruta = filedialog.askdirectory()
  if ruta:
    print(f"Ruta seleccionada: {ruta}")
  else:
    print("No se seleccionó ninguna carpeta.")
  return ruta

def seleccionar_ruta_txt():
  root = tk.Tk()
  root.withdraw()  # Oculta la ventana principal de Tkinter
  ruta = filedialog.askopenfilename()
  if ruta:
    print(f"Txt seleccionado: {ruta}")
  else:
    print("No se seleccionó ningun archivo.")
  return ruta

# # Rutas
origen = seleccionar_ruta()
contador = 1
for root, _, files in os.walk(origen):
  files.sort()
  print(files)
  print("Len: ", len(files))
  print(f'{contador}: ############################################################################')
  contador += 1
# destino = seleccionar_ruta()
# txt_file = seleccionar_ruta_txt()

# # Leer nombres desde el archivo de texto
# with open(txt_file, "r", encoding="utf-8") as f:
#   nombres = [line.strip() for line in f if line.strip()]

# if origen and destino and txt_file:
#   print(f"Realizando operaciones en: {destino}")

#   # Crear carpeta de destino si no existe
#   Path(destino).mkdir(parents=True, exist_ok=True)

  # Recorrer árbol de archivos solo una vez (mejor rendimiento)
  # contador = 1
  # for root, _, files in os.walk(origen):
    # for file in files:
      # if file.endswith(".xml"):
        # for i, nombre in enumerate(nombres):
        #   print(f"Comparando {nombre} y su posicion {i}")
        #   try:
        #     if file.lower().startswith(nombre.lower().strip()):
        #       origen_file = Path(root) / file
        #       destino_file = Path(destino) / file
              
        #       print(f"Comparando {origen_file.stem} con {nombre}")

        #       try:
        #         shutil.copy2(origen_file, destino_file)
        #         print(f"{contador}: Copiado {origen_file.stem} a {destino_file}")
        #       except Exception as e:
        #         print(f"Error copiando {origen}: {e}")
              
        #       contador += 1 #Elemento para tener un control visual sobre los archivos copiados
        #       nombres.pop(i) # Eliminar el nombre una vez que se ha encontrado para evitar evualuar datos innecesarios
        #       break  # Ya coincide con un nombre, no seguir comparando

        #     else:
        #       print(f"{contador} No coincide {file} con {nombre}")

        #   except Exception as e:
        #     print(f"Error: {e}")
  
print("Operación completada.")
