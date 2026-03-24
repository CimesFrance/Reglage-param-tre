import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy.optimize import minimize
from scipy.interpolate import interp1d
import copy

from utils.import_manager import importer_image_tk,info_extract_courbe_numerique
from utils.correction_manager import inv_correct,correct,erreur,erreur_minim


class Utils:
    @staticmethod
   
    # def inv_correct(tamis_act,scale_act,offset_act):
    #     """Retorune l'axe des x de la courbe originale selon les paramètres de correction actuels"""
    #     return list((np.array(tamis_act)-offset_act) / scale_act)
    
    # def correct(tamis_act,scale_nv,offset_nv):
    #     """Retorune l'axe des x de la courbe originale modifiée selon les nouveaux paramètres de correction"""
    #     return list(np.array(tamis_act)*scale_nv+offset_nv)
    

    # def erreur(tamis_corrigee,cumulatif_corrigee,tamis_pratique,cumulatif_pratique):
    #     Xfine = np.linspace(min(tamis_pratique), max(tamis_pratique), 300)
    #     exp_interp = interp1d(tamis_pratique, cumulatif_pratique, kind='linear')
    #     y_exp_interp = exp_interp(Xfine)
    #     # Interpolation cumulatif_actuel
    #     corr_interp = interp1d(tamis_corrigee, cumulatif_corrigee, kind='linear',fill_value="extrapolate")
    #     y_corr_interp = corr_interp(Xfine)
    #     # interpolation des valeurs corrigées
    #     # erreur 2D
    #     dx = Xfine - Xfine   # Xfine vs Xfine → pas d’écart sur X
    #     dy = y_corr_interp - y_exp_interp
    #     return np.sum(dy**2)

    # def erreur_minim(params_correct,tamis_originale,cumulatif_originale,tamis_pratique,cumulatif_pratique):
    #     scale , offset = params_correct
    #     tamis_corr = tamis_originale * scale + offset
    #     Xfine = np.linspace(min(tamis_pratique), max(tamis_pratique), 300)
    #     corr_interp = interp1d(tamis_corr, cumulatif_originale,kind='linear',fill_value="extrapolate")
    #     cumul_corr_interp = corr_interp(Xfine)
    #     prat_interp = interp1d(tamis_pratique, cumulatif_pratique,kind='linear')
    #     cumul_prat_interp = prat_interp(Xfine)
    #     dy = cumul_corr_interp - cumul_prat_interp
    #     return np.sum(dy**2)
    def hihi():
        return None

        

class cumul:
    """Classe contenant les informations d'UN SEUL CUMUL"""
    def __init__(self,Name,Color,granulo,logo):
        self.Name = Name #Format str
        self.Color = Color #Format str
        self.granulo = granulo #format List, contenant la granulo
        self.logo = logo #image format tk
        self.flag_affichage = tk.IntVar(value=0)

class mes_cumuls:
    """Classe contenant tout les cumuls de l'application"""
    def __init__(self):
        self.num = cumul(Name="Courbe numerique Importee",Color='red',granulo=None,logo=importer_image_tk("photo camera.png")) 
        self.originale = cumul(Name="Courbe numerique originale",Color='Blue',granulo=None,logo=None) 
        self.corrigee = cumul(Name="Courbe numerique corrigée",Color='Orange',granulo=None,logo=None)
        self.prat = cumul(Name="Courbe pratique",Color='green',granulo=None,logo=importer_image_tk("logo tamis.png"))



