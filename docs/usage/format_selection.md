# Choisir entre heatmap et line chart race

## Ce que couvre cette étape

Dans cette V1, après l'interprétation du besoin, le chatbot présente les deux formats du MVP :
- `heatmap`
- `line chart race`

L'utilisateur doit ensuite choisir explicitement l'un des deux. Cette étape ne génère pas encore la visualisation finale.

## Comment le chatbot présente les formats

La proposition :
- rappelle brièvement le besoin compris
- présente les deux formats disponibles
- explique en une phrase simple pourquoi chaque format peut correspondre au besoin

La proposition reste contextuelle. Par exemple, un besoin sur les écarts en qualifications sera reformulé avec une justification courte liée aux écarts, aux pilotes et à la saison.

## Ce que représente chaque format

`heatmap`
- utile pour comparer rapidement des valeurs ou des écarts entre plusieurs pilotes ou équipes

`line chart race`
- utile pour montrer une évolution au fil du temps ou de la saison

## Comment choisir

Le choix doit être explicite et limité à l'un des deux formats du MVP :

```text
heatmap
```

```text
line chart race
```

Si le choix est absent ou invalide, le flux reste bloqué sur cette étape.

## Limite actuelle

Cette étape s'arrête après la sélection du format :
- pas de génération automatique
- pas de rendu final
- pas d'embed
- pas de pipeline data lancé
