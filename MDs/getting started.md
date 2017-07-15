# Einführung

Diese Einführung zeigt, wie man mit EngineL ein eigenes Textadventure erstellt. Wenn Sie mit diesem Tutorial fertig sind, haben Sie ein kleines fertiges Spiel, was Sie nach belieben erweitern können.

## Installation

Um vernünftig mit EngineL arbeiten zu können, benötigen Sie Visual Studio Code, Python, PyQt5 und Pylint. Obwohl dir Nutzung von EngineL auf allen Systemen gleich ist, unterscheidet sich die Installation sehr, führen Sie daher die für Ihr System passende Anleitung aus!

#### Windows

1. Laden Sie Python 3.6.1 [hier](https://www.python.org/downloads/) herunter und starten Sie den Installer!
2. Klicken Sie auf "Install Now". Wenn die Meldung "Setup was successfull" erscheint, können Sie das Fenster schließen.
4. Laden Sie sich VS Code [hier](https://code.visualstudio.com/docs/?dv=win) herunter und führen Sie das Installationsprogramm aus.
5. Ist die Installation abgeschlossen, starten Sie VS Code und öffnen den Erweiterungstab (linker Rand, das fünfte Symbol von oben).
6. Suchen Sie nach der Erweiterung "Python" und drücken Sie auf "Installieren". Nach einem Moment erscheint an der Stelle des "Installieren"-Knopfes ein "Neustarten"-Knopf, den Sie dann drücken.
7. Drücken Sie Strg+ö sobald VS Code wieder gestartet ist und geben in dem sich öffnenden Terminal den Befehl `py.exe -m pip install pylint PyQt5` ein.

#### Ubuntu

1. Laden Sie sich VS Code [hier](https://code.visualstudio.com/docs/?dv=linux64_deb) herunter und installieren Sie das Paket mit ihrem Software-Manager.
2. Ist die Installation abgeschlossen, starten Sie VS Code und öffnen mit Strg+Umschalt+´ ein Terminal. Geben dort den Befehl `sudo apt-get update && sudo apt-get install python3 python3-pyqt5 pylint` ein.
3. Öffnen Sie anschließend den Erweiterungstab (linker Rand, das fünfte Symbol von oben) und suchen dort nach der Erweiterung "Python". Installieren Sie diese und starten VS Code neu!

#### Fedora

1. Laden Sie sich VS Code [hier](https://code.visualstudio.com/docs/?dv=linux64_rpm) herunter und installieren Sie das Paket mit ihrem Software-Manager.
2. Ist die Installation abgeschlossen, starten Sie VS Code und öffnen mit Strg+Umschalt+´ ein Terminal. Geben dort den Befehl `sudo dnf install python3 python3-qt5 pylint` ein.
3. Öffnen Sie anschließend den Erweiterungstab (linker Rand, das fünfte Symbol von oben) und suchen dort nach der Erweiterung "Python". Installieren Sie diese und starten VS Code neu!