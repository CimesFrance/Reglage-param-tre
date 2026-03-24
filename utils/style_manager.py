import tkinter as tk
from tkinter import ttk

class StyleManager:
    # Palette de couleurs "Professionnelle & Minimaliste"
    BG_MAIN = "#F8F9FA"       # Gris très clair pour le fond
    BG_SIDEBAR = "#FFFFFF"   # Blanc pour les panneaux latéraux
    PRIMARY = "#2C3E50"      # Bleu nuit (Texte et titres)
    ACCENT = "#3498DB"       # Bleu clair (Boutons et actions)
    SUCCESS = "#27AE60"      # Vert (Validation)
    BORDER = "#DCDDE1"       # Gris clair pour les bordures
    TEXT = "#2F3640"         # Anthracite pour la lecture

    def __init__(self, root):
        self.style = ttk.Style()
        # Utilisation d'un thème de base moderne si disponible
        if "clam" in self.style.theme_names():
            self.style.theme_use("clam")

        self._configure_styles()

    def _configure_styles(self):
        # Configuration globale des Frames
        self.style.configure("TFrame", background=self.BG_MAIN)
        self.style.configure("Sidebar.TFrame", background=self.BG_SIDEBAR, relief="flat")

        # Configuration des Labels
        self.style.configure("TLabel", 
                             background=self.BG_MAIN, 
                             foreground=self.TEXT, 
                             font=("Segoe UI", 10))
        
        self.style.configure("Title.TLabel", 
                             font=("Segoe UI", 12, "bold"), 
                             foreground=self.PRIMARY)

        # Configuration des Boutons (Modern Flat)
        self.style.configure("TButton", 
                             font=("Segoe UI", 10, "bold"), 
                             borderwidth=0, 
                             focuscolor="none")
        
        self.style.map("TButton",
                       background=[('active', self.ACCENT), ('!disabled', self.PRIMARY)],
                       foreground=[('!disabled', 'white')])

        # Configuration des Entrées (Entry)
        self.style.configure("TEntry", 
                             fieldbackground="white", 
                             bordercolor=self.BORDER, 
                             lightcolor=self.BORDER, 
                             darkcolor=self.BORDER)

        # Style spécifique pour le bouton de sauvegarde
        self.style.configure("Success.TButton", background=self.SUCCESS)
        self.style.map("Success.TButton", background=[('active', "#219150")])

    def apply_to_root(self, root):
        root.configure(bg=self.BG_MAIN)