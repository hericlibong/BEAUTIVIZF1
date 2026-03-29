# Validation manuelle: choix explicite du format

## But

Vérifier que la V1 sait :
- proposer les deux formats du MVP après un besoin interprété,
- accepter un choix explicite valide entre `heatmap` et `line chart race`,
- rester bloquée avant toute génération.

Cette validation s'arrête avant la récupération des données, le rendu et les exports.

## Préparation

- Partir d'un besoin F1 déjà interprétable.
- Observer la proposition de formats puis le résultat du choix explicite.
- Vérifier qu'aucune génération n'est lancée à ce stade.

## Cas 1: les deux formats sont proposés

Message :

```text
Je veux comparer les écarts des pilotes en qualifications 2025.
```

Comportement attendu :
- le besoin est interprété
- la proposition contient exactement `heatmap` et `line chart race`
- la proposition rappelle brièvement le besoin compris
- la prochaine étape attendue est le choix explicite du format

## Cas 2: choix explicite valide

Choix utilisateur :

```text
heatmap
```

Comportement attendu :
- le résultat du choix est `selected`
- une sélection exploitable est produite
- le format retenu est `heatmap`
- le flux confirme que la suite peut être préparée, sans encore générer la visualisation

## Rappel de verrou

À ce stade :
- aucune génération ne doit partir automatiquement
- aucun rendu final ne doit être produit
- aucun provider F1 ne doit être appelé
