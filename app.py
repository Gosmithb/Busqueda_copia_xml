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
# txt_file = seleccionar_ruta_txt()

# ##################################################################
# Obtener nombres de archivo en destino (sin rutas)
# nombres_destino = set()
# for root, _, files in os.walk(destino):
#   for file in files:
#     nombres_destino.add(Path(file).stem)

# contador = 1
# # Buscar y eliminar archivos en origen que coincidan por nombre
# for root, _, files in os.walk(origen):
#   for file in files:
#     nombre_sin_extension = Path(file).stem
#     if nombre_sin_extension in nombres_destino:
#       ruta_archivo = Path(root) / file
#       try:
#         ruta_archivo.unlink()
#         # eliminados.append(str(ruta_archivo))
#         print(f"{contador} Eliminado: {ruta_archivo}")
#       except Exception as e:
#         print(f"Error al eliminar {ruta_archivo}: {e}")

# Guardar en TXT
# with open("log_path", "w", encoding="utf-8") as log_file:
#   for ruta in eliminados:
#     log_file.write(ruta + "\n")


########################################################################

# Leer nombres desde el archivo de texto
# with open(txt_file, "r", encoding="utf-8") as f:
#   nombres = [line.strip().split(",") for line in f if line.strip()]

# Para contar xml de cada RFC
# for root, _, files in os.walk(destino):
#   nombre_carpeta = os.path.basename(root)
#   cantidad = len(files)

#   with open(f"ConteoDeXML.txt", "a", encoding="utf-8") as f:
#     f.write(f"RFC {nombre_carpeta} | {cantidad}\n")

########################################################################


# Recortar nombres de archivos a los primeros 13 caracteres y guardarlos en un archivo de texto
# salida_txt = "nombres_recortados.txt"
# with open(salida_txt, "w", encoding="utf-8") as f_out:
#   for archivo in os.listdir(origen):
#     ruta_archivo = os.path.join(origen, archivo)
#     if os.path.isfile(ruta_archivo):
#       nombre_corto = archivo[:13]
#       f_out.write(f"update Hw_nomie222024c1bv2 set timbrados = 'B' where rfc = '{nombre_corto}'\n")

########################################################################

# Leer nombres desde el archivo de texto
# with open(txt_file, "r", encoding="utf-8") as f:
#   nombres = [line.strip().split(",") for line in f if line.strip()]

# if origen and destino and txt_file:
#   print(f"Realizando operaciones en: {destino}")

#   contador = 0
#   for root, _, files in os.walk(origen):
#     files.sort()
#     nombres.sort()

#     for nombre in nombres:
#       index = bisect.bisect_left(files, nombre[0].upper().strip())

#       if index < len(files) and files[index].lower().startswith(nombre[0].lower().strip()):
#         origen_path = Path(root) / files[index]
#         destino_path = Path(destino) / files[index]

#         try:
#           destino_path.parent.mkdir(parents=True, exist_ok=True)
#           shutil.copy2(origen_path, destino_path)

#           # Crear querys para actualizar "retimbrar"
#           # with open(f"UpdateRetimbrarConDiferencias.txt", "a", encoding="utf-8") as f:
#           #   f.write(f"UPDATE Hw_nomie122024c1bv2 SET retimbrar = 'B' WHERE rfc = '{nombre[1]}' and periodo = '202412c1'\n")

#           print(f"{contador}: Copiado de {origen_path} a {destino_path}")
#           contador += 1
#         except Exception as e:
#           print(f"Error copiando {origen}: {e}")

####################################################################

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
