"""Module d'importation de ressources pour l'application.
Gestion des fichiers externes et des images."""

import os
import zipfile
import pandas as pd
from PIL import Image, ImageTk

def importer_image_tk(nom_image, w=24, h=24):
    """Charge une image depuis le dossier assets et la convertit en PhotoImage pour Tkinter."""
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(base_path, "assets", "icons", nom_image)
    try:
        img = Image.open(path).resize((w, h), Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Erreur lors du chargement de l'image {nom_image} : {e}")
        return None

def info_extract_courbe_numerique(zip_file):
    """Extrait les données de la courbe numérique et les 
    paramètres de correction depuis un fichier zip."""
    with zipfile.ZipFile(zip_file, "r") as z:
        with z.open("data.csv") as f:
            df = pd.read_csv(f)
        with z.open("params_correction.txt") as f:
            texte = f.read().decode("utf-8")
    vars_dict = {}
    for ligne in texte.splitlines():
        if "=" in ligne:
            k, v = ligne.split("=")
            try: vars_dict[k.strip()] = float(v.strip())
            except: vars_dict[k.strip()] = v.strip()
    return {"tamis": df.iloc[:,0].tolist(), "cumul": df.iloc[:,1].tolist()}, vars_dict
