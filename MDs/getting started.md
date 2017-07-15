# Einführung

Diese Einführung zeigt, wie man mit EngineL ein eigenes Textadventure erstellt. Wenn Sie mit diesem Tutorial fertig sind, haben Sie ein kleines fertiges Spiel, was Sie nach belieben erweitern können.

## Installation

Um vernünftig mit EngineL arbeiten zu können, benötigen Sie Visual Studio Code (kurz "VS Code"), Python, PyQt5 und Pylint. Obwohl dir Nutzung von EngineL auf allen Systemen gleich ist, unterscheidet sich die Installation sehr, führen Sie daher die für Ihr System passende Anleitung aus!

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

## Erstellen des Projektes

Zuerst laden Sie sich den Quellcode der aktuellen Version von EngineL herunter, den Sie auf der [Releaseseite ](https://github.com/Janonard/EngineL/releases) finden. Entpacken Sie das Archiv in einem Ordner ihrer Wahl, wenn Sie möchten, auch in einem Git-Repository. Öffnen Sie dann in VS Code über die Reiter "Datei -> Ordner öffnen" den Ordner. Auf der linken Seite finden Sie dann im Explorer alle Dateien des Ordners. Damit haben Sie ihr Projekt auch schon angelegt!

## Etwas Theorie vorweg

EngineL nutzt zum Beschreiben der Spielwelt einen [Baum](https://de.wikipedia.org/wiki/Baum_(Datenstruktur)). Jeder Gegenstand im Spiel ist ein Knoten in diesem Baum und kann ein Elternteil und beliebig viele Kinder haben. Wenn zum Beispiel auf einem Balkon ein Kaktus, ein Tisch und Sie selbst stehen, dann sind Sie, der Tisch und der Kaktus Kinder vom Balkon. Möchte Sie man den Kaktus aufnehmen, müssen Sie das Elternteil des Kaktus' vom Balkon zu sich selbst änern und schon haben Sie, zumindest in der Spiellogik, den Kaktus aufgenommen.

Um diese Konstellation mit ihrer Variablität zu beschreiben, gibt es drei Grundklassen: `Entity`, `StaticEntity`, `Place` und `Player`. `Entity` ist die absolute Grundklasse und ermöglicht die Verwaltung von Kindern und die Transfers. `StaticEntity` ist eine Kindklasse von `Entity` und für den Sonderfall gedacht, dass ein Gegenstand unbeweglich ist, da diese jegliche Tranferversuche als Subjekt ablehnt. `Place` ist ebenfalls eine Kindklasse von `Entity` und ermöglicht Transfers zu anderen Orten und zu guter letzt ist ein Objekt der Klasse `Player`, ebenfalls ein Kind von `Entity`, die spielinterne Darstellung des Spielers bzw. der Spielfigur.

Das sollte für's erste an Theorie reichen.

## Das erste Spiel

Jetzt geht es endlich um das eigentliche Spiel! Öffnen Sie zuerst VS Code, falls es nicht schon offen ist.

Öffnen Sie den Debugging-Tab auf der linken Seite und wählen Sie oben im Drop-down-Menü die Option "EngineL without saving" aus. Wenn Sie auf den grünen Pfeil drücken, erscheint auch schon das Spielfenster! Besonders viel zu tun gibt es zwar nicht, aber es zeigt, dass alles funktioniert.

Der Titel des Fensters lautet bei Ihnen wahrscheinlich "Ort | EngineL" und im Textfeld steht "Ein Ort, aber man kann nirgendwo hingehen." Der Fenstertitel gibt den Namen Ihres aktuellen Standortes an und das Textfeld nennt die Beschreibung dieses Ortes und beides können Sie ändern: Öffnen Sie in VS Code den Explorer und öffnen die Datei `Resources/world.xml`. Diese Datei enthält einen XML-Text und sollte diesen Abschnitt enthalten:

    <safe>
        <Place name="Ort" description="Ein Ort" gender="m">
            <children>
                <Player />
            </children>
        </Place>
    </safe>

Diese Datei beschreibt die Ausgangslage des Spiels. Aktuell gibt es einen Ort (`Place`) mit dem Namen "Ort", der Beschreibung "Ein Ort" und dem grammatischen Geschlecht "m", also "maskulin". Ebenfalls hat dieser Ort ein Kind, nämlich den Spieler (`Player`). Ändern Sie doch mal den Namen und die Beschreibung des Ortes in etwas anderes, interessanteres, vielleicht zu "Balkon"! Wenn Sie das Spiel nochmal starten, werden Sie dann das angezeigt bekommen. Der Teil ", aber man kann nirgendwo hingehen." wird übrigens automatisch generiert und angehängt, Sie brauchen sich darum also nicht zu kümmern.

Als nächstes fügen wir den Kaktus hinzu: Schreiben Sie zwischen die `<children>`-Tags diese Zeile:

    <Entity name="Kaktus" description="Mein kleiner grüner Kaktus, der draußen am Balkon steht" gender="m" />

Starten Sie das Spiel nochmal! Die Beschreibung sagt jetzt auch, dass da ein Kaktus ist. Gucken Sie sich den Kaktus einmal an, indem Sie den Befehl "sieh zum Kaktus" in die Eingabezeile unten eingeben. Auch jetzt sollte die eingebene Beschreibung sichtbar sein. Dann können Sie den Kaktus auch mit "nimm den Kaktus" aufnehmen und ihn in Ihrer Tasche ("sieh zur Tasche") sehen. Sie haben gerade das gemacht, was schon in der Theorie beschrieben wurde: Sie haben den Kaktus auf sich selbst transferiert und nun sind Sie bzw. der Spieler das Elternteil des Kaktus'.