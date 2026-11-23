# GeniControl unter Python 3 / wxPython 4

## Installation

**Raspberry Pi OS / Debian:**

```bash
sudo apt install python3-wxgtk4.0 python3-yaml python3-serial
```

**Windows** (Python 3 von python.org):

```bat
py -m pip install wxPython pyyaml pyserial
```

Weitere Pakete (pypubsub o. ä.) werden nicht benötigt.

## Start

```bash
cd GENIBus/tools/genicontrol
python3 GeniControl.py          # Windows: py GeniControl.py
```

Über SSH (Linux): `ssh -Y pi@raspberrypi`, dann wie oben.

## Verbindung einstellen

Menü **Extras → Options**:

* **Serial Port** – RS485-Adapter (9600 Baud, 8N1), z. B. `/dev/ttyUSB0` bzw. unter Windows `COM3`
  (Nummer im Geräte-Manager unter „Anschlüsse (COM & LPT)“)
* **Arduino / TCP** – Arduino-Passthrough-Server (IP/Port)
* **Simulator** – emulierte Pumpe, ohne Hardware

Die Einstellung wird beim Beenden gespeichert und gilt ab dem **nächsten Start**.
Alternativ die Datei direkt bearbeiten – `~/GeniControl/GeniControl.cfg`
(Windows: `%USERPROFILE%\GeniControl\GeniControl.cfg`):

```ini
[network]
driver = 2          # 0 = Simulator, 1 = Arduino/TCP, 2 = serielle Schnittstelle

[serial]
serialport = /dev/ttyUSB0     # Windows: COM3
```

Linux: Der Benutzer braucht Zugriff auf die serielle Schnittstelle:
`sudo usermod -aG dialout $USER` (danach neu anmelden).
Läuft ein anderes Programm auf derselben Schnittstelle (z. B. ein MQTT-Dienst),
muss es vorher gestoppt werden.

## Hinweise zur Bedienung (MAGNA3)

* Der Knopf **Remote/Local** zeigt die aktuelle Steuerquelle (grün = Remote/GENIbus).
  Beim Umschalten auf Remote wird der Bus-Sollwert mitgesendet – die MAGNA übernimmt
  einen gespeicherten Bus-Sollwert sonst nicht.
* Regelarten (Control-Mode) wirken nur im Remote-Modus; GeniControl fragt ggf. nach.
* Remote-Modus und Bus-Sollwert bleiben in der Pumpe gespeichert. Vor dem Beenden auf
  **Local** schalten, wenn die Pumpe wieder mit dem an ihr eingestellten Sollwert laufen soll.
* Sollwerte: Meter in Konstant-/Proportionaldruck und AutoAdapt, Prozent in Konstantfrequenz.
