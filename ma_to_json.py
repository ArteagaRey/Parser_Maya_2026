#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import argparse

# Lista global para acumular los errores encontrados en todo el lote (batch)
CORRUPT_NODES_REPORT = []

def parse_maya_ascii(input_path):
    """
    Lee un archivo .ma línea por línea, extrae los nodos de tipo 'mesh'
    y audita si existen nodos corruptos o rotos ('unknown').
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"El archivo no existe: {input_path}")
    
    if not input_path.endswith('.ma'):
        raise ValueError("El archivo debe tener extensión .ma (Maya ASCII)")

    mesh_regex = re.compile(r'^createNode\s+mesh\s+.*-n\s+"([^"]+)"')
    parent_regex = re.compile(r'-p\s+"([^"]+)"')
    attr_regex = re.compile(r'^\s+([a-zA-Z0-9]+.*);')

    meshes = []
    current_mesh = None
    file_name = os.path.basename(input_path)

    with open(input_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line_num, line in enumerate(file, 1):
            
            # Detección de nodos corruptos (unknown)
            if line.startswith('createNode unknown'):
                CORRUPT_NODES_REPORT.append({
                    "archivo": file_name,
                    "linea": line_num,
                    "detalle": "Nodo 'unknown' detectado (Plugin faltante o escena rota)"
                })

            # Lógica de extracción de meshes
            if line.startswith('createNode mesh'):
                if current_mesh:
                    meshes.append(current_mesh)

                name_match = mesh_regex.search(line)
                if not name_match:
                    continue
                
                name = name_match.group(1)
                parent_match = parent_regex.search(line)
                parent = parent_match.group(1) if parent_match else None

                current_mesh = {
                    "name": name,
                    "parent": parent,
                    "attrs": []
                }
                continue

            if current_mesh and (line.startswith(' ') or line.startswith('\t')):
                attr_match = attr_regex.search(line)
                if attr_match:
                    current_mesh["attrs"].append(line.strip())
            
            elif current_mesh and line.strip() and not (line.startswith(' ') or line.startswith('\t')):
                meshes.append(current_mesh)
                current_mesh = None

        if current_mesh:
            meshes.append(current_mesh)

    return meshes


def process_batch(input_folder, output_folder):
    """
    Escanea una carpeta completa, junta la información de todas las escenas
    y exporta UN SOLO archivo JSON unificado.
    """
    if not os.path.exists(input_folder):
        print(f"[ERROR] La carpeta de entrada no existe: {input_folder}")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    all_files = [f for f in os.listdir(input_folder) if f.endswith('.ma')]
    total_files = len(all_files)
    
    print(f"[INFO] Se encontraron {total_files} archivos .ma para procesar.")
    
    # Este diccionario guardará la base de datos completa de todas las escenas
    all_scenes_database = {}
    processed_count = 0
    
    for file_name in all_files:
        full_input_path = os.path.join(input_folder, file_name)
        scene_name_base = os.path.splitext(file_name)[0]
        
        try:
            # Extraemos los meshes de la escena actual
            mesh_data = parse_maya_ascii(full_input_path)
            
            # Guardamos los datos asociándolos al nombre de la escena
            all_scenes_database[scene_name_base] = mesh_data
            
            processed_count += 1
            print(f"[BATCH] ({processed_count}/{total_files}) Analizado con éxito: {file_name}")
            
        except Exception as e:
            print(f"[WARNING] Saltando archivo {file_name}: {e}")

    # -----------------------------------------------------------------
    # CAMBIO AQUÍ: Guardar todo en UN SOLO archivo JSON maestro
    # -----------------------------------------------------------------
    master_json_path = os.path.join(output_folder, "base_datos_escenas.json")
    with open(master_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(all_scenes_database, json_file, indent=4, ensure_ascii=False)
    
    print(f"\n[SUCCESS] ¡Proceso masivo terminado!")
    print(f"[INFO] Se generó UN SOLO archivo maestro con todas las mallas en: {master_json_path}")

    # Escritura del Reporte Consolidado de Auditoría (Sigue igual)
    report_path = os.path.join(output_folder, "auditoria_reporte.txt")
    with open(report_path, 'w', encoding='utf-8') as report_file:
        report_file.write("=== REPORTE DE AUDITORÍA DE PIPELINE (NODOS CORRUPTOS) ===\n")
        report_file.write(f"Total de archivos analizados: {total_files}\n")
        report_file.write(f"Total de anomalías detectadas: {len(CORRUPT_NODES_REPORT)}\n")
        report_file.write("-" * 60 + "\n\n")
        
        if CORRUPT_NODES_REPORT:
            for error in CORRUPT_NODES_REPORT:
                report_file.write(f"[ALERT] Archivo: {error['archivo']} | Línea: {error['linea']} -> {error['detalle']}\n")
            print(f"[ALERT] ¡Se encontraron {len(CORRUPT_NODES_REPORT)} nodos corruptos!")
        else:
            report_file.write("¡Felicidades! No se detectaron nodos 'unknown' en ninguna escena.\n")
            print("[SUCCESS] Todas las escenas están limpias.")
            
    print(f"[INFO] Reporte unificado de errores guardado en: {report_path}")


def main():
    parser = argparse.ArgumentParser(description="Parser optimizado y masivo de archivos Maya ASCII (.ma) a un solo JSON.")
    parser.add_argument('-i', '--input', required=True, help="Ruta de la carpeta contenedora con los archivos .ma.")
    parser.add_argument('-o', '--output', required=True, help="Ruta de la carpeta donde se guardarán los resultados.")
    
    args = parser.parse_args()
    process_batch(args.input, args.output)


if __name__ == '__main__':
    main()