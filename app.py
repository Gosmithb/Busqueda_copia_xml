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

if origen and destino:
    print(f"Realizando operaciones en: {destino}")

    contador = 0
    for root, _, files in os.walk(origen):
        # Crear las carpetas (aunque estén vacías)
        rel_path = Path(root).relative_to(origen)
        destino_dir = Path(destino) / rel_path
        destino_dir.mkdir(parents=True, exist_ok=True)

        for file in files:
            origen_path = Path(root) / file
            destino_path = destino_dir / file

            try:
                destino_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(origen_path, destino_path)

                print(f"{contador}: Copiado de {origen} a {destino_path}")
                contador += 1
            except Exception as e:
                print(f"Error copiando {origen}: {e}")

print("Operación completada.")
