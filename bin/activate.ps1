# setup.ps1
# Obtenir le répertoire du fichier script
$SCRIPT_DIR = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent

# Obtenir le répertoire parent
$PARENT_DIR = Join-Path -Path $SCRIPT_DIR -ChildPath ".."

# Créer le répertoire .venv dans le répertoire parent
if (Test-Path "$PARENT_DIR\.venv") {

    Write-Output "The virtual environment already exists in $PARENT_DIR. Activating..."

    # Activer l'environnement virtuel
    . "$PARENT_DIR\.venv\Scripts\Activate.ps1"

} else {
    Write-Output "Creating the virtual environment in $PARENT_DIR.."
    python -m venv "$PARENT_DIR\.venv"
    # Activer l'environnement virtuel
    . "$PARENT_DIR\.venv\Scripts\Activate.ps1"


    # Installer les dépendances depuis requirements.txt dans le répertoire parent
    if (Test-Path "$PARENT_DIR\requirements.txt") {
        pip install -r "$PARENT_DIR\requirements.txt"
    } else {
        Write-Output "requirements.txt non trouvé dans $PARENT_DIR."
    }

    python.exe -m pip install --upgrade pip
}


# # Ajouter un chemin à la variable d'environnement PATH
# $NEW_PATH = "$PARENT_DIR\.venv\Scripts"
# Write-Output "Ajout du chemin $NEW_PATH à la variable d'environnement PATH."

# # Ajouter le chemin à la variable PATH pour la session en cours
# $env:Path += ";$NEW_PATH"

# # Ajouter le chemin à la variable PATH pour les sessions futures
# [System.Environment]::SetEnvironmentVariable("Path", "$env:Path", [System.EnvironmentVariableTarget]::Machine)

# Garder la session PowerShell active
Write-Output "The virtual environment is activated. You can now work in this PowerShell session."