"""Module de gestion de l'affichage du graphique de granulométrie dans l'application.
Ce module contient la classe graphe, qui est responsable de l'affichage et de la mise 
à jour du graphique de granulométrie en fonction des données fournies par l'état global de l'application."""

import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class graphe(tk.Frame):
    """Classe pour afficher le graphique de granulométrie dans la partie droite de l'application."""
    def __init__(self, parent, app, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.fig = Figure(figsize=(6, 5), dpi=100, facecolor="#F5F6FA")
        self.ax = self.fig.add_subplot(111)
        self.canvas_my_graph = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_my_graph.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self._maj_cumuls()

    def _maj_cumuls(self):
        """Met à jour le graphique de granulométrie en fonction des données actuelles de l'application."""
        self.ax.cla()
        self.ax.set_title("Analyse Granulométrique", fontsize=12, fontweight='bold', pad=15)
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.set_xlabel("Ouverture des tamis (mm)", fontsize=10, fontweight='medium')
        self.ax.set_ylabel("Quantité cumulée (%)", fontsize=10, fontweight='medium')
        
        
        m_gran = self.app.my_granulos
        dict_infos = {
            "num": {"flag": m_gran.num.flag_affichage.get(), "courbe": m_gran.num.granulo, "name": m_gran.num.Name, "color": m_gran.num.Color},
            "orig": {"flag": m_gran.originale.flag_affichage.get(), "courbe": m_gran.originale.granulo, "name": m_gran.originale.Name, "color": m_gran.originale.Color},
            "prat": {"flag": m_gran.prat.flag_affichage.get(), "courbe": m_gran.prat.granulo, "name": m_gran.prat.Name, "color": m_gran.prat.Color}
        }

        for info in dict_infos.values():
            if info["flag"] == 1 and info["courbe"] is not None:
                self.ax.plot(info["courbe"]["x_axis"], info["courbe"]["y_axis"], label=info["name"], color=info["color"], linewidth=2)
        
        self.ax.set_xlim(0, 90)
        self.ax.set_ylim(0, 110)
        if self.ax.get_legend_handles_labels()[0]:
            self.ax.legend(loc='lower right', fontsize=8)
        self.canvas_my_graph.draw()