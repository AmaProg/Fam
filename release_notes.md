# Version 1.7.10

- Ajout de la sous-commande `transaction` dans la commande `delete`. Cette sous-commande permet de supprimer toutes les transactions présentes dans la base de données.
- Correction du problème lié au type de transaction lorsque celui-ci est automatiquement catégorisé.



# Version 1.6.9
- Suppression du fichier `transaction_rule` devenu obsolète.
- Standardisation des relevés bancaires dans la commande `add` pour uniformiser le traitement des transactions.
- Mise à jour du message pour l'option zéro dans `add statement`, avec remplacement de "Fam: The description cannot be categorized." par "The transaction has not been categorized."

# Version 1.6.8
- Correction des doublons dans l'affichage des choix.
- Déplacement de la commande `subcategory` vers `get subcategory` pour une meilleure organisation.
- Amélioration de la présentation du menu de sélection des choix.
- Ajout de la sous-commande `account-nickname` à `get`, facilitant la gestion des comptes avec surnoms.

# Version 1.5.7
- **Nouvelle commande `account-nickname`** : Permet de créer et gérer des comptes avec des surnoms personnalisés pour une gestion simplifiée.
- **Ajout de la commande `finance income-statement`** : Génère un compte de résultats complet.
- **Amélioration de l'auto-classification** : Résolution des doublons en utilisant les surnoms de comptes via `account-nickname`.

# Version 1.4.6
- Préchargement automatique des catégories et sous-catégories lors de l'inscription pour accélérer le démarrage.

# Version 1.3.5
- **Intégration de la banque Tangerine** : Gestion des relevés de cartes de crédit Tangerine.
- **Amélioration de la gestion des descriptions** : Prise en charge des caractères spéciaux dans les descriptions lors de la comparaison.
- **Informations enrichies sur les sous-catégories** : Affichage des détails supplémentaires dans l'aide de la commande `create` via `--help`.

# Version 1.2.4
- **Nouvelle commande `create transaction`** : Permet l’ajout manuel de transactions.
- **Nouvelle commande `create classification`** : Simplifie l'ajout manuel des classifications.
- **Mise à jour automatique de la base de données** : La commande `upgrade` met automatiquement à jour la base de données de l'utilisateur avec les dernières modifications.
- **Organisation améliorée des menus** : Réorganisation des menus pour une meilleure lisibilité.
- **Nouvelle option de "proportion de paiement"** : Partage des montants des transactions, pratique pour les dépenses partagées (ex. couple, amis).

# Version 1.1.4
- Ajout de la sous-commande `list` à la commande `subcategory`.
- Ajout de la commande `logout` pour déconnexion rapide.
- Ajout de filtres par date pour la commande `expense` afin de mieux cibler les transactions.

# Version 1.0.3
- Correction du message d’erreur dans Fam : "The following description {transaction} already exists."
- Résolution des problèmes avec la commande `expense`.
- Amélioration de l'affichage des choix en colonnes, avec 10 éléments par ligne pour une meilleure lisibilité.
