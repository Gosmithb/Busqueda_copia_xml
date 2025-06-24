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

# Rutas
origen = seleccionar_ruta()
destino = seleccionar_ruta()
txt_file = seleccionar_ruta_txt()

# Leer nombres desde el archivo de texto
with open(txt_file, "r", encoding="utf-8") as f:
  nombres = [line.strip() for line in f if line.strip()]

if origen and destino and txt_file:
  print(f"Realizando operaciones en: {destino}")

  # Crear carpeta de destino si no existe
  Path(destino).mkdir(parents=True, exist_ok=True)

  contador = 0
  for root, _, files in os.walk(origen):
    files.sort()
    nombres.sort()

    for nombre in nombres:
      index = bisect.bisect_left(files, nombre.upper().strip())

      if index < len(files) and files[index].lower().startswith(nombre.lower().strip()):
        origen_file = Path(root) / files[index]
        destino_file = Path(destino) / files[index]

        try:
          shutil.copy2(origen_file, destino_file)
          print(f"{contador}: Copiado de {origen_file} a {destino_file}")
        except Exception as e:
          print(f"Error copiando {origen}: {e}")
        contador += 1

print("Operación completada.")
