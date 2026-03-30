"""Module de définition des composants graphiques pour
 l'application de réglage de paramètres granulométriques."""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from src.core.engine import correct, inv_correct, calc_erreur, erreur_minim
from src.utils.importers import info_extract_courbe_numerique, importer_image_tk

PARAM_FILE_PATH = "mesure/params_correction.txt"

def _update_global_error(app):
    """Met à jour le calcul de l'erreur globale entre la courbe numérique et pratique."""
    if app.my_granulos.num.granulo and app.my_granulos.prat.granulo:
        err = calc_erreur(np.array(app.my_granulos.num.granulo["x_axis"]),
                          np.array(app.my_granulos.num.granulo["y_axis"]),
                          np.array(app.my_granulos.prat.granulo["x_axis"]),
                          np.array(app.my_granulos.prat.granulo["y_axis"]))
        app.erreur.set(str(err))
        app.flag_affiche_erreur.set(True)

class UneCourbeAffiche(tk.Frame):
    """Composant pour afficher une courbe dans la sidebar 
    avec son nom et une case à cocher pour l'affichage"""

    def __init__(self, parent, un_cumul, graphe, *args, **kwargs):
        super().__init__(parent, bg=parent["bg"], *args, **kwargs)
        self.un_cumul = un_cumul
        self.graphe = graphe
        self.un_cumul.show_courbe_elt.trace_add("write", self.affiche_elt_courbe)
        self._une_courbe_frame_gui()

    def _une_courbe_frame_gui(self):
        self.color_square = tk.Label(
            self, bg=self.un_cumul.color, width=2, relief="flat", state="disabled")
        self.label_check = ttk.Label(
            self, text=self.un_cumul.name, style="Sidebar.TLabel", state="disabled")
        self.check = ttk.Checkbutton(
            self, variable=self.un_cumul.flag_affichage,
            command=self.maj_cumul, style="Sidebar.TCheckbutton", state="disabled")
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
        self.columnconfigure(1, weight=1)
        ttk.Label(
            self, image=logo_ref,
            style="Sidebar.TLabel").grid(row=0, column=0, padx=5)
        ttk.Label(
            self, text=txt,
            style="Sidebar.TLabel").grid(row=0, column=1, sticky='w')
        ttk.Button(self,
                   image=self.tk_img_dl,
                   command=self._import,
                   style="Icon.TButton").grid(row=0, column=2, padx=5, sticky='e')

    def _import(self):
        if self.type == 'num':
            path = filedialog.askopenfilename(filetypes=[("ZIP", "*.zip")])
            if path:
                try:
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
                except Exception as e:
                    messagebox.showerror("Erreur d'import", f"Le fichier ZIP sélectionné est invalide ou illisible.\n\nDétails : {e}")
                    return
        else:
            path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx")])
            if path:
                try:
                    df = pd.read_excel(path)
                    self.app.my_granulos.prat.granulo = {
                        'x_axis': df.iloc[:,0].tolist(), 'y_axis': df.iloc[:,1].tolist()}
                    self.app.my_granulos.prat.show_courbe_elt.set(True)
                except Exception as e:
                    messagebox.showerror("Erreur d'import", f"Impossible de lire ce fichier Excel. Vérifiez qu'il n'est pas déjà ouvert.\n\nDétails : {e}")
                    return
        
        _update_global_error(self.app)
        self.graphe._maj_cumuls()


class BarreCorrectFrameNv(ttk.Frame):
    """Composant pour la saisie manuelle des nouveaux paramètres"""
    def __init__(self, parent, app, graphe, *args, **kwargs):
        super().__init__(parent, style="Sidebar.TFrame", *args, **kwargs)
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
            style="Sidebar.TLabel",
            font=("Segoe UI", 10, "bold")).grid(row=0, column=0, columnspan=3,
                                                pady=(5,10))
        # Scale
        ttk.Label(self, text="Scale:", style="Sidebar.TLabel").grid(row=1, column=0)
        self.ent_scale = ttk.Entry(
            self, textvariable=self.var_nv["scale"], width=8)
        self.ent_scale.grid(row=2, column=0, padx=5)
        # Offset
        ttk.Label(self, text="Offset:", style="Sidebar.TLabel").grid(row=1, column=1)
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
            _update_global_error(self.app)
            self.graphe._maj_cumuls()
        except ValueError:
            messagebox.showwarning("Format invalide", "Veuillez entrer des chiffres valides pour le Scale et l'Offset (ex: 1.25).", parent=self)

