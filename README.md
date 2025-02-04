# Analyse Automatisée des Fragments Rocheux dans les Profils de Sol

## Description
Ce projet implémente une application de traitement d'image pour l'analyse automatisée des profils de sol. Il utilise des algorithmes de traitement d'image classiques afin de détecter et quantifier les fragments rocheux visibles sur des images de profils. L'objectif est d'automatiser cette tâche de manière objective et reproductible, en remédiant à l'absence de données massives pour entraîner des modèles d'intelligence artificielle.

Les principales fonctionnalités comprennent :
- Prétraitement des images (suppression des ombres, filtrage).
- Segmentation par seuils pour détecter les fragments rocheux.
- Calcul de la densité des fragments identifiés sur le profil.

## Structure du Projet
```
root/
├── main.py                      # Script principal pour l'analyse d'une image
├── elements_grossiers.py        # Implémentation des fonctions de détection des fragments rocheux
├── README.md                    # Documentation du projet
├── requirements.txt             # Dépendances nécessaires
└── images/                      # Dossier pour les images d'entrée
```

## Installation
1. **Cloner le dépôt**
```bash
git clone https://github.com/Jidoex/Projet3A.git
cd votre-repo
```

2. **Créer un environnement virtuel (optionnel)**
```bash
python3 -m venv env
source env/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

## Utilisation
### Analyse d'une image
1. Placer l'image à analyser dans le dossier `images/`.
2. Modifier le chemin de l'image dans `main.py` :
   ```python3
   image_path = "./images/nom_image.jpg"
   ```
3. Exécuter le script principal :
   ```bash
   python3 main.py
   ```

### Exemple de sortie
```
Segmentation finie.
La densité des éléments grossiers sur le profil est 12.45%
```

## Fonctionnalités principales
### Prétraitement
- Suppression des ombres sur le canal de valeur.
- Filtrage Gaussien pour réduire le bruit.

### Segmentation
- Application de seuils prédéfinis pour détecter les fragments de différents contrastes.

### Calcul de la densité
- Évaluation de la proportion de fragments rocheux dans le profil analysé.

## Améliorations Futures
- Affiner les seuils de segmentation pour une détection plus précise.
- Optimiser la combinaison des masques dans la fonction `post_segmentation`.
- Ajouter une détection automatisée de la zone exacte du profil.
- Intégrer une interface graphique pour une utilisation plus conviviale.

## Contributions
Les contributions sont les bienvenues ! N'hésitez pas à ouvrir des issues ou à soumettre des pull requests.