# 🎬 Maya ASCII (.ma) to JSON Pipeline Parser

![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.11-blue?style=for-the-badge&logo=python)
![Pipeline Status](https://img.shields.io/badge/pipeline-passing-brightgreen?style=for-the-badge)
![DCC Dependency](https://img.shields.io/badge/DCC%20Dependency-None-orange?style=for-the-badge)

Un parser de alto rendimiento diseñado para entornos de Technical Art y Pipeline de CGI/Videojuegos. Esta herramienta permite auditar y extraer metadatos de escenas de Maya en formato ASCII (.ma) a velocidad de software puro, de forma masiva y sin necesidad de abrir o depender de licencias de Autodesk Maya.

---

## 💡 ¿Por qué esto importa?

En un pipeline de producción a gran escala (como auditorías nocturnas o flujos de integración continua), abrir cientos de archivos dentro de Maya para validar contenido es inviable por el tiempo de carga del DCC. 

Este script soluciona el problema procesando los archivos como texto plano (Stream I/O) utilizando Expresiones Regulares (RegEx). Esto permite:
* Validación de Render Farms: Detectar texturas rotas o rutas absolutas antes de gastar presupuesto en la granja.
* Pre-commit Hooks (Git): Bloquear archivos corruptos o con namespaces sucios antes de que entren al servidor.
* Migración de Assets: Extraer jerarquías y nombres de mallas en segundos para catalogación de proyectos viejos.

---

## 📦 Estructura del Repositorio

├── ma_to_json.py          # Herramienta principal CLI (Batch Parser & Auditoría)
├── test_parser.py         # Suite de pruebas unitarias automatizadas (Pytest)
└── README.md              # Documentación técnica del proyecto

---

## 🚀 Instalación y Requisitos

El script utiliza librerías nativas de Python (re, json, argparse, os). Solo requieres instalar pytest si deseas ejecutar la suite de pruebas de control de calidad.

1. Clona este repositorio en tu estación de trabajo.

2. Instala la dependencia de testing:
   pip install pytest

---

## 🛠️ Guía de Uso (CLI)

El script cuenta con una interfaz de línea de comandos robusta armada con argparse. Para ejecutar el procesamiento masivo (Batch) de tus carpetas de escenas, utiliza los flags --input (directorio origen) y --output (directorio destino):

python ma_to_json.py --input "./tus_escenas_maya" --output "./reportes_json"

### 📄 Ejemplo de Output Estructurado (.json)
Cada archivo .ma procesado generará un archivo homónimo <nombre_escena>_meshes.json con la siguiente estructura limpia de diccionarios:

[
    {
        "name": "hero_sword_0_geo",
        "parent": "character_GRP",
        "attrs": [
            "rename -uid \"8492-ABC-51\";",
            "setAttr -k off \".v\";",
            "setAttr \".io\" yes;"
        ]
    }
]

### 🔍 Reporte Automatizado de Auditoría
Además de los archivos JSON individuales, el pipeline genera un archivo consolidado de texto llamado auditoria_reporte.txt en la carpeta de salida. Este archivo actúa como un log rápido para detectar anomalías de un solo vistazo:

=== REPORTE DE AUDITORÍA DE PIPELINE (NODOS CORRUPTOS) ===
Total de archivos analizados: 800
Total de anomalías detectadas: 2
------------------------------------------------------------

[ALERT] Archivo: prop_lamp_v02.ma | Línea: 14520 -> Nodo 'unknown' detectado (Plugin faltante o escena rota)
[ALERT] Archivo: character_boss_v09.ma | Línea: 902340 -> Nodo 'unknown' detectado (Plugin faltante o escena rota)

---

## 🧪 Suite de Pruebas Unitarias

Para garantizar la estabilidad de las expresiones regulares y el correcto aislamiento de excepciones y errores del sistema operativo, ejecuta la suite de pytest:

pytest test_parser.py

### 📋 Cobertura de Tests Integrados:
* test_parse_valid_mesh: Verifica la captura exacta de jerarquías padre-hijo y el aislamiento de atributos identados.
* test_file_not_found: Asegura el correcto manejo de errores en caso de rutas inválidas o inexistentes.
* test_invalid_extension: Bloquea la ingesta de formatos binarios no soportados (.mb), protegiendo la ejecución del pipeline.
