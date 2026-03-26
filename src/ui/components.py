"""Module de définition des composants graphiques pour
 l'application de réglage de paramètres granulométriques."""

import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from src.core.engine import correct, inv_correct, calc_erreur, erreur_minim
from src.utils.importers import info_extract_courbe_numerique, importer_image_tk

class UneCourbeAffiche(tk.Frame):
    """Composant pour afficher une courbe dans la sidebar 
    avec son nom et une case à cocher pour l'affichage"""

    def __init__(self, parent, un_cumul, graphe, *args, **kwargs):
        super().__init__(parent, bg="white", *args, **kwargs)
        self.un_cumul = un_cumul
        self.graphe = graphe
        self.un_cumul.show_courbe_elt.trace_add("write", self.affiche_elt_courbe)
        self._une_courbe_frame_gui()

    def _une_courbe_frame_gui(self):
        self.color_square = tk.Label(
            self, bg=self.un_cumul.color, width=2, relief="flat", state="disabled")
        self.label_check = ttk.Label(
            self, text=self.un_cumul.name, state="disabled")
        self.check = ttk.Checkbutton(
            self, variable=self.un_cumul.flag_affichage,
            command=self.maj_cumul, state="disabled")
        self.color_square.pack(side="left", padx=5, pady=2)
        self.label_check.pack(side="left", padx=5, expand=True, fill="x")
        self.check.pack(side="right", padx=5)

    def affiche_elt_courbe(self, *args):
        """Active ou désactive les éléments de la courbe selon l'état de la case à cocher"""
        etat = "normal" if self.un_cumul.show_courbe_elt.get() else "disabled"
        self.color_square.config(state=etat)
        self.label_check.config(state=etat)
        self.check.config(state=etat)

    def maj_cumul(self):
        """Met à jour les cumulatives dans le graphe lorsque l'affichage est modifié"""
        self.graphe._maj_cumuls()