class une_courbe_affiche(tk.Frame):
    """Cette classe permet de construire un carré, le titre du graphe et un check button"""
    def __init__(self,parent,un_cumul,graphe,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        
        self.graphe = graphe
        self.un_cumul = un_cumul

        self._une_courbe_frame_GUI()

    def _une_courbe_frame_GUI(self):
        self.color_square = tk.Label(self, bg=self.un_cumul.Color, width=2, height=1, relief="raised",state="disabled")
        self.label_check_affichage_courbe = tk.Label(self,text=self.un_cumul.Name,state="disabled")
        self.check_affichage_courbe = tk.Checkbutton(self,state="disabled",variable=self.un_cumul.flag_affichage
                                        ,command=self.afficher_courbe,onvalue=1, offvalue=0)

        self.color_square.grid(row=0,column=0,sticky='w',padx=(2,2),pady=(2,2))
        self.label_check_affichage_courbe.grid(row=0,column=1,sticky="ew",padx=(2,2),pady=(2,2))
        self.check_affichage_courbe.grid(row=0,column=2,sticky='e',padx=(2,2),pady=(2,2))

        for i in range(3):
            self.columnconfigure(i,weight=1)

    def activer_affichage(self):
        self.color_square.config(state='normal')
        self.label_check_affichage_courbe.config(state='normal')
        self.check_affichage_courbe.config(state='normal')

    def afficher_courbe(self):
        if self.un_cumul.flag_affichage.get() == 1:
            self.un_cumul.flag_affichage.set(1)
            self.graphe._maj_cumuls()
            self.graphe.canvas_my_graph.draw()
        elif self.un_cumul.flag_affichage.get() == 0:
            self.un_cumul.flag_affichage.set(0)
            self.graphe._maj_cumuls()
            self.graphe.canvas_my_graph.draw()
        else:
            print("Valeur de flag affichage incorrecte")


class courbes_frame(tk.Frame):
    """Regroupe tout les afficheurs de courbes avec un titre"""
    def __init__(self,parent,my_granulos,graphe,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)

        self.my_granulos = my_granulos
        self.graphe = graphe
        self._courbes_frame_GUI()

    def _courbes_frame_GUI(self):
        titre_affichage_courbes = tk.Label(self,text = "Courbes",font=("Arial", 14, "bold"))
        self.courbe_num = une_courbe_affiche(self,self.my_granulos.num,self.graphe)# Courbe avec correction actuelle
        self.courbe_originale = une_courbe_affiche(self,self.my_granulos.originale,self.graphe)# Courbe avan ancienne corrrection
        self.courbe_corrigee = une_courbe_affiche(self,self.my_granulos.corrigee,self.graphe) #courbe après nouvelle correction
        self.courbe_prat = une_courbe_affiche(self,self.my_granulos.prat,self.graphe)
        
         
        titre_affichage_courbes.grid(row=0,sticky="nsew",padx=(2,2),pady=(2,2))
        self.courbe_num.grid(row=1,column=0,sticky="nsew",padx=(2,2),pady=(2,2))
        self.courbe_originale.grid(row=2,column=0,sticky="nsew",padx=(2,2),pady=(2,2))
        self.courbe_corrigee.grid(row=3,column=0,sticky="nsew",padx=(2,2),pady=(2,2))
        self.courbe_prat.grid(row=4,column=0,sticky="nsew",padx=(2,2),pady=(2,2))
        
        self.columnconfigure(0,weight=2)



class import_granulo_frame(tk.Frame):
    """Importation d'une courbe exterieur"""
    def __init__(self,parent,my_granulos,type,graphe,eplac_corr,eplac_courbes,param_corr_act,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        if type == 'num':
            self.cumul = my_granulos.num
        elif type == 'prat':
            self.cumul = my_granulos.prat
        self.my_granulos = my_granulos
        self.graphe = graphe
        self.eplac_corr = eplac_corr
        self.eplac_courbes = eplac_courbes
        self.param_corr_act = param_corr_act
        self.tk_img_import_logo = importer_image_tk("logodownload.png")

        self._import_granulo_frame_GUI()

    def _import_granulo_frame_GUI(self):
        photo = tk.Label(self,image=self.cumul.logo)
        txt = "Importer "+self.cumul.Name
        label_import = tk.Label(self,text=txt)
        btn_import = ttk.Button(self,image=self.tk_img_import_logo,command=lambda : self._import())

        photo.grid(row=0,column=0,padx=(2,2),pady=(2,2))
        label_import.grid(row=0,column=1,sticky='nsew',padx=(2,2),pady=(2,2))
        btn_import.grid(row=0,column=2,sticky='w',padx=(2,2),pady=(2,2))

        for i in range(3):
            self.columnconfigure(i,weight=1)

    def _import(self):
        """Fonction qui importe le chemin des fichiers d'analyse numérique/pratique"""
        if self.cumul.Name == "Courbe numerique Importee":
            path = filedialog.askopenfilename(title="Selectionner un fichier d\'anlyse numérique",
                                            filetypes=[("Fichiers ZIP", "*.zip")])
            if not path:
                print("Erreur : Aucune fichier n'a été selectionné")
            else:
                granulo , correct_var = info_extract_courbe_numerique(path)
                self.cumul.granulo = {"x_axis" : granulo["tamis"] , "y_axis" : granulo["cumul"] }
                self.param_corr_act.var_correct_act["scale"].set(str(correct_var["Scale"]))
                self.param_corr_act.var_correct_act["offset"].set(str(correct_var["Offset"]))
                scale_act = float(self.param_corr_act.var_correct_act["scale"].get())
                offset_act = float(self.param_corr_act.var_correct_act["offset"].get())
                inv_corr_x_axes = inv_correct(granulo["tamis"],scale_act,offset_act)
                self.my_granulos.originale.granulo = {"x_axis" : inv_corr_x_axes , "y_axis" : granulo["cumul"]}
                self.my_granulos.corrigee.granulo = copy.deepcopy(self.my_granulos.originale.granulo)
                self.cumul.flag_affichage.set(1)
                self.my_granulos.originale.flag_affichage.set(1)
                self.my_granulos.corrigee.flag_affichage.set(1)
                self.graphe._maj_cumuls()
                self.graphe.canvas_my_graph.draw()
                self.eplac_courbes.courbe_num.activer_affichage()
                self.eplac_courbes.courbe_originale.activer_affichage()
                self.eplac_courbes.courbe_corrigee.activer_affichage()
                self.eplac_corr.param_correct_nv.enable_affichage_corr_frame()
                self.eplac_corr.save_btn.config(state='normal')
        elif self.cumul.Name == "Courbe pratique":
            path = filedialog.askopenfilename(title="Selectionner un fichier d\'anlyse numérique",
                                          filetypes=[("Fichiers Excel", "*.xlsx")])    
            if not path:
                print("Erreur : Aucune fichier n'a été selectionné")
            else:
                df = pd.read_excel(path)
                self.cumul.granulo = {"x_axis" : df["Tamis(mm)"].tolist() , "y_axis" : df["Cumul(%)"].tolist()}
                self.cumul.flag_affichage.set(1)
                self.graphe._maj_cumuls()
                self.graphe.canvas_my_graph.draw()
                self.eplac_courbes.courbe_prat.activer_affichage()
        else :
            print("Type Error !")
        if self.my_granulos.num.granulo != None and self.my_granulos.prat.granulo != None:
            self.eplac_corr.enable_aff_corr_elt()
            
        

class barre_correct_frame_act(tk.Frame):
    def __init__(self,parent,var_correct,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.var_correct_act = var_correct['var_act'] 
        self._barre_correct_frame_act_GUI()

    def _barre_correct_frame_act_GUI(self):
        tite = tk.Label(self,text="Paramètres de correction actuels",font=("Arial", 10, "bold"))
        scale_label = tk.Label(self,text='scale')
        scale_affiche = tk.Label(self,textvariable=self.var_correct_act["scale"])
        offset_label = tk.Label(self,text='offset') 
        offset_affiche = tk.Label(self,textvariable=self.var_correct_act["offset"]) 

        tite.grid(row=0,column=0,columnspan=2,sticky='we',padx=(2,2),pady=(2,2))
        scale_label.grid(row=1,column=0,sticky='we',padx=(2,2),pady=(2,2))
        offset_label.grid(row=1,column=1,sticky='we',padx=(2,2),pady=(2,2))
        scale_affiche.grid(row=2,column=0,sticky='we',padx=(2,2),pady=(2,2))
        offset_affiche.grid(row=2,column=1,sticky='we',padx=(2,2),pady=(2,2))

        for i in range(2):
            self.columnconfigure(i,weight=1)





class barre_correct_frame_nv(tk.Frame):
    def __init__(self,parent,var_correct,graphe,my_granulos,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.my_granulos = my_granulos
        self.var_correct_nv = var_correct['var_nv']
        self.graphe = graphe
        self._barre_correct_frame_GUI()

    def _barre_correct_frame_GUI(self):
        
        tite = tk.Label(self,text="Nouveaux paramètres de correction",font=("Arial", 10, "bold"))
        scale_entry_label = tk.Label(self,text='scale')
        self.scale_entry = tk.Entry(self,textvariable=self.var_correct_nv["scale"],state='disabled')
        offset_entry_label = tk.Label(self,text='offset') 
        self.offset_entry = tk.Entry(self,textvariable=self.var_correct_nv["offset"],state='disabled') 
        self.validat_btn = ttk.Button(self,text='valider',command=lambda : self._validate_corr_change(),state='disabled')

        tite.grid(row=0,column=0,columnspan=3,sticky='we',padx=(2,2),pady=(2,2))
        scale_entry_label.grid(row=1,column=0,sticky='we',padx=(2,2),pady=(2,2))
        offset_entry_label.grid(row=1,column=1,sticky='we',padx=(2,2),pady=(2,2))
        self.scale_entry.grid(row=2,column=0,sticky='we',padx=(2,2),pady=(2,2))
        self.offset_entry.grid(row=2,column=1,sticky='we',padx=(2,2),pady=(2,2))
        self.validat_btn.grid(row=2,column=2,sticky='we',padx=(2,2),pady=(2,2))

        for i in range(3):
            self.columnconfigure(i,weight=1)
    
    def enable_affichage_corr_frame(self):
        self.scale_entry.config(state='normal')
        self.offset_entry.config(state='normal')
        self.validat_btn.config(state='normal')


    def _validate_corr_change(self):
        scale = float(self.var_correct_nv["scale"].get())
        if scale < 0:
            scale = 0.001
            self.var_correct_nv["scale"].set(str(0.001))
        offset = float(self.var_correct_nv["offset"].get())
        # if corr_type == "var_act":
        #     inv_corr_x_axes = Utils.inv_correct(self.my_granulos.num.granulo["x_axis"],scale,offset)
        #     self.my_granulos.originale.granulo = {"x_axis" : inv_corr_x_axes , "y_axis" : self.my_granulos.originale.granulo["y_axis"]}
        corr_x_axes = Utils.correct(self.my_granulos.originale.granulo["x_axis"],scale,offset)
        self.my_granulos.corrigee.granulo = {"x_axis" : corr_x_axes , "y_axis" : self.my_granulos.originale.granulo["y_axis"]}
        self.graphe._maj_cumuls()
        self.graphe.canvas_my_graph.draw()
        


        
    
class donnees_ext_frame(tk.Frame):
    """S'occupe d'organiser la partie importation de données exterieurs"""
    def __init__(self,parent,my_granulos,graphe,var_correct,eplac_corr,eplac_courbes,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)

        self.my_granulos = my_granulos
        self.graphe = graphe
        self.var_correct = var_correct
        self.eplac_corr = eplac_corr
        self.eplac_courbes = eplac_courbes

        self._donnees_ext_frame_GUI()

    def _donnees_ext_frame_GUI(self):
        titre = tk.Label(self,text="Données Exterieurs",font=("Arial", 14, "bold"))
        self.param_correct_act = barre_correct_frame_act(self,self.var_correct)
        # self.param_correct_act = barre_correct_frame(self,self.var_correct,"var_act",self.graphe,self.my_granulos)
        import_num = import_granulo_frame(self,self.my_granulos,'num',self.graphe,self.eplac_corr,self.eplac_courbes,self.param_correct_act)
        import_prat = import_granulo_frame(self,self.my_granulos,'prat',self.graphe,self.eplac_corr,self.eplac_courbes,self.param_correct_act)
        separator = tk.Frame(self, bg="black", height=2)

        titre.grid(row=0,column=0,columnspan=3,sticky='nsew',padx=(2,2),pady=(2,2))
        import_num.grid(row=1,column=0,sticky='nsew',padx=(2,2),pady=(2,2))
        import_prat.grid(row=2,column=0,sticky='nsew',padx=(2,2),pady=(2,2))
        separator.grid(row=3,column=0,sticky='nsew',padx=(2,2),pady=(2,2))
        self.param_correct_act.grid(row=4,column=0,sticky='nsew',padx=(2,2),pady=(2,2))

        self.columnconfigure(0,weight=2)
    

class correct_frame(tk.Frame):
    def __init__(self,parent,my_granulos,graphe,var_correct,erreur,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.my_granulos = my_granulos
        self.graphe = graphe
        self.var_correct = var_correct
        self.erreur = erreur

        self._auto_error_fram_GUI()
        self._correct_frame_GUI()

    def _auto_error_fram_GUI(self):
        self.auto_err = tk.Frame(self)
        afficheur_err_label = tk.Label(self.auto_err,text="Erreur : ")
        self.afficheur_err = tk.Label(self.auto_err,textvariable=self.erreur,state="disabled")
        self.btn_auto_corr = ttk.Button(self.auto_err,text="Correction Auto",command=self._correction_auto,state="disabled")

        afficheur_err_label.grid(row=0,column=0,sticky="w",padx=(2,2),pady=(2,2))
        self.afficheur_err.grid(row=0,column=1,sticky="w",padx=(2,2),pady=(2,2))
        self.btn_auto_corr.grid(row=0,column=2,sticky="e",padx=(2,2),pady=(2,2))

        self.auto_err.columnconfigure(2,weight=1)


    def _correct_frame_GUI(self):
        title = tk.Label(self,text="Correction",font=("Arial", 14, "bold"))
        separator = tk.Frame(self, bg="black", height=2)
        self.param_correct_nv = barre_correct_frame_nv(self,self.var_correct,self.graphe,self.my_granulos)
        self.save_btn = ttk.Button(self,text="Sauvegarder les nouveaux paramètres",command=self._save_new_corr_params,state="disabled")

        title.grid(row=0,column=0,columnspan=3,sticky="nsew",padx=(2,2),pady=(2,2))
        self.auto_err.grid(row=1,column=0,columnspan=3,sticky="nsew",padx=(2,2),pady=(2,2))
        separator.grid(row=2,column=0,columnspan=3,sticky="nsew",padx=(2,2),pady=(2,2))
        self.param_correct_nv.grid(row=3,column=0,columnspan=3,sticky="nsew",padx=(2,2),pady=(2,2))
        self.save_btn.grid(row=4,column=0,columnspan=3,sticky="nsew",padx=(2,2),pady=(2,2))

        self.columnconfigure(0,weight=1)
    
    def enable_aff_corr_elt(self):
        self.afficheur_err.config(state='normal')
        self.btn_auto_corr.config(state='normal')

    def _correction_auto(self):
        param0 = [1.0 , 0.0]
        tamis_originale = np.array(self.my_granulos.originale.granulo["x_axis"])
        cumulatif_originale = np.array(self.my_granulos.originale.granulo["y_axis"])
        tamis_pratique = np.array(self.my_granulos.prat.granulo["x_axis"])
        cumulatif_pratique = np.array(self.my_granulos.prat.granulo["y_axis"])
        res = minimize(
        erreur_minim,
        param0,
        args=(tamis_originale, cumulatif_originale,
            tamis_pratique, cumulatif_pratique),
        bounds = [(1e-6, None), (None, None)]   
        )
        scale_nv , offset_nv = res.x
        self.var_correct["var_nv"]["scale"].set(str(round(scale_nv,3)))
        self.var_correct["var_nv"]["offset"].set(str(round(offset_nv,3)))
        tamis_orig = self.my_granulos.originale.granulo["x_axis"]
        self.my_granulos.corrigee.granulo["x_axis"] =  correct(tamis_orig,scale_nv,offset_nv)
        self.graphe._maj_cumuls()
        self.graphe.canvas_my_graph.draw()
    
    def _save_new_corr_params(self):
        self.win=tk.Toplevel(self)
        self.win.title("Attention !")
        self.win.geometry("600x80")
        self.win.grab_set()
        message = tk.Label(self.win,text="Etes vous sur de vouloir mettre à jour les nouveaux paramètre de correction sur l'application principale ?")
        btn_oui = tk.Button(self.win,text="Oui",command=self.rep_confirmation_oui)
        btn_non = tk.Button(self.win,text="Non",command=self.rep_confirmation_non)
        message.grid(row=0,column=0,columnspan=2,padx=(2,2),pady=(10,2))
        btn_oui.grid(row=1,column=0,sticky="we",padx=(2,2),pady=(10,2))
        btn_non.grid(row=1,column=1,sticky='we',padx=(2,2),pady=(10,2))
        self.win.columnconfigure(0,weight=1)
        self.win.columnconfigure(1,weight=1)
    
    def rep_confirmation_oui(self):
        self.win.destroy()
        return None
    
    def rep_confirmation_non(self):
        self.win.destroy()
        return None

    


class graphe(tk.Frame):
    def __init__(self,parent,my_granulos,erreur,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)
        self.my_granulos = my_granulos
        self.erreur = erreur
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self._maj_cumuls()

        self.canvas_my_graph = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_my_graph.draw()
        self.canvas_my_graph.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    def _maj_cumuls(self):
        self.ax.cla()
        if self.my_granulos.num.flag_affichage.get() == 1:
            self.ax.plot(self.my_granulos.num.granulo["x_axis"], self.my_granulos.num.granulo["y_axis"],label=self.my_granulos.num.Name,color=self.my_granulos.num.Color)
        if self.my_granulos.originale.flag_affichage.get() == 1:
            self.ax.plot(self.my_granulos.originale.granulo["x_axis"], self.my_granulos.originale.granulo["y_axis"],label=self.my_granulos.originale.Name,color=self.my_granulos.originale.Color)
        if self.my_granulos.prat.flag_affichage.get() == 1:
            self.ax.plot(self.my_granulos.prat.granulo["x_axis"], self.my_granulos.prat.granulo["y_axis"],label=self.my_granulos.prat.Name,color=self.my_granulos.prat.Color)
        if self.my_granulos.corrigee.flag_affichage.get() == 1:
            self.ax.plot(self.my_granulos.corrigee.granulo["x_axis"], self.my_granulos.corrigee.granulo["y_axis"],label=self.my_granulos.corrigee.Name,color=self.my_granulos.corrigee.Color)
        self.ax.set_xlim(0, 90)
        self.ax.set_ylim(0, 100)
        if self.my_granulos.num.flag_affichage.get() == 1 or self.my_granulos.prat.flag_affichage.get() == 1:
            self.ax.legend()
        if self.my_granulos.corrigee.granulo != None and self.my_granulos.prat.granulo != None:
            tam_prat = self.my_granulos.prat.granulo["x_axis"]
            cumul_prat = self.my_granulos.prat.granulo["y_axis"]
            tam_corr = self.my_granulos.corrigee.granulo["x_axis"]
            cumul_corr = self.my_granulos.corrigee.granulo["y_axis"]
            self.erreur.set(str(round(erreur(tam_corr,cumul_corr,tam_prat,cumul_prat),3)))




class interfaceCommunication(tk.Frame):
    def __init__(self,parent,my_granulos,graphe,var_correct,erreur,*args,**kwargs):
        super().__init__(parent,*args,**kwargs)

        #Variables 
        self.my_granulos = my_granulos
        self.graphe = graphe
        self.var_correct = var_correct
        self.erreur = erreur

        #Graphique
        self._interfaceCommunication_GUI()
    

    def _interfaceCommunication_GUI(self):
        """Disposition graphique des élement de l'interface"""
        self.eplac_courbes = courbes_frame(self,self.my_granulos,self.graphe)
        self.eplac_corr = correct_frame(self,self.my_granulos,self.graphe,self.var_correct,self.erreur)
        eplac_donnees_ext = donnees_ext_frame(self,self.my_granulos,self.graphe,self.var_correct,self.eplac_corr,self.eplac_courbes)

        eplac_donnees_ext.grid(row=0,columnspan=3,sticky='nsew',padx=(2,2),pady=(2,2))
        self.eplac_courbes.grid(row=1,columnspan=3,sticky='nsew',padx=(2,2),pady=(2,2))
        self.eplac_corr.grid(row=2,columnspan=3,sticky='nsew',padx=(2,2),pady=(2,2))

        self.columnconfigure(0,weight=2)
 
     
        

    


class appReglageParamsCorrectEmpririque(tk.Tk):
    """Application qui permet de changer les paramètres de correction empirique ("scale" et "offset") appliqués à la courbe numérique"""
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        #Variables
        self.my_granulos = mes_cumuls()
        self.var_correct = {"var_act" : None , "var_nv" : None}
        for key in self.var_correct:
            self.var_correct[key] = {"scale" : tk.StringVar(value="1.00") , "offset" : tk.StringVar(value="0.00")}
        self.erreur = tk.StringVar(value="0.00")


        #Dimensionnement de la fenêtre
        self.geometry("1000x750")
        self.resizable(False, False)
        self.title("CIMES - Changer les paramètres de correction")

        #Créer une interface d'interration avec l'utilisateur
        self.graphe = graphe(self,self.my_granulos,self.erreur)
        iC = interfaceCommunication(self,self.my_granulos,self.graphe,self.var_correct,self.erreur,width = 300,bg='grey')
        

        #Graphique
        iC.grid(row=0,column=0,sticky='nsew',padx=(2,2),pady=(2,2))
        iC.grid_propagate(False)
        self.graphe.grid(row=0,column=1,sticky='nsew')

        self.rowconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
  

        
if __name__ == '__main__':
  app = appReglageParamsCorrectEmpririque()
  app.mainloop()




        
