# Pironman 5 OLED tekst — testversie

Stop de originele Pironman-add-on (inclusief watchdog en automatisch starten)
voordat je deze start. Er mag maar één hardwarebesturing actief zijn.

Deze versie voegt `/api/v1.0/set-oled-text`, `clear-oled-text` en `get-oled-text`
toe op poort 34001. Gebruik voor Node-RED de hostnaam van DEZE add-on.

Voorbeeld POST naar set-oled-text:
`{"lines":["Hallo!"],"duration":30}` met Content-Type application/json.

Zie LEESMIJ.md in het downloadpakket voor installatie, instellingenovername,
Node-RED, testresultaten en terugschakelen. Tien lokale softwaretests geslaagd; een eerste gebruiker heeft tekstweergave
en terugkeer naar het standaardscherm op een Pi bevestigd. Verdere hardwaretests blijven nodig.