class ImportGranuloFrame(ttk.Frame):
    """Composant pour l'importation de courbes
      granulométriques numériques ou réelles"""
    def __init__(self, parent, app, graphe, type_import, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app, self.graphe, self.type = app, graphe, type_import
        # On force le fond de la frame d'import à blanc
        self.config(style="Sidebar.TFrame")
        self.tk_img_dl = importer_image_tk("logodownload.png")
        self._setup()

    def _setup(self):
        logo_ref = self.app.my_granulos.num.logo if self.type == 'num' else self.app.my_granulos.prat.logo
        txt = "Importer Courbe Numérique" if self.type == 'num' else "Importer Courbe Réelle"
        # Ajout explicite du style Sidebar
        ttk.Label(
            self, image=logo_ref,
            style="Sidebar.TLabel").grid(row=0, column=0, padx=5)
        ttk.Label(
            self, text=txt,
            style="Sidebar.TLabel").grid(row=0, column=1, sticky='w')
        ttk.Button(self,
                   image=self.tk_img_dl,
                   command=self._import,
                   style="Icon.TButton").grid(row=0, column=2, padx=5)

    def _import(self):
        if self.type == 'num':
            path = filedialog.askopenfilename(filetypes=[("ZIP", "*.zip")])
            if path:
                granulo, c_var = info_extract_courbe_numerique(path)
                self.app.my_granulos.num.granulo = {
                    'x_axis': granulo["tamis"], 'y_axis': granulo["cumul"]}
                self.app.var_correct["var_act"]["scale"].set(str(c_var["Scale"]))
                self.app.var_correct["var_act"]["offset"].set(str(c_var["Offset"]))
                inv_x = inv_correct(granulo["tamis"], c_var["Scale"], c_var["Offset"])
                self.app.my_granulos.originale.granulo = {
                    "x_axis": inv_x, "y_axis": granulo["cumul"]}
                self.app.show_correct_frame_act.set(True)
                self.app.my_granulos.num.show_courbe_elt.set(True)
                self.app.my_granulos.originale.show_courbe_elt.set(True)
                self.app.show_param_nv.set(True)
                self.app.flag_affiche_btn_sauvegarde.set(True)
        else:
            path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
            if path:
                df = pd.read_excel(path)
                self.app.my_granulos.prat.granulo = {
                    'x_axis': df.iloc[:,0].tolist(), 'y_axis': df.iloc[:,1].tolist()}
                self.app.my_granulos.prat.show_courbe_elt.set(True)
        if self.app.my_granulos.num.granulo and self.app.my_granulos.prat.granulo:
            err = calc_erreur(np.array(self.app.my_granulos.num.granulo["x_axis"]),
                             np.array(self.app.my_granulos.num.granulo["y_axis"]),
                             np.array(self.app.my_granulos.prat.granulo["x_axis"]),
                             np.array(self.app.my_granulos.prat.granulo["y_axis"]))
            self.app.erreur.set(str(err))
            self.app.flag_affiche_erreur.set(True)
        self.graphe._maj_cumuls()


class BarreCorrectFrameNv(ttk.Frame):
    """Composant pour la saisie manuelle des nouveaux paramètres"""
    def __init__(self, parent, app, graphe, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.graphe = graphe
        self.var_nv = app.var_correct['var_nv']
        # Trace pour activer/désactiver les champs
        self.app.show_param_nv.trace_add("write", self._update_state)
        self._build_ui()

    def _build_ui(self):
        ttk.Label(
            self,
            text="Paramètres manuels",
            font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=3,
                                                pady=(5,10))
        # Scale
        ttk.Label(self, text="Scale:").grid(row=1, column=0)
        self.ent_scale = ttk.Entry(
            self, textvariable=self.var_nv["scale"], width=8)
        self.ent_scale.grid(row=2, column=0, padx=5)
        # Offset
        ttk.Label(self, text="Offset:").grid(row=1, column=1)
        self.ent_offset = ttk.Entry(self, textvariable=self.var_nv["offset"], width=8)
        self.ent_offset.grid(row=2, column=1, padx=5)
        # Bouton Valider
        self.btn_valider = ttk.Button(self, text="Appliquer", command=self._validate_change)
        self.btn_valider.grid(row=2, column=2, padx=5)
        self._update_state()

    def _update_state(self, *args):
        state = "normal" if self.app.show_param_nv.get() else "disabled"
        self.ent_scale.config(state=state)
        self.ent_offset.config(state=state)
        self.btn_valider.config(state=state)

    def _validate_change(self):
        try:
            scale = float(self.var_nv["scale"].get())
            offset = float(self.var_nv["offset"].get())
            # Sécurité scale
            if scale <= 0: scale = 0.001
            orig = self.app.my_granulos.originale.granulo
            prat = self.app.my_granulos.prat.granulo
            # Mise à jour de la courbe numérique
            self.app.my_granulos.num.granulo["x_axis"] = correct(
                orig["x_axis"], scale, offset)
            # Recalcul de l'erreur
            if prat:
                err = calc_erreur(np.array(self.app.my_granulos.num.granulo["x_axis"]),
                                 np.array(self.app.my_granulos.num.granulo["y_axis"]),
                                 np.array(prat["x_axis"]), np.array(prat["y_axis"]))
                self.app.erreur.set(str(err))
            self.graphe._maj_cumuls()
        except ValueError:
            print("Erreur : Valeurs de scale/offset invalides")

class CorrectFrame(ttk.Frame):
    """Conteneur global pour la zone de correction """
    def __init__(self, parent, app, graphe, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.app = app
        self.graphe = graphe
        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Correction", style="Title.TLabel").pack(pady=(0, 10))
        # Section Erreur et Auto
        auto_f = ttk.Frame(self)
        auto_f.pack(fill="x", pady=5)
        ttk.Label(auto_f, text="Erreur :").pack(side="left")
        ttk.Label(
            auto_f,
            textvariable=self.app.erreur,
            font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
        self.btn_auto = ttk.Button(auto_f, text="Auto-Ajuster", command=self._auto)
        self.btn_auto.pack(side="right")
        # Séparateur
        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=10)
        # Section Manuelle
        self.manual_f = BarreCorrectFrameNv(self, self.app, self.graphe)
        self.manual_f.pack(fill="x")
        # Bouton Sauvegarde
        self.btn_save = ttk.Button(self, text="Sauvegarder Paramètres", state="disabled")
        self.btn_save.pack(fill="x", pady=15)
        # Traces pour l'état des boutons
        self.app.flag_affiche_erreur.trace_add("write", self._toggle_buttons)

    def _toggle_buttons(self, *args):
        state = "normal" if self.app.flag_affiche_erreur.get() else "disabled"
        self.btn_auto.config(state=state)
        self.btn_save.config(state=state)

    def _auto(self):
        orig = self.app.my_granulos.originale.granulo
        prat = self.app.my_granulos.prat.granulo
        res = minimize(erreur_minim, [1.0, 0.0],
                       args=(np.array(orig["x_axis"]), np.array(orig["y_axis"]),
                             np.array(prat["x_axis"]), np.array(prat["y_axis"])),
                       bounds=[(1e-6, None), (None, None)])
        s, o = res.x
        self.app.var_correct["var_nv"]["scale"].set(str(round(s, 3)))
        self.app.var_correct["var_nv"]["offset"].set(str(round(o, 3)))
        # Appliquer le résultat
        self.app.my_granulos.num.granulo["x_axis"] = correct(orig["x_axis"], s, o)
        # Recalcul erreur
        err = calc_erreur(np.array(self.app.my_granulos.num.granulo["x_axis"]),
                         np.array(self.app.my_granulos.num.granulo["y_axis"]),
                         np.array(prat["x_axis"]), np.array(prat["y_axis"]))
        self.app.erreur.set(str(err))
        self.graphe._maj_cumuls()
