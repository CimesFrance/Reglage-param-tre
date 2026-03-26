
# CIMES - Ajustement des Paramètres de Correction Granulométrique

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange.svg)
![SciPy](https://img.shields.io/badge/Library-SciPy-green.svg)

**Correction CIMES** est une application Python interactive conçue pour synchroniser des courbes granulométriques issues d'analyses numériques avec des données réelles de tamisage physique. Elle permet d'appliquer et d'optimiser des transformations linéaires (**Scale** et **Offset**) pour corriger les écarts de mesure entre le virtuel et le réel.

---

## Fonctionnalités 

* **Importation Multiformat** : 
    * Lecture de courbes numériques via fichiers `.zip` (extraction automatique du CSV de données et du fichier texte de paramètres).
    * Importation de courbes réelles via fichiers Excel (`.xlsx`).
* **Correction Dynamique** : Ajustement manuel des paramètres de correction via l'interface, avec mise à jour immédiate du graphique.
* **Optimisation Automatique** : Intégration de `scipy.optimize.minimize` pour calculer mathématiquement les paramètres optimaux minimisant l'erreur quadratique entre les deux courbes.
* **Visualisation Avancée** : Comparaison simultanée de trois états de données via `Matplotlib` :
    * 🔴 **Courbe numérique corrigée** : État actuel après application des paramètres.
    * 🔵 **Courbe numérique originale** : Données brutes avant toute correction.
    * 🟢 **Courbe réelle tamisée** : La référence physique de laboratoire.

---

## Architecture du Code

Le projet est découpé en modules spécialisés pour une meilleure maintenance :

| Fichier | Rôle Principal |
| :--- | :--- |
| **`main.py`** | Gère le cycle de vie de l'application, l'interface graphique (Tkinter) et les interactions utilisateur. |
| **`utils/correction_manager.py`** | Contient le moteur mathématique : fonctions de correction, calcul d'erreur quadratique et algorithme de minimisation. |
| **`utils/import_manager.py`** | Gère l'extraction des données depuis les archives ZIP et la conversion des formats de fichiers. |

---

## Logique de Correction

L'application utilise une transformation linéaire sur l'axe des abscisses (diamètre des particules) :

$$x_{corrigé} = x_{original} \cdot \text{scale} + \text{offset}$$

L'erreur affichée dans l'interface est calculée sur **300 points interpolés** (via `interp1d`) pour garantir une précision constante, même si les deux courbes n'ont pas les mêmes points de mesure initiaux :

$$\text{Erreur} = \frac{1}{300} \sum (y_{corrigé} - y_{pratique})^2$$

---

## Installation et Lancement

1.  **Prérequis** : Assurez-vous d'avoir Python 3.x installé.
2.  **Installation des dépendances** :
    ```bash
    git clone git@github.com:CimesFrance/Reglage-param-tre.git
    ```
    ```bash
    pip install -r requirements.txt
    ```
3.  **Lancement** :
    ```bash
    python main.py
    ```

> [!IMPORTANT]
> L'application nécessite la présence des icônes (`photo camera.png`, `logo tamis.png`, `logodownload.png`) dans le répertoire de travail pour charger l'interface correctement.

---

## Utilisation

1.  **Importer** la courbe numérique (Zip) et la courbe de référence (Excel).
2.  Observer l'**Erreur** initiale affichée dans le module de correction.
3.  Cliquer sur **"Correction Auto"** pour laisser l'algorithme `minimize` trouver le meilleur compromis mathématique.
4.  Ajuster manuellement si nécessaire et **Sauvegarder** les paramètres une fois satisfait.


