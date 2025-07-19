import sys
from pathlib import Path

def resource_path(relative_path):
    """Devuelve la ruta absoluta a un recurso, compatible con desarrollo y PyInstaller"""
    try:
        # Para ejecutables empaquetados con PyInstaller
        base_path = Path(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else Path(__file__).parent.parent
        
        # Construye la ruta completa
        full_path = base_path / relative_path
        
        # Verifica si el archivo existe
        if not full_path.exists():
            raise FileNotFoundError(f"No se encontró el recurso: {full_path}")
            
        return str(full_path)
    except Exception as e:
        print(f"Error en resource_path: {e}")
        return str(Path(__file__).parent.parent / relative_path)
