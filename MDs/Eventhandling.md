# Events in EngineL {#events}

In der vorherigen @ref einfuehrung haben Sie einen Prototyp für ein Textadventure angelegt. In diesem Tutorial werden Sie eigene Klassen für die Gegenstände im Spiel anlegen, die auf verschiedene Aktionen des Spielers reagieren können.

## Prototypisierung

Fangen wir damit an, Prototypen für die jeweiligen Klassen zu erstellen: Legen Sie im 
`Game`-Ordner ihres Projektes eine Datei mit dem Namen `Balcony.py` an und öffnen diese. In dieser Datei sollen alle Klassen enthalten sein, die für den Balkon notwendig sind. 

Schreiben Sie in die erste Zeile `from EngineL import Core`, um das `Core`-Modul zu importieren. Anschließend kommen die einzelnen Klassen:

    class Balcony(Core.Place):
        def __init__(self, parent=None):
            Core.Place.__init__(self, parent)
    
    class Cactus(Core.Entity):
        def __init__(self, parent=None):
            Core.Entity.__init__(self, parent)
    
    class Table(Core.StaticEntity):
        def __init__(self, parent=None):
            Core.StaticEntity.__init__(self, parent)
    
Die Konstruktoren müssen immer überschrieben werden und als Keyword-Argument den Vater bekommen. 


Als nächstes muss dafür gesorgt werden, dass diese Klassen vom Spiel erkannt werden. Dafür benötigt unser `Balcony`-Modul noch diese Funktion:

    def register_entity_classes(app):
        app.register_entity_classes([Balcony, Cactus, Table])

Öffnen Sie nun die Datei `__init__.py` und schreiben unter `import EngineL` die Zeile `import Game.Balcony` und anstelle von `# Place your class registrations here!` schreiben Sie `Game.Balcony.register_entity_classes(self)`.

Was genau passiert hier? Wenn das Spiel gestartet wird, wird eine Instanz der Klasse `GameApp` erstellt, die das Spiel im Allgemeinen repräsentiert. Diese Klasse registriert während des Ladevorganges alle `Enitity`-Klassen um diese in der `world.xml` oder Speicherständen zu erkennen. Allerdings muss Sie nicht jede einzelne Klasse auflisten, stattdessen wird einfach das Modul importiert und die `register_enitity_classes`-Funktion des Moduls führt dann die eigentliche Registrierung durch.

Da die Klassen jetzt erkannt werden, können wir diese in der `world.xml` benutzen: Öffnen Sie diese und ersetzen die Tag-Namen der jeweiligen Gegenstände mit den Namen der Klassen. Wenn Sie das Spiel jetzt starten, sollte alles so sein wie vorher.

## Eigene Aktionen

Jetzt kommt der interessante Teil: Die Möglichkeit, auf Aktionen des Spielers zu reagieren! Fangen wir einfach an: Öffnen Sie das `Balcony`-Modul und ändern Sie die `Cactus`-Klasse wie folgend ab:

    class Cactus(Core.Entity):
        def __init__(self, parent=None):
            Core.Entity.__init__(self, parent)
            self.activly_usable = True
        
        def on_used(self, user, other_entity=None):
            user.get_window().show_text("Autsch! Warum sind die Stacheln so spitz?!")
            return True

Die Methode `on_used` wird aufgerufen, wenn der Spieler den Befehl "benutze Kaktus" anwendet. Der `user` ist dabei der, der den Befehl ausgeführt hat, was im Normalfall der Spielert ist. Wird also der Kaktus benutzt, kriegt der Spieler den oben genannten Text ausgegeben. Probieren Sie es ruhig aus!

Weitere Möglichkeiten, Ihren Code zu erweitern, finden Sie in der [Dokumentation](https://janonard.github.io/EngineL-docs/): Neben dem schon verwendeten [`on_used`](https://janonard.github.io/EngineL-docs/classEngineL_1_1Core_1_1Entity.html#aa45c987efe03adb3037fccb66d5c8d69) ist auch [`on_transfer`](https://janonard.github.io/EngineL-docs/classEngineL_1_1Core_1_1Entity.html#ab91a29dd97d404d093899f77a209eb2f) und [`on_game_launched`](https://janonard.github.io/EngineL-docs/classEngineL_1_1Core_1_1Entity.html#aff2b9c988f98888b5460c35c715149ec) interessant. EngineL bietet übrigens auch die Möglichkeit, Dialoge bzw. geskriptete \ref scene wiederzugeben.