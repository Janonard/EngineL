# Einführung {#einfuehrung}

Diese Einführung zeigt, wie man mit EngineL ein eigenes Textadventure erstellt. Wenn Sie mit diesem Tutorial fertig sind, haben Sie ein kleines Spiel, was Sie nach belieben erweitern können. Bevor Sie damit anfangen, sollten Sie sicherstellen, dass alle benötigten Programme installiert sind (@ref installation).

## Erstellen des Projektes

Zuerst laden Sie sich den Quellcode der aktuellen Version von EngineL herunter, den Sie auf der [Releaseseite](https://github.com/Janonard/EngineL/releases) finden. Entpacken Sie das Archiv in einem Ordner ihrer Wahl, wenn Sie möchten, auch in einem Git-Repository. Öffnen Sie dann in VS Code über die Reiter "Datei -> Ordner öffnen" den Ordner. Auf der linken Seite finden Sie dann im Explorer alle Dateien des Ordners. Damit haben Sie ihr Projekt auch schon angelegt!

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

Der Balkon braucht noch einen Tisch! Probieren Sie einmal selbst aus, den Tisch in die Datei zu schreiben. Von der Form her funktioniert das genauso wie bei dem Kaktus, nur dass Sie jetzt statt der Klasse `Entity` die Klasse `StaticEntity` benutzen sollten. Sind Sie damit fertig, können Sie das Ganze mal ausprobieren, wobei Sie den Tisch nicht aufnehmen können.

Als letzter Schritt für diese Einleitung fügen wir noch einen weiteren Ort, das Wohnzimmer, hinzu, das man über den Balkon betreten kann. Als erstes kommt der Ort selbst: Alle Orte in EngineL sind im "Weltenbaum" auf einer Ebene, also nebeneinander. Fügen Sie also im Text der `world.xml` über dem Balkon diese zwei Zeilen hinzu:

    <Place name="Wohnzimmer" description="Das ist mein Wohnzimmer" gender="n">
    </Place>

Wenn Sie das Spiel aber jetzt starten, werden Sie sehen, dass man noch nicht zu diesem Ort gehen kann. Um von einem Ort zu einem Anderen zu kommen, müssen diese miteinander verbunden sein, nach Möglichkeit in beide Richtungen. Fügen Sie also innerhalb den `Place`-Tags des Wohnzimmers die Zeile `<connection name="Balkon" />` und zwischen die des Balkons `<connection name="Wohnzimmer" />` ein. Die fertige Datei könnte dann in etwa so aussehen:

    <safe>
        <Place name="Wohnzimmer" description="Das ist mein Wohnzimmer" gender="n">
            <connection name="Balkon" />
        </Place>
        <Place name="Balkon" description="Der Balkon geht zur Straße hinaus" gender="m">
            <children>
                <StaticEntity name="Tisch" description="Ein Tisch aus Holz" gender="m" />
                <Entity name="Kaktus" description="Mein kleiner grüner Kaktus, der draußen am Balkon steht" gender="m" />
                <Player />
            </children>
            <connection name="Wohnzimmer" />
        </Place>
    </safe>

Damit sind wir auch schon fertig! Am besten machen Sie jetzt mit den @ref events weiter.