# Nope - KI Spieler (Python)
Kurze Beschreibung des Repos und der übergreifenden Schnittstelle für die unterschiedlichen Clients.

## Mitglieder 
Mitglied | entwickelter Client |  
--- | --- | 
[Dennis Edler](https://github.com/deedz-x) | Client1

## Dokumentation
[Link zum Doku-Ordner](https://github.com/Nope-Cardgame/Doku)

## Struktur des Codes

Die finale Abgabe besteht aus drei Ordnern mit relevanten Dateien für Klassen und Funktionen, sowie einer ausführbaren [main-Datei](https://github.com/Nope-Cardgame/KIPython1/blob/main/main.py) um den Client zu starten. Diese umfasst ein Konsolen-Menü welches es dem User ermöglicht sich Anzumelden oder zu registrieren und anschließend Spiele oder Turniere zu starten. Dabei können Einladungen entweder gezielt an einzelne oder an alle verbundenen Clients gesendet werden.
Neben der main.py befinden sich hier noch weitere auführbare Dateien: Eine test.py (welche irrelevant für die Abgabe ist und nur für interne, lokale Tests verwendet wurde) sowie eine TestClient.py, welche auf einem anderen Gerät genutzt wurde um schnell einen zweiten Client ohne die Menüs einzuloggen und zu einem Spiel einzuladen.

Im [Socket-Order](https://github.com/Nope-Cardgame/KIPython1/tree/main/Socket) befindet sich die Datei [Connection.py](https://github.com/Nope-Cardgame/KIPython1/blob/main/Socket/Connection.py). In dieser finden sich alle relevanten Funktionen für die Kommunikation mit der REST-API sowie SocketIO. 
Die ersten 212 Zeilen sind Funktionen für die Kommunikation mit den, in der [Dokumentation](https://github.com/Nope-Cardgame/Doku/blob/main/Schnittstellen/Schnittstellen.md#rest-api) definierten, REST-API Schnittstellen, die folgenden händeln die [SocketIO Events](https://github.com/Nope-Cardgame/Doku/blob/main/Schnittstellen/Schnittstellen.md#events). Die Funktionen in Zeile 215-228 bearbeiten die Events welche vom Client gesendet werden, also das playAction und ready Event, die nachfolgenden bearbeiten die empfangenen Events.

Im [Misc-Ordner](https://github.com/Nope-Cardgame/KIPython1/tree/main/Misc) befinden sich vier Dateien welche hauptsächlich Klassen und Objekte beinhalten und verarbeiten:
- Die Datei [Globals.py](https://github.com/Nope-Cardgame/KIPython1/blob/main/Misc/Globals.py) umfasst nur eine Zeile und wurde als Hilfsdatei implementiert um ein globales, in allen Dateien und Funktionen nutzbares User-Objekt zu erstellen. Dies war notwendig, da Python ansonsten nur Referenzen eines Objekten erstellt und Attribute nicht zuverlässig gespeichert/geändert werden.
- Die Datei [Bearer-Auth.py](https://github.com/Nope-Cardgame/KIPython1/blob/main/Misc/BearerAuth.py) beinhaltet eine Klasse, welche ein einfacheres Authentifizieren bietet, da der Authentication Header korrekt geparsed wird. Die Idee und Vorlage für die Klasse kamen [hierher](https://requests.readthedocs.io/en/latest/user/authentication/#new-forms-of-authentication).
- Die Datei [User.py](https://github.com/Nope-Cardgame/KIPython1/blob/main/Misc/User.py) wurde als Klasse für einen User implementiert. Dieser wird beim registrieren/anmelden mit den benötigten Attributen erstellt und für das Senden von Requests (z.B. bei der Spielerstellung) sowie die Überprüfung des aktuellen Spielers verwendet.
- Die Datei [JSONObjects.py](https://github.com/Nope-Cardgame/KIPython1/blob/main/Misc/JSONObjects.py) beinhaltet Klassen für alle in der [Dokumentation](https://github.com/Nope-Cardgame/Doku/blob/main/Schnittstellen/Schnittstellen.md#objects) genannten und benötigten JSON-Objekte. Beim auslesen der Daten aus den empfangenen SocketIO Events werden Objekte der jeweiligen Klasse erstellt um einfacher auf Attribute zugreifen zu können.

Das Gehirn des KI-Clients befindet sich im [Logic-Ordner](https://github.com/Nope-Cardgame/KIPython1/tree/main/Logic). Dieser beinhaltet die [MainLogic.py](https://github.com/Nope-Cardgame/KIPython1/blob/main/Logic/MainLogic.py), welche alle Funktionen für Spielzüge enthält, sowie eine Datei [ideas](https://github.com/Nope-Cardgame/KIPython1/blob/main/Logic/ideas), in der (während der Arbeit am KI-Client) Ideen für die Umsetzung festgehalten wurden. Jedoch wurden nicht alle davon implementiert. Den Ablauf der KI-Logik finden Sie im Reflektionsdokument.


## Coding-Conventions
- Code und Dokumentation auf Englisch
- Dokumentation durch DocStrings in Funktions- oder Klassenkopf
- DocStrings in SphinxStyle
- Parameter und Rückgabetyp durch Type Hints in Funktion definieren
- Erläuterung der Parameter und des Rückgabewerts in DocString
- camelCase mit führendem lowercase Buchstaben für Variablen und Funktionen
- Sinnvolle, einmalige Namen für Variablen, Funktionen und Klassen
- KlassenNamen als camelCase mit führendem uppercase Buchstaben
- Zeilenumbrüche bei langen/vielen Parametern. Einrücken um Lesbarkeit zu vereinfachen
- Trennung der Funktionen durch zwei leere Zeilen
- Einzelne leere Zeile zur Trennung logischer Blöcke in einer Methode
- Whitespace zur besseren Lesbarkeit verwenden. [Hieran](https://peps.python.org/pep-0008/#pet-peeves) orientieren
- Kommentare als Block Comments. Inline Comment nur in Ausnahmefällen!
- Redundanten Code in Funktion auslagern

## Installation

Erklärung wie das Projekt ausgeführt wird

1. Installation von benötigten Softwarepakete (requests, python-socketio, websocket-client)
2. Klonen des GitHub-Repo
3. Ausführen der main.py

## Benutzung
Das Programm verfpgt über eine vollständiges Menü, welches in der Konsole dargstellt wird.
Durch Auswahl der Menüpunkte wird die entprechende Aktion, z.B. "Sign In" gestartet.

### Client1
Beschreibung der Bedienung für Client1 um ein NOPE Spiel zu spielen

### Client2
Beschreibung der Bedienung für Client2 um ein NOPE Spiel zu spielen
