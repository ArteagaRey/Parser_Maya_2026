# 🎬 Automatización en Maya: Extractor de Datos a JSON (.ma a JSON)

![Estado](https://img.shields.io/badge/Proyecto-Completado-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/Hecho%20con-Python%203-blue?style=for-the-badge)

¡Hola! Este proyecto es una herramienta en Python diseñada para escanear archivos de Maya (`.ma`) a máxima velocidad, extraer la información de sus mallas (meshes) y guardarla en archivos ordenados de formato JSON. 

Lo mejor de todo: **funciona fuera de Maya**, lo que significa que puedes revisar cientos de escenas sin tener que abrir el programa, ahorrando horas de trabajo.

---

## 💡 ¿Para qué sirve esta herramienta?

Imagínate que estás en un estudio de animación o videojuegos y te dan **800 escenas de Maya**, pero te dicen que algunas tienen errores o carpetas rotas. Abrir los 800 archivos a mano en Maya para buscar el problema tomaría días y congelaría tu computadora.

Este script lee los archivos como si fueran un bloc de notas gigante, busca la información en segundos y te genera:
1. Un archivo **JSON** por cada escena con la lista de mallas, quién es su "padre" en la jerarquía y sus atributos.
2. Un **Reporte de Alertas (`auditoria_reporte.txt`)** que te dice exactamente qué archivos están corruptos o rotos y en qué línea está el fallo. ¡Así solo abres en Maya los archivos que de verdad necesitan reparación!

---

## 📦 Carpetas del Proyecto

├── ma_to_json.py          # El script principal que procesa los archivos y busca errores.
├── test_parser.py         # Un script de pruebas para verificar que todo funcione bien.
└── README.md              # Este archivo de instrucciones.

---

## 🚀 Cómo instalarlo

No necesitas instalar programas complejos. Solo asegúrate de tener Python en tu computadora.

Si quieres correr las pruebas de seguridad, abre tu terminal (consola de comandos) e instala esta herramienta de ayuda:
```bash
pip install pytest
```

---

## 🛠️ Cómo se usa (Paso a Paso)
Para poner a trabajar el script con tus archivos, abre la terminal de tu computadora y usa el siguiente comando. Solo debes indicarle dónde están tus escenas de Maya (--input) y dónde quieres guardar los resultados (--output):
```
python ma_to_json.py --input "./mis_escenas_maya" --output "./resultados_json"
```
---

## 📄 ¿Qué resultado obtienes?
En tu carpeta de resultados verás archivos que se ven así de limpios y ordenados:
<img width="970" height="1074" alt="image" src="https://github.com/user-attachments/assets/0fbafe7f-4f19-4066-99a7-0ce6679f5c83" />

---

## 🔍 Tu Reporte de Errores Listo
Al finalizar, el script te dejará un archivo de texto llamado auditoria_reporte.txt. Al abrirlo, verás un resumen directo como este:
<img width="1271" height="232" alt="image" src="https://github.com/user-attachments/assets/0f116888-f83f-42c6-a06a-0b77167c0971" />

## 🧪 Pruebas de Seguridad (Opcional)
Para estar 100% seguro de que el script hace su trabajo correctamente y no se va a trabar con archivos inexistentes o extensiones equivocadas, ejecuta este comando en tu terminal:
```bash
pytest test_parser.py
```
