# WP8 Arduino Staging Report

## Ziel

Lokales Library-Staging fuer die Legacy-Sketches unter `examples/` aufsetzen und den Compile-Status mit `arduino-cli` erneut pruefen.

## Durchgefuehrte Schritte

1. Lokale Library `Genibus` unter `~/Documents/Arduino/libraries/Genibus` angelegt.
2. Header aus `commlib/genibus/*.h` nach `.../Genibus/src/genibus/` kopiert.
3. Wrapper-Header in `.../Genibus/src/` erzeugt:
   - `Genibus.h`
   - `Types.h`
   - `Crc.h`
   - `GB_Datalink.h`
   - `Pdu.h` (temporärer Minimal-Wrapper)
4. `library.properties` fuer die lokale Staging-Library angelegt.
5. `Ethernet` via `arduino-cli lib install Ethernet` installiert.
6. Re-Compile fuer folgende Sketches ausgefuehrt:
   - `examples/example01`
   - `examples/example02`
   - `examples/example03`
   - `examples/passThruServer`
   - `examples/passThruServer328`

## Ergebnis des Re-Compiles

### Verbleibende Blocker

- `examples/passThruServer328`: `EtherShield.h` fehlt (externe Legacy-Library nicht installiert).
- `examples/example03`, `examples/passThruServer`: `GB_Datalink`-Klasse fehlt im aktuellen staged Header-Set.
- `examples/example01`, `examples/example02`: `Crc`-Klasse fehlt in der staged Form (aktueller Header exportiert nur C-APIs).
- Mehrfach: Konflikt mit `boolean`-Typ (`types.h` vs. Arduino Core `Arduino.h`).

### Interpretation

Das Staging hat Include-Fehler fuer `Genibus.h`/`Types.h`/`Crc.h` reduziert, aber die eigentliche Arduino-C++-API der alten GENIBus-Library ist im Repository nicht vollstaendig vorhanden.

## Empfohlene naechste Schritte

1. Fehlende Legacy-Header/Implementierungen aus historischem Arduino-Library-Stand nachziehen:
   - `GB_Datalink.h`
   - `Pdu.h`
   - C++-`Crc`-Klasse kompatibel zu den Sketches
2. `types.h` fuer Arduino-Umgebung guarden (kein eigenes `boolean`, wenn bereits im Core definiert).
3. Optional fuer 328er-Sketch:
   - passende `EtherShield`-Library installieren oder
   - `passThruServer328` aus der Standard-Build-Matrix ausnehmen.

## Follow-up: Header-Mapping und erweitertes Staging

### Umgesetzt

1. Historische Legacy-Header aus Git-Historie in lokales Staging uebernommen (`1113819395763cc95f39f535c76043a5df536b13`):
   - `commlib/Crc.h`
   - `commlib/GB_Datalink.h`
   - `commlib/Genibus.h`
   - `commlib/Types.h`
2. `Types.h` lokal fuer Arduino guarded (`typedef boolean` nur wenn `!defined(ARDUINO)`).
3. `Pdu.h` bleibt ein temporaerer Minimal-Stub, da keine echte Datei in der Historie gefunden wurde.
4. Re-Compile erneut ausgefuehrt fuer alle `examples/*` Sketches.
5. Historische Legacy-Implementierungen lokal uebernommen:
   - `commlib/Crc.cpp`
   - `commlib/GB_Datalink.cpp`
6. `Types.h` im lokalen Staging um `#include <Arduino.h>` ergaenzt, damit `boolean` in der Arduino-Toolchain sicher verfuegbar ist.

### Neuer Ergebnisstand

- `examples/example01`: Build erfolgreich.
- `examples/example02`: Build erfolgreich.
- `examples/example03`: Build erfolgreich.
- `examples/passThruServer`: Build erfolgreich.
- `examples/passThruServer328`: nach Migration auf `UIPEthernet` buildbar.

## Follow-up: EtherShield-Migration fuer 328

### Umgesetzt

1. `examples/passThruServer328/passThruServer328.ino` von `EtherShield` auf `UIPEthernet` migriert.
2. Low-level ENC28J60-API (`ES_*`) durch `EthernetServer`/`EthernetClient`-Fluss ersetzt.
3. `UIPEthernet` via `arduino-cli lib install UIPEthernet` installiert.
4. Re-Compile fuer `examples/passThruServer328` erfolgreich.

### Hinweise

- Der UNO-Build ist funktional erfolgreich, liegt aber mit globalen Variablen bei ~97% RAM-Auslastung (42 Bytes frei). 
- Fuer robusten Betrieb sollte perspektivisch RAM reduziert oder ein Board mit mehr SRAM genutzt werden.

### Schlussfolgerung

Das lokale Staging deckt die Legacy-GENIBus-API nun fuer alle Example-Sketches ab (inklusive migriertem `passThruServer328`).

