#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest
from ma_to_json import parse_maya_ascii

# TEST 1: Validar que extrae correctamente un nodo mesh con atributos
def test_parse_valid_mesh(tmp_path):
    # Creamos un archivo .ma virtual/temporal en el disco
    test_file = tmp_path / "scene_test.ma"
    content = (
        "createNode mesh -n \"hero_sword_geo\" -p \"char_GRP\";\n"
        "    setAttr \"_uid\" \"1234\";\n"
        "    setAttr \".io\" yes;\n"
        "createNode lambert -n \"mat_sword\";\n" # Este nodo no es mesh, debe ignorarse
    )
    test_file.write_text(content, encoding="utf-8")
    
    # Ejecutamos el parser sobre el archivo de prueba
    result = parse_maya_ascii(str(test_file))
    
    # Aserciones (Verificaciones del test)
    assert len(result) == 1
    assert result[0]["name"] == "hero_sword_geo"
    assert result[0]["parent"] == "char_GRP"
    assert "setAttr \".io\" yes;" in result[0]["attrs"]

# TEST 2: Validar el manejo de errores si el archivo no existe
def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        parse_maya_ascii("ruta_fantasma_que_no_existe.ma")

# TEST 3: Validar el manejo de errores si la extensión no es .ma
def test_invalid_extension(tmp_path):
    bad_file = tmp_path / "invalid_scene.mb" # Extensión binaria .mb no soportada
    bad_file.write_text("content", encoding="utf-8")
    
    with pytest.raises(ValueError):
        parse_maya_ascii(str(bad_file))