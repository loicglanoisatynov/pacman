# Pacman & AI

## Sommaire

- [Pacman \& AI](#pacman--ai)
  - [Sommaire](#sommaire)
  - [Description](#description)
  - [Prérequis](#prérequis)
  - [Structure du projet](#structure-du-projet)
  - [Utilisation](#utilisation)
  - [Auteurs](#auteurs)

## Description

Ce projet est composé de deux parties :

Le jeu Pacman : Un jeu classique où le joueur contrôle Pacman et interagit avec les fantômes.
L'IA de Pacman : Une intelligence artificielle qui apprend à jouer au jeu à l'aide de l'apprentissage par renforcement (DQN).

En l'état, seul la partie jeu Pacman est fonctionnelle. L'IA en est encore à un état d'intelligence embryonnaire et la partie renforcement n'est pas fonctionnelle.

## Prérequis

Vous aurez besoin d'avoir Python d'installé sur votre machine. Si c'est fait, vous n'avez plus qu'à installer les bibliothèques renseignées dans le fichier requirements.txt. Les bibliothèques en question sont les suivantes :

- Pygame
- PyTorch
- Numpy

Vous pouvez les installer avec la commande `pip install -r requirements.txt` ou `conda install --file requirements.txt` si vous utilisez Conda.

## Structure du projet

Jeu Pacman :
main.py : Point d'entrée du jeu, gère la boucle du jeu et l'interaction avec l'environnement.

Le code source du jeu est réparti dans le répertoire `./src/`. Vous y trouverez les classes, les fichiers relatifs au machine learning et les paramètres de configuration.

Vous trouverez également un répertoire `./assets/` contenant les images et les sons du jeu.

## Utilisation

Pour lancer le jeu, exécutez la commande `python main.py` dans le répertoire racine du projet.

Jeu Pacman : Pacman se déplace dans un labyrinthe pour manger des pac-gommes tout en évitant les fantômes.

Vous trouverez un mode de jeu manuel, où vous contrôlez Pacman avec les touches fléchées, et un mode de jeu automatique, où Pacman se déplace en suivant un algorithme de pathfinding. A noter que l'IA n'est pas encore fonctionnelle. Vous trouverez aussi un mode AI training, qui permet de lancer l'entraînement de l'IA.

Apprentissage par renforcement : L'IA apprend à jouer en optimisant ses actions à travers des itérations d'entraînement avec DQN, en s'appuyant sur un réseau neuronal pour prédire les meilleures actions.

## Auteurs

Ce projet est le résultat de la collaboration conjointe d'Adrien FROECHLY, de Loïc GLANOIS et de Mustapha NOUSSAIR, tous trois étudiants en Bachelor 2 Informatique à Lyon Ynov Campus. Ce projet est réalisé dans le cadre de notre module pédagogique en Python.