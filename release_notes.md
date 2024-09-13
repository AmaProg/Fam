# 1.6.8

- Correction de l'affichage des choix en doublon.
- Déplacement de la commande `subcategory` vers la commande `get subcategory`.
- Amélioration de l'affichage du menu des choix.
- Ajout de la sous-commande `account-nickname` à la commande `get`.


# 1.5.7

- **Ajout de la commande `account-nickname`** : Permet de créer des comptes avec des surnoms.
- **Ajout de la commande `finance income-statement`** : Permet de créer un compte de résultats.
- **Correction de l'auto-classification** : Résout le problème des doublons en utilisant la commande `account-nickname`.

# 1.4.6

- Précharge des données telles que les catégories et sous-catégories dans la base de données lors de l'inscription

# 1.3.5

- **Intégration de la banque Tangerine**  
  Pour le traitement des relevés de carte de crédit.

- **Résolution du problème de comparaison des descriptions**  
  Gérer correctement les descriptions contenant des caractères spéciaux.

- **Ajout d'informations sur les sous-catégories**  
  Afficher des détails sur la sous-catégorie dans l'aide de la commande `create` via l'option `--help`.


# 1.2.4

- **Intégration de la commande "create transaction"** : Permet la saisie manuelle des transactions.
- **Intégration de la commande "create classification"** : Facilite l'ajout manuel de classifications.
- **Mise à jour automatique de la base de données** : Lors de l'exécution de la commande "upgrade", la base de données de l'utilisateur sera mise à jour automatiquement pour refléter les dernières modifications de l'application.
- **Optimisation de l'affichage des menus** : Les menus sont maintenant mieux organisés pour une visibilité accrue.
- **Ajout de l'option "proportion de paiement"** : Permet de définir la proportion du montant à partager lors des transactions, utile pour les dépenses en couple ou entre amis.


# 1.1.4

- Ajout de la command subcategory avec le sous-commande list
- Ajoute de la command logout
- Ajoute de filtrege de date pour la command expense

# 1.0.3

- Corriger le problème de Fam : "The following description {transaction} already exists." [x]
- Corriger le problème pour la commande expense
- Afficher les choix en colonnes de 10 éléments par ligne [x]



