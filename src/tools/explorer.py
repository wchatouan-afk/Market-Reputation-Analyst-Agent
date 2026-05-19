import os
import json

def list_python_files(directory_path="."):
    """Outil qui scanne le dossier et convertit les données en JSON structuré."""
    if not os.path.exists(directory_path):
        return json.dumps({"error": f"Le dossier '{directory_path}' n'existe pas."}, indent=2)
    
    try:
        files = [f for f in os.listdir(directory_path) if f.endswith('.py')]
        
        return json.dumps({
            "status": "success",
            "directory": os.path.abspath(directory_path),
            "files_found": files,
            "count": len(files)
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)