from datetime import datetime
from dbm import sqlite3
import os
import shutil
import tkinter as tk
from pathlib import Path
from tkinter import filedialog
import bisect
import sqlite3
import xml.etree.ElementTree as ET

import psycopg2

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

herramienta_elegida = input("""
Herramientas
(1) Eliminar archivos en origen que coincidan por nombre con destino (De DESTINO toman los nombres y de ORIGEN elimina los que coincidan)
(2) Copiar archivos de origen a destino, creando estructura de carpetas si no existen, basado en lista txt
(3) Copiar archivos de origen a destino, creando estructura de carpetas si no existen, filtrado por .xml
(4) Insertar o descargar XML a DB postgresql
Seleccione una opción (1-4): 
""")

# ##################################################################
# Obtener nombres de archivo en destino (sin rutas)
if herramienta_elegida == "1":

    origen = seleccionar_ruta()
    destino = seleccionar_ruta()

    nombres_destino = set()
    for root, _, files in os.walk(destino):
        for file in files:
            nombres_destino.add(Path(file).stem)

    contador = 1
    # Buscar y eliminar archivos en origen que coincidan por nombre (sin extensión) con los de destino
    for root, _, files in os.walk(origen):
        for file in files:
            nombre_sin_extension = Path(file).stem
            if nombre_sin_extension in nombres_destino:
                ruta_archivo = Path(root) / file
                try:
                    ruta_archivo.unlink()
                    print(f"{contador} Eliminado: {ruta_archivo}")
                    contador += 1
                except Exception as e:
                    print(f"Error al eliminar {ruta_archivo}: {e}")

########################################################################
# Copiar archivos de origen a destino, creando carpetas si no existen basado en lista txt
elif herramienta_elegida == "2":

    origen = seleccionar_ruta()
    destino = seleccionar_ruta()
    txt_file = seleccionar_ruta_txt()

    with open(txt_file, "r", encoding="utf-8") as f:
        nombres = [line.strip().split(",") for line in f if line.strip()]

    if origen and destino and txt_file:
        print(f"Realizando operaciones en: {destino}")
        contador = 0
        nombres.sort()

        for root, _, files in os.walk(origen):
            files.sort()

            for nombre in nombres:
                index = bisect.bisect_left(files, nombre[0].upper().strip())

                if index < len(files) and os.path.splitext(files[index])[0].upper().strip() == nombre[0].upper().strip():
                    origen_path = Path(root) / files[index]
                    destino_path = Path(destino) / files[index]

                    try:
                        destino_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(origen_path, destino_path)

                        print(f"{contador}: Copiado de {origen_path} a {destino_path}")
                        contador += 1
                    except Exception as e:
                        print(f"Error copiando {origen_path}: {e}")

####################################################################
# Copiar archivos de origen a destino, creando carpetas si no existen filtrado por .xml
elif herramienta_elegida == "3":

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
                if not file.endswith(".xml"):
                    continue

                origen_path = Path(root) / file
                destino_path = destino_dir / file

                try:
                    destino_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(origen_path, destino_path)

                    print(f"{contador}: Copiado de {origen} a {destino_path}")
                    contador += 1
                except Exception as e:
                    print(f"Error copiando {origen}: {e}")

####################################################################
# Insertar o descargar XML a DB Postgresql
elif herramienta_elegida == "4":

    conn = psycopg2.connect(
        host="host",
        database="database",
        user="user",
        password="password",
        port="port"
    )

    nombre_tabla = "nominas_2025.cfdi_nominas"
    errores_log = "Errores_log.txt"
    cursor = conn.cursor()

    def parse_fecha_iso(fecha_str: str):
        if not fecha_str:
            return None
        
        formatos = [
            "%Y-%m-%d",          # solo fecha
            "%Y-%m-%dT%H:%M:%S"  # fecha con hora
        ]
        for fmt in formatos:
            try:
                return datetime.strptime(fecha_str, fmt).date().isoformat()
            except ValueError:
                continue
        return None


    opcion = input("(1) Insertar XML a BD\n(2) Descargar XML de BD desde lista txt\n(3) Descargar y marcar como cancelado (En caso de descargar para cancelar CFDI)\nSeleccione una opción (1-3): ")

    # Guardar xml en sqlite
    def insertarXML():
        origen = seleccionar_ruta()
        with open(errores_log, "a", encoding="utf-8") as log_file:
            for rootPath, _, files in os.walk(origen):
                for file in files:
                    if file.endswith(".xml"):
                        ruta_archivo = Path(rootPath) / file
                        try:
                            # Leer contenido xml para parsear a txt
                            with open(ruta_archivo, "r", encoding="utf-8-sig") as file:
                                xml_content = file.read()
                            
                            tree = ET.parse(ruta_archivo)
                            root = tree.getroot()

                            ns = {
                                'cfdi': '',
                                'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital',
                                'nomina12': 'http://www.sat.gob.mx/nomina12'
                            }

                            # Determinar version del cfdi
                            version = root.attrib.get("Version")
                            if version == "4.0":
                                ns['cfdi'] = "http://www.sat.gob.mx/cfd/4"
                            elif version == "3.3":
                                ns['cfdi'] = "http://www.sat.gob.mx/cfd/3"

                            receptor_elem = root.find('.//cfdi:Receptor', ns)
                            nomina_elem = root.find('.//nomina12:Nomina', ns)
                            nomina_receptor_elem = nomina_elem.find('.//nomina12:Receptor', ns) if nomina_elem is not None else None
                            timbre_fiscal_digital_elem = root.find('.//tfd:TimbreFiscalDigital', ns)
                            entidad_sncf_elem = nomina_elem.find('.//nomina12:EntidadSNCF', ns) if nomina_elem is not None else None
                            nomina_deducciones_elem = nomina_elem.find('.//nomina12:Deducciones', ns) if nomina_elem is not None else None

                            if receptor_elem is None or nomina_elem is None or timbre_fiscal_digital_elem is None:
                                print(f"Error: {ruta_archivo} no contiene los elementos necesarios, se omitirá.")
                                continue

                            # Datos comprobante
                            llave = Path(ruta_archivo).stem
                            sub_total = float(root.attrib.get('SubTotal', '0.00') or '0.00')
                            total = float(root.attrib.get('Total', '0.00') or '0.00')
                            fecha = root.attrib.get('Fecha') or ''

                            # Datos receptor
                            rfc_receptor = receptor_elem.attrib.get('Rfc', '')
                            domicilio_fiscal = receptor_elem.attrib.get('DomicilioFiscalReceptor', '') or None

                            # Datos nomina
                            fecha_pago = nomina_elem.attrib.get('FechaPago') or ''
                            total_impuestos_retenidos = float(nomina_deducciones_elem.attrib.get('TotalImpuestosRetenidos', '0.00')) if nomina_deducciones_elem is not None else 0.00
                            origen_recurso = entidad_sncf_elem.attrib.get('OrigenRecurso', '') if entidad_sncf_elem is not None else None
                            tipo_nomina = nomina_elem.attrib.get('TipoNomina', '')
                            total_deducciones = float(nomina_elem.attrib.get('TotalDeducciones', '0.00') or '0.00')
                            numero_plaza = nomina_receptor_elem.attrib.get('Puesto') if nomina_receptor_elem is not None else None

                            # Datos timbre fiscal digital
                            uuid = timbre_fiscal_digital_elem.attrib.get('UUID', '')
                            fecha_timbrado = timbre_fiscal_digital_elem.attrib.get('FechaTimbrado', '')

                            cursor.execute(f"""
                                INSERT INTO {nombre_tabla} (
                                    llave, 
                                    domicilio_fiscal_receptor,
                                    rfc,
                                    numero_plaza,
                                    origen_recurso,
                                    tipo_nomina,
                                    uuid,
                                    fecha,
                                    fecha_pago,
                                    fecha_timbrado,
                                    total_deducciones,
                                    total_impuestos_retenidos,
                                    sub_total,
                                    total,
                                    xml_content
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (uuid) DO NOTHING
                                """, (
                                    llave, 
                                    domicilio_fiscal, 
                                    rfc_receptor, 
                                    numero_plaza,
                                    origen_recurso, 
                                    tipo_nomina,
                                    uuid, 
                                    parse_fecha_iso(fecha), 
                                    parse_fecha_iso(fecha_pago), 
                                    parse_fecha_iso(fecha_timbrado), 
                                    total_deducciones,
                                    total_impuestos_retenidos, 
                                    sub_total, 
                                    total, 
                                    xml_content #Se guarda como tipo xml (TEXT en sqlite, XML en postgres)
                            )) 
                            
                            print(f"Insertado: {ruta_archivo} en {nombre_tabla}")
                            conn.commit()
                        except Exception as e:
                            mensaje_error = f"Error al procesar {ruta_archivo}: {e}\n"
                            print(f"Error al procesar {ruta_archivo}: {e}")
                            log_file.write(mensaje_error)
                            continue
        conn.commit()

    # Descargar archivos .xml de la bd
    def descargarEliminarXMLdeBD(eliminar: bool = False):
        txt_file = seleccionar_ruta_txt()
        destino = seleccionar_ruta()

        with open(txt_file, "r", encoding="utf-8") as f:
            nombres = [line.strip() for line in f if line.strip()]

        Path(destino).mkdir(parents=True, exist_ok=True)
        for nombre in nombres:
            cursor.execute(f"SELECT xml_content FROM {nombre_tabla} WHERE llave = %s OR uuid = %s", (nombre, nombre))
            row = cursor.fetchone()
            if row is None: 
                print(f"No se encontró XML para: {nombre}")
                continue
                
            xml_content = row[0]

            # Eliminar BOM si existe
            if xml_content.startswith("\ufeff"):
                xml_content = xml_content.lstrip("\ufeff")

            with open(f"{destino}/{nombre}.xml", "w", encoding="utf-8") as xml_file:
                xml_file.write(xml_content)

            if eliminar:
                cursor.execute(
                    f"UPDATE {nombre_tabla} SET vigente = False WHERE llave = %s OR uuid = %s",
                    (nombre, nombre)
                )
            
            print(f"Descargado: {destino}/{nombre}.xml de {nombre_tabla}")

    if opcion == "1":
        insertarXML()
    elif opcion == "2":
        descargarEliminarXMLdeBD(eliminar=False)
    elif opcion == "3":
        descargarEliminarXMLdeBD(eliminar=True)
    else:
        print("Opción no válida.")

    conn.close()

print("Operación completada.")