class CorrectFrame(ttk.Frame):
    """Conteneur global pour la zone de correction """
    def __init__(self, parent, app, graphe, *args, **kwargs):
        super().__init__(parent, style="Sidebar.TFrame", *args, **kwargs)
        self.app = app
        self.graphe = graphe
        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Correction", style="Sidebar.Title.TLabel").pack(pady=(0, 10))
        # Section Erreur et Auto
        auto_f = ttk.Frame(self, style="Sidebar.TFrame")
        auto_f.pack(fill="x", pady=5)
        ttk.Label(auto_f, text="Erreur :", style="Sidebar.TLabel").pack(side="left")
        ttk.Label(
            auto_f,
            textvariable=self.app.erreur,
            style="Sidebar.TLabel",
            font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
        self.btn_auto = ttk.Button(auto_f, text="Auto-Ajuster", command=self._auto)
        self.btn_auto.pack(side="right")
        # Séparateur
        ttk.Separator(self, orient='horizontal').pack(fill='x', pady=10)
        # Section Manuelle
        self.manual_f = BarreCorrectFrameNv(self, self.app, self.graphe)
        self.manual_f.pack(fill="x")
        # Bouton Sauvegarde
        self.btn_save = ttk.Button(self, text="Sauvegarder Paramètres", command=self._save_params)
        self.btn_save.config(state="disabled")
        self.btn_save.pack(fill="x", pady=(15, 5))
        
        # Label confirmation sauvegarde
        self.lbl_save_info = ttk.Label(self, text="", style="Sidebar.TLabel", justify="center")
        self.lbl_save_info.pack(pady=5)
        
        # Charge les paramètres si existants
        self._load_saved_params()
        
        # Traces pour l'état des boutons
        self.app.flag_affiche_erreur.trace_add("write", self._toggle_buttons)

    def _toggle_buttons(self, *args):
        state = "normal" if self.app.flag_affiche_erreur.get() else "disabled"
        self.btn_auto.config(state=state)
        self.btn_save.config(state=state)

    def _auto(self):
        orig = self.app.my_granulos.originale.granulo
        prat = self.app.my_granulos.prat.granulo
        
        # Vérification indispensable avant de lancer les calculs
        if orig is None or prat is None:
            messagebox.showwarning("Importation requise", "Veuillez d'abord importer la courbe numérique et la courbe réelle avant de lancer l'auto-ajustement.", parent=self)
            return
            
        try:
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
            _update_global_error(self.app)
            self.graphe._maj_cumuls()
        except Exception as e:
            messagebox.showerror("Échec de l'optimisation", f"L'algorithme de calcul n'a pas pu faire converger les deux courbes.\n\nDétails : {e}", parent=self)

    def _save_params(self):
        try:
            scale_val = self.app.var_correct["var_nv"]["scale"].get()
            offset_val = self.app.var_correct["var_nv"]["offset"].get()
            
            # Validation avant sauvegarde
            try:
                float(scale_val)
                float(offset_val)
            except ValueError:
                messagebox.showwarning("Format invalide", "Valeurs de Scale ou Offset incorrectes. entrez une valeur de type int ou float.", parent=self)
                return

            os.makedirs(os.path.dirname(PARAM_FILE_PATH), exist_ok=True)
            
            with open(PARAM_FILE_PATH, "w", encoding="utf-8") as f:
                f.write(f"Scale = {scale_val}\nOffset = {offset_val}\n")
                
            self.lbl_save_info.config(
                text=f" Nouveaux paramètres sauvegardés\nScale: {scale_val}  |  Offset: {offset_val}",
                foreground="#FFFFFF" 
            )
        except Exception as e:
            self.lbl_save_info.config(text=f"Erreur de sauvegarde", foreground="#E74C3C")

    def _load_saved_params(self):
        if os.path.exists(PARAM_FILE_PATH):
            try:
                with open(PARAM_FILE_PATH, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                scale_val, offset_val = "1.0", "0.0"
                for line in lines:
                    if line.startswith("Scale"):
                        scale_val = line.split("=")[1].strip()
                    elif line.startswith("Offset"):
                        offset_val = line.split("=")[1].strip()
                self.lbl_save_info.config(
                    text=f"Derniers paramètres sauvegardés:\nScale: {scale_val}  |  Offset: {offset_val}",
                    foreground="#BDC3C7" # Grisé clair
                )
            except Exception:
                pass
