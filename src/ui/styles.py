# Fichier : src/ui/styles.py
from tkinter import ttk

class StyleManager:
    """Classe pour gérer les styles de l'application."""
    BG_MAIN = "#F5F6FA"
    BG_SIDEBAR = "#FFFFFF"
    PRIMARY = "#2C3E50"
    ACCENT = "#3498DB" 
    TEXT = "#2F3640"
    BORDER = "#DCDDE1"

    def __init__(self, root):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._configure_styles()
        root.configure(bg=self.BG_MAIN)

    def _configure_styles(self):
        self.style.configure("TFrame", background=self.BG_MAIN)
        self.style.configure("Sidebar.TFrame", background=self.BG_SIDEBAR, relief="flat")
        self.style.configure("TLabel", background=self.BG_MAIN, foreground=self.TEXT, font=("Segoe UI", 10))
        self.style.configure("Title.TLabel", font=("Segoe UI", 12, "bold"), foreground=self.PRIMARY)

        
        self.style.configure("TButton", font=("Segoe UI", 9, "bold"))
        self.style.map("TButton", 
                       background=[('active', self.ACCENT), ('!disabled', self.PRIMARY)], 
                       foreground=[('!disabled', 'white')])

       
        # On configure le bouton pour qu'il ait le même fond que la sidebar (Blanc)
        self.style.configure("Icon.TButton", 
                             background=self.BG_SIDEBAR,
                             borderwidth=0, 
                             relief="flat",
                             focuscolor="none", 
                             padding=0) 

        # On configure l'effet au survol
        self.style.map("Icon.TButton", 
                       background=[('active', "#F0F0F0"), ('!disabled', self.BG_SIDEBAR)],
                       relief=[('pressed', 'flat')]) 
        # ------------------------------------------------------------------