import json
from tools.explorer import list_python_files

class AutoDocAgent:
    def __init__(self, target_dir="."):
        self.target_dir = target_dir
        self.context_memory = {}

    def run_react_loop(self):
        print(f"[Agent] Input reçu : Analyse du dossier '{self.target_dir}'")
        
        print("[Agent] Thought: Je dois cartographier le projet. J'ai besoin de lister les fichiers Python présents.")
        
        print("[Agent] Action: Appel de l'outil 'list_python_files'.")
        tool_output_json = list_python_files(self.target_dir)
        
        print("[Agent] Observation: Réception des données converties.")
        data = json.loads(tool_output_json)
        
        if data.get("status") == "success":
            self.context_memory["files"] = data["files_found"]
            print(f"[Agent] Mmoire mise à jour. {data['count']} fichier(s) détecté(s).")
            
            print("[Agent] Thought: Analyse complétée. Génération du rapport de sortie.")
            self.generate_documentation_manifest()
        else:
            print(f"[Agent] Erreur rencontrée : {data.get('error')}")

    def generate_documentation_manifest(self):
        manifest_path = "DOCUMENTATION_MANIFEST.json"
        output_data = {
            "project_architecture": "Modular Python CLI",
            "detected_modules": self.context_memory.get("files", []),
            "status": "Validated for documentation"
        }
        with open(manifest_path, "w") as f:
            json.dump(output_data, f, indent=4)
        print(f"[Agent] Succès : Sortie générée dans '{manifest_path}'")