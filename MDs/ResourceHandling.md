# Verwaltung von Strings {#resourcehandling}

In den vorherigen Tutorials haben Sie schon mehrfach mit Zeichenketten (strings) gearbeitet, die direkt auf dem Bildschirm ausgegeben werden. Für die ersten Experimente ist das noch Okay, aber stellen Sie sich vor, Sie erstellen ein großes Projekt, das in mehrere Sprachen übersetzt werden soll und dazu noch literarisch sehr anspruchsvoll ist. Ihr Quellcode würde dann von langen Zeichenketten überschwellen, die zum einen relativ schwierig wiederzufinden sind und zum anderen die Bedeutung des Quelltextes verschleiern.

Sie sehen, der Ansatz ist nicht sonderlich effektiv. Dafür bietet EngineL den String Resources Manager (hier kurz SRM) an, ein Objekt, das über die Spielinstanz immer verfügbar ist und als eine Art Wörterbuch fungiert: Man gibt ihm einen Schlüssel und er gibt einen den vollständigen Text zurück. Auch kann er einen Text mit mehreren Schlüsseln übersetzen.

Die dafür nötigen Resourcen liegen in einer eigenen Datei: `Resources/strings.xml`. Bei einem frisch erstellten Projekt enthält diese vor allem Textfragmente, die von der Engine selbst benötigt werden, um Befehle zu entschlüsseln oder Inventarlisten zu generieren. Ganz am Ende der Vorlage befinden sich die `game`-Tags, in denen Sie ihre Texte anlegen können.

### Anpassen des Balkons

Nehmen Sie sich noch einmal das Spielchen aus der \ref einfuehrung. In ihrer `Resources/world.xml` sind alle Texte fest eingebaut. Fangen wir doch damit an, jeden Text in die `strings.xml` aufzunehmen. Beispielsweise könnte innerhalb Ihrer `game`-Tags folgendes stehen:

    <game>
        <balcony>
            <name bold="True">Balkon</name>
            <desc>Der Balkon geht zur Straße hinaus</desc>
        </balcony>
        <cactus>
            <name bold="True">Kaktus</name>
            <desc>Mein kleiner grüner Kaktus, der draußen am Balkon steht</desc>
        </cactus>
        <table>
            <name bold="True">Tisch</name>
            <desc>Ein Tisch aus Holz</desc>
        </table>
        <livingroom>
            <name bold="True">Wohnzimmer</name>
            <desc>Das ist mein Wohnzimmer</desc>
        </livingroom>
    </game>

Jetzt haben Sie eine komplette und geordnete Auflistung von allen Strings, die in der `world.xml` benötigt werden. Wie Sie das alles ordnen ist Ihnen überlassen, der SRM achtet nicht besonders darauf, nur müssen Namen immer die Eigenschaft `bold="True"` haben, damit sie im Spiel fett gedruckt werden.

Wie greifen Sie jetz aber auf diese Texte zu? Der Schlüssel eines Textes setzt sich aus den XML-Elementen zusammen, in dem er steht, also hätte der Text "Balkon" den Schlüssel `game.balcony.name`. Damit der SRM aber eindeutig erkennen kann, dass es sich um einen Schlüssel handelt, müssen um den Schlüssel noch Erkennungsklammern gesetzt werden: `${game.balcony.name}`. Jetzt können Sie in der `world.xml` jeden Text mit seinem Schlüssel ersetzen. Sie werden sehen, dass die Zeilen insgesamt deutlich kürzer werden!

Wenn Sie das Tutorial zu den \ref events gemacht haben, haben Sie auch Text innerhalb der Spiellogik verwendet und zwar wenn Sie den Kaktus benutzen. Auch dieser Text kann und sollte in die `strings.xml` aufgenommen werden! Fügen Sie ihn ersteinmal irgendwo in der `strings.xml` hinzu und ersetzen dann den Text in der Spiellogik mit dessen Schlüssel (Klammern nicht vergessen!). Bevor der Text ausgegeben wird, geht der SRM nochmal darüber und ersetzt mögliche Schlüssel.

Wenn Sie anderweitig Text aus der `strings.xml` brauchen, können Sie den SRM auch direkt aufrufen: Wenn Sie das `Core`-Modul von EngineL importiert haben, können Sie über `Core.get_res_man().decode_string(ihr_text)` jederzeit ihren Text decodieren lassen.