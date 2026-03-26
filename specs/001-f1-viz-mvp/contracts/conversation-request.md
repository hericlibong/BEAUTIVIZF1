# Contract: Conversation Request and Format Selection

## Purpose

Définir le contrat d'entrée du chatbot simple: expression d'un besoin analytique en langage naturel, interprétation, proposition des deux formats disponibles du MVP, puis choix explicite de l'utilisateur.

## Interface

- **Consumer**: utilisateur de BEAUTIVIZF1
- **Provider**: couche conversationnelle du chatbot
- **Cardinality**: une demande conduit au maximum à une seule visualisation

## Step 1: Conversation Request

| Field | Description |
|-------|-------------|
| `user_message` | Besoin analytique ou éditorial formulé en langage naturel |
| `conversation_context` | Contexte minimal utile si un échange court précède la demande |

## Step 2: Interpretation Outcome

| Outcome | Meaning |
|---------|---------|
| `interpreted` | Le besoin est compris de manière exploitable |
| `clarify` | Une précision simple est nécessaire |
| `reject` | La demande est hors périmètre ou trop ambiguë |

## Step 3: Format Proposal and Selection

| Field | Rule |
|-------|------|
| `available_formats` | Doit présenter `heatmap` et `line_chart_race` |
| `chosen_format` | Doit être explicitement choisi par l'utilisateur |
| `generation_allowed` | Ne devient vrai qu'après ce choix explicite |

## Rejection and Clarification Rules

- Refuser les demandes portant sur plusieurs visualisations dans un seul besoin.
- Demander une précision si le besoin est compréhensible mais pas assez cadré.
- Ne jamais générer de visualisation avant le choix explicite du format.
