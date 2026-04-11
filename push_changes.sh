#!/bin/bash

# 1. Verzeichnis scannen und Status anzeigen
echo "--- Aktueller Git Status ---"
git status -s
echo "----------------------------"

# 2. Dateien hinzufügen
git add .

# 3. Den Benutzer nach der Commit-Nachricht fragen
# Wir schlagen deinen Standard vor, aber du kannst ihn überschreiben
DEFAULT_MSG="update"

echo "Bitte Commit-Nachricht eingeben (Enter für Standard):"
echo "Standard: $DEFAULT_MSG"
read -r USER_INPUT

# Wenn die Eingabe leer ist, nimm den Standard
if [ -z "$USER_INPUT" ]; then
    COMMIT_MSG="$DEFAULT_MSG"
else
    COMMIT_MSG="$USER_INPUT"
fi

# 4. Bestätigung vor dem Push
echo ""
echo "Bereit zum Committen mit Nachricht: \"$COMMIT_MSG\""
echo "Fortfahren? (y/n)"
read -r CONFIRM

if [ "$CONFIRM" != "y" ]; then
    echo "Abgebrochen. Nichts wurde hochgeladen."
    exit 1
fi

# 5. Ausführen
git commit -m "$COMMIT_MSG"
git push origin main

echo "--- Fertig! Alles ist auf GitHub. ---"
