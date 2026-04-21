# real_world_search_engine / SDSA

Ce dépôt contient désormais un **prototype exécutable** d'un *Système de Découverte Scientifique Assistée (SDSA)* avec :

- une architecture modulaire (knowledge, hypothèses, simulation, orchestration),
- une CLI pour lancer un pipeline complet,
- une interface graphique Tkinter,
- des tests unitaires de base.

> ⚠️ Important: construire en une seule passe un produit industriel complet de 2500+ fichiers et 150k+ lignes n'est pas réaliste sans équipe, lotissement, validation scientifique et cycles V&V. Ce repo livre une **fondation propre et extensible**.

## Démarrage rapide

### 1) Installer
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2) Lancer la CLI
```bash
sdsa --objective "Matériau de stockage énergie haute densité" --budget 5
```

### 3) Lancer la GUI Tkinter
```bash
python -m sdsa.gui.app
```

### 4) Exécuter les tests
```bash
pytest
```

## Structure

- `sdsa/core`: modèles de données + orchestrateur
- `sdsa/services`: couche connaissance + génération d'hypothèses
- `sdsa/sim`: moteur de simulation prototype
- `sdsa/gui`: interface utilisateur Tkinter
- `sdsa/api`: contrats API (spécification)
- `tests`: tests unitaires

## Prochaines étapes industrielles

1. Remplacer les stubs par solveurs réels (FEM/FVM/PDE, UQ robuste).
2. Brancher une base de connaissance persistante (RDF + graph DB + vector DB).
3. Ajouter provenance immuable, policy service et contrôles dual-use.
4. Déployer en microservices (gRPC + event bus + orchestration DAG + HPC).
