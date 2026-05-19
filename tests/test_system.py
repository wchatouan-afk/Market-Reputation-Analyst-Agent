import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from tools.explorer import list_python_files
from agent.manager import AutoDocAgent

def test_tool_explorer_valid():
    """Scénario 1: Test de l'outil de scan sur le dossier courant (doit trouver des fichiers)"""
    result_json = list_python_files(".")
    data = json.loads(result_json)
    assert data["status"] == "success"
    assert "files_found" in data

def test_agent_execution_creates_manifest():
    """Scénario 2: Test du flux complet de l'agent (génération du fichier manifeste)"""
    agent = AutoDocAgent(target_dir=".")
    agent.run_react_loop()
    
    
    assert os.path.exists("DOCUMENTATION_MANIFEST.json")
    
    if os.path.exists("DOCUMENTATION_MANIFEST.json"):
        os.remove("DOCUMENTATION_MANIFEST.json")