# Validation manuelle: interprétation en langage naturel

## But

Vérifier que la V1 sait :
- interpréter un besoin F1 exploitable,
- demander une clarification simple quand le besoin est trop vague,
- rejeter une demande hors périmètre.

Cette validation s'arrête avant la proposition des formats et avant toute génération.

## Préparation

- Utiliser le point d'entrée conversationnel léger.
- Saisir un message utilisateur unique en langage naturel.
- Observer uniquement le résultat d'interprétation : `interpreted`, `clarify` ou `reject`.

## Cas 1: besoin interprété

Message :

```text
Je veux comparer les écarts des pilotes en qualifications 2025.
```

Comportement attendu :
- le résultat est `interpreted`
- une intention est produite
- l'intention ne demande pas de clarification
- le périmètre reconnu inclut la saison 2025 et les pilotes

## Cas 2: besoin à clarifier

Message :

```text
Comparer les pilotes en F1
```

Comportement attendu :
- le résultat est `clarify`
- une intention existe encore
- l'intention demande une clarification
- la clarification demande de préciser la saison ou la période

## Cas 3: besoin rejeté

Message :

```text
Je veux visualiser les ventes de smartphones en Europe.
```

Comportement attendu :
- le résultat est `reject`
- aucune intention exploitable n'est produite
- la raison du rejet indique que la demande est hors périmètre F1
