# Financial Advisor for Me (FAM)

Bienvenue à **Financial Advisor for Me (FAM)**, une application dédiée à la gestion budgétaire personnelle. FAM vous permet de suivre et de gérer efficacement vos finances en catégorisant vos transactions bancaires extraites de fichiers CSV. Grâce à cette application, vous pouvez analyser vos dépenses et vos revenus pour mieux contrôler votre budget.

## Fonctionnalités principales
- **Importation de fichiers CSV** : Récupérez vos données bancaires automatiquement via des fichiers CSV.
- **Catégorisation intelligente** : Classez vos transactions par catégories et sous-catégories (dépenses, revenus, etc.).
- **Gestion budgétaire** : Suivez vos finances en temps réel, identifiez les tendances, et ajustez votre budget.
- **Rapports personnalisés** : Générez des rapports de dépenses et de revenus pour mieux comprendre votre situation financière.

## Prérequis
- **Python 3.8+**
- **PowerShell** (pour Windows)

## Installation et configuration

### Étape 1 : Télécharger l'application
Clonez ou téléchargez le dépôt Git contenant l'application sur votre ordinateur. Nous recommandons de placer l'application dans le chemin suivant :  
`C:\user\src\FAM`

```bash
git clone https://github.com/AmaProg/Fam.git
```

### Étape 2 : Ajouter le chemin de l'application aux variables d'environnement (Windows)
Pour faciliter l'utilisation de l'application via la ligne de commande, vous devez ajouter le chemin du dossier de l'application à vos variables d'environnement.

#### Instructions pour Windows 10 et 11 :
1. Faites un clic droit sur **Ce PC** et sélectionnez **Propriétés**.
2. Cliquez sur **Paramètres système avancés**.
3. Dans l'onglet **Avancé**, cliquez sur **Variables d'environnement**.
4. Dans la section **Variables système**, sélectionnez la variable **Path** et cliquez sur **Modifier**.
5. Ajoutez un nouveau chemin avec l'emplacement du dossier où l'application a été téléchargée (exemple : `C:\user\src\FAM`).
6. Cliquez sur **OK** pour valider.

### Étape 3 : Activer l'environnement de travail
Pour activer l'environnement virtuel et gérer les dépendances automatiquement, Ouvrez **PowerShell** et tapez la commande suivante :

```bash
activate
```

Une fois activé, vous pouvez tester que l'application fonctionne correctement avec :

```bash
fam -v
```

### Étape 4 : S'inscrire et se connecter à l'application
1. **Créer un compte** :
   ```bash
   fam signup
   ```
2. **Se connecter** :
   ```bash
   fam login
   ```

### Étape 5 : Ajouter des relevés bancaires
Ajoutez vos relevés de compte sous forme de fichiers CSV avec la commande suivante :

```bash
fam add statement
```

### Étape 6 : Générer une facture
Pour créer une facture à partir de vos données financières, exécutez :

```bash
fam invoice build
```

## Support
Si vous rencontrez des problèmes ou avez des questions, n'hésitez pas à consulter la documentation ou à ouvrir une issue sur le dépôt GitHub.

## Remarque
Actuellement, seules les banques **BMO** et **Tangerine** sont prises en charge.
