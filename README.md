# Système de Recommandation de Films en Temps Réel

Ce projet consiste à développer un système de recommandation de films en temps réel, en exploitant les données de MovieLens. Il utilise Apache Spark pour le traitement des données, Elasticsearch pour le stockage et la recherche, Kibana pour la visualisation, et Flask (ou FastAPI) pour l'API REST.

## Objectif

L'objectif est de créer un système qui permet de :
- Collecter et traiter les données d'interactions utilisateurs et les métadonnées des films.
- Générer des recommandations de films en temps réel.
- Fournir une API REST permettant aux utilisateurs de recevoir des recommandations personnalisées.

## Ressources

- **Dataset MovieLens** : Utilisé pour les interactions utilisateur et les métadonnées des films.
- **Technologies principales** :
  - **Apache Spark** : Traitement et analyse des données.
  - **Elasticsearch** : Stockage et recherche des données.
  - **Kibana** : Visualisation des données.
  - **Flask (ou FastAPI)** : Développement de l'API REST pour les recommandations.

## Configuration de l'Environnement

### Prérequis

- **Docker** : Pour exécuter tous les services dans des conteneurs.
- **Docker Compose** : Pour gérer plusieurs conteneurs Docker et faciliter l'orchestration.

### Installation des Services

1. Clonez le repository :

   ```bash
   git clone https://github.com/votre-repository/recommendation-system.git
   cd recommendation-system
