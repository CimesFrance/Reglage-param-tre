"""Module principal de l'application de réglage de paramètres granulométriques."""

import tkinter as tk
from src.ui.styles import StyleManager
from src.ui.graph import graphe
from src.ui.components import import_granulo_frame, une_courbe_affiche, correct_frame
from src.core.models import AppState
from src.utils.importers import importer_image_tk

class CIMESApp(tk.Tk):
    """Creation de la fenetre qui contient la fenetre principale."""
    def __init__(self):
        super().__init__()
        self.title("CIMES - Correction Granulométrique")
        self.geometry("1100x800")
        
        self.state = AppState()
        self.style_manager = StyleManager(self)
        
        self._build_layout()

    def _build_layout(self):
        # Sidebar
        sidebar = tk.Frame(self, width=350, bg="white", padx=15, pady=15)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Graph
        self.graph_view = graphe(self, self.state)
        self.graph_view.pack(side="right", fill="both", expand=True)

        self.logo_entreprise_side = importer_image_tk("cimes-logo.png", w=250, h=100)
        
        if self.logo_entreprise_side:
            lbl_logo = tk.Label(sidebar, image=self.logo_entreprise_side, bg="white")
            lbl_logo.pack(side="bottom", pady=(20, 0)) 
       
        # Components in Sidebar
        # Importation
        tk.Label(sidebar, text="Importation", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w", pady=(0,10))
        import_granulo_frame(sidebar, self.state, self.graph_view, 'num').pack(fill="x", pady=5)
        import_granulo_frame(sidebar, self.state, self.graph_view, 'tamis').pack(fill="x", pady=5)
        
        tk.Frame(sidebar, height=1, bg="#DCDDE1").pack(fill="x", pady=15)
        
        # Gestion des courbes
        tk.Label(sidebar, text="Gestion des Courbes", font=("Segoe UI", 12, "bold"), bg="white").pack(anchor="w", pady=(0,10))
        une_courbe_affiche(sidebar, self.state.my_granulos.num, self.graph_view).pack(fill="x")
        une_courbe_affiche(sidebar, self.state.my_granulos.originale, self.graph_view).pack(fill="x")
        une_courbe_affiche(sidebar, self.state.my_granulos.prat, self.graph_view).pack(fill="x")

        tk.Frame(sidebar, height=1, bg="#DCDDE1").pack(fill="x", pady=15)
        # Correction
        correct_frame(sidebar, self.state, self.graph_view).pack(fill="x")