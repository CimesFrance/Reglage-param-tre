"""Module de définition des modèles de données pour l'application
 de réglage de paramètres granulométriques.
Ce module contient les classes de données utilisées pour stocker les informations 
sur les cumuls granulométriques, ainsi que l'état global de l'application."""

import tkinter as tk
from src.utils.importers import importer_image_tk

class cumul:
    """Modèle de données pour un cumul granulométrique unique"""
    def __init__(self, Name, Color, granulo=None, logo=None):
        self.Name = Name
        self.Color = Color
        self.granulo = granulo
        self.logo = logo
        self.flag_affichage = tk.IntVar(value=0)
        self.show_courbe_elt = tk.BooleanVar(value=False)

class mes_cumuls:
    """Conteneur pour les trois types de courbes de l'application"""
    def __init__(self):
        self.num = cumul(Name="Courbe numérique corrigée", Color='#E74C3C', logo=importer_image_tk("photo camera.png"))
        self.originale = cumul(Name="Courbe numérique originale", Color='#34495E')
        self.prat = cumul(Name="Courbe réelle tamisée", Color='#27AE60', logo=importer_image_tk("logo tamis.png"))

class AppState:
    """Gestionnaire d'état global partagé entre les vues"""
    def __init__(self):
        self.my_granulos = mes_cumuls()
        self.var_correct = {
            "var_act": {"scale": tk.StringVar(value="1.00"), "offset": tk.StringVar(value="0.00")},
            "var_nv": {"scale": tk.StringVar(value="1.00"), "offset": tk.StringVar(value="0.00")}
        }
        self.erreur = tk.StringVar(value="0.00")
        self.show_correct_frame_act = tk.BooleanVar(value=False)
        self.flag_affiche_erreur = tk.BooleanVar(value=False)
        self.show_param_nv = tk.BooleanVar(value=False)
        self.flag_affiche_btn_sauvegarde = tk.BooleanVar(value=False)