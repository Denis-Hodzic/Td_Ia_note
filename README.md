# Velonecy – Quadtree des stations de vélos

Application Flask qui génère et affiche un **Quadtree** (arbre quaternaire) des stations de vélos en libre-service de la société Velonecy, afin d'identifier les zones sous-équipées de la commune.

## Ce que fait l'application

- Génère un jeu de données simulé de 240 stations sur une carte de 1000 × 1000 m (Suburbs, Petit-Port, City-Centre, Campus et New-Stations).
- Construit un Quadtree : une cellule est subdivisée en quatre quadrants dès qu'elle contient plus de `capacity` stations (profondeur maximale : 8).
- Affiche le graphique sur la page HTML, avec le nombre de nœuds obtenus.

L'utilisateur choisit la **capacité** (entier entre 1 et 100, 8 par défaut) via un formulaire. Le graphique est régénéré et affiché sur la même page.
Une valeur invalide (texte, 0, > 100) affiche un message d'erreur avec le code HTTP `400`.

Plus la capacité est faible, plus l'arbre est profond. Les petites cellules correspondent aux zones denses, les grandes cellules aux zones peu équipées, où de nouvelles stations seraient utiles.

## Structure du projet

```
app.py                   # Application Flask et route GET "/"
quadtree_utils.py        # Génération des données, construction du Quadtree, graphique
templates/index.html     # Page HTML (formulaire + affichage Jinja du graphique)
static/style.css         # Feuille de style
requirements.txt         # Dépendances Python
Dockerfile               # Image Docker
quadtree_stations.ipynb  # Notebook d'origine
```

## Lancer avec Docker

### 1. Construire l'image

Depuis le dossier du projet :

```bash
docker build -t velonecy-quadtree .
```

### 2. Lancer le conteneur

```bash
docker run -p 5000:5000 velonecy-quadtree
```

Puis ouvrir **http://localhost:5000** dans un navigateur.

Si le port 5000 est déjà utilisé, changer le port de gauche (port de la machine) :

```bash
docker run -p 5001:5000 velonecy-quadtree
```

et ouvrir **http://localhost:5001**.

### 3. Utilisation

Saisir une capacité dans le formulaire puis cliquer sur **Generate**. On peut aussi passer la capacité directement dans l'URL :

```
http://localhost:5000/?capacity=3
```

### Arrêter le conteneur

`Ctrl+C` dans le terminal, ou :

```bash
docker ps                 # récupérer l'ID du conteneur
docker stop <id>
```
