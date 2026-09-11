# Pironman 5 OLED-tekst — testversie 0.1.1

Dit is een lokaal te bouwen Home Assistant-add-on voor Pironman 5 met
pironman5 1.2.6, pm_auto 1.2.5 en pm_dashboard 1.2.6. Het pakket bevat broncode,
een Dockerfile, een Node-RED-flow en tests. De eerste gebruiker heeft versie 0.1.1 op een Pi geïnstalleerd en bevestigd
dat tekstweergave en terugkeer naar het standaardscherm lijken te werken. Installeer dit als testversie, met de originele
add-on beschikbaar om terug te schakelen.

## Mogelijkheden

- Een tot vier regels tekst op het bestaande 128 × 64 OLED.
- duration: 30 toont een bericht 30 seconden; duration: 0 blijft staan.
- Een nieuw bericht vervangt het vorige; clear herstelt het standaardscherm.
- Lange regels worden ingekort met drie punten. Printbare ASCII en ° worden ondersteund.
- Een slapend, ingeschakeld scherm wordt tijdens een bericht wakker gehouden.
- Een bewust uitgeschakeld OLED weigert tekst met HTTP 409. OLED uitschakelen wist de tekst.
- De weergave verandert bij de volgende hardwarecyclus, normaal binnen circa een seconde.
- Tekst wordt alleen in het geheugen bewaard; een herstart wist de tekst.
- RGB, dashboard en ventilatorregeling blijven via de bestaande software lopen.

## Installeren

1. Pak de ZIP uit op je computer. Bewaar de originele Pironman-add-on en maak
   vooraf een Home Assistant-back-up van die add-on.
2. Kopieer de map `pironman5_text` naar de Home Assistant-map `/addons`.
   Het resultaat moet `/addons/pironman5_text/config.yaml` zijn.
   Met de Samba share-add-on op Windows is dit doorgaans de share
   `\\HOME_ASSISTANT_IP\addons`. Gebruik je eigen Home Assistant/Samba-aanmelding.
   Is die share niet beschikbaar, gebruik een SSH/SFTP-omgeving met toegang tot `/addons`.
   De map heet `addons`, niet `addon_configs` of de gewone Home Assistant-configuratiemap.
3. Open Instellingen → Add-ons (of Apps) → Winkel → ⋮ → Controleren op updates.
   Onder Lokale add-ons/apps verschijnt **Pironman 5 OLED tekst (test)**.
4. Klik Installeren. Home Assistant bouwt de container met het officiële ARM64
   basisimage. Dit vereist internet en kan enkele minuten duren. Laat de
   originele add-on tijdens alleen het bouwen nog draaien.
5. Optioneel: neem bestaande instellingen over vóór de eerste start; zie hieronder.
6. Zet bij de ORIGINELE add-on zowel 'Bij systeemstart starten' als 'Watchdog' uit,
   en stop hem. Start daarna pas de test-add-on. Laat nooit beide tegelijk draaien:
   ze bedienen dezelfde GPIO/I2C/SPI-hardware en ventilatoren.
7. Controleer het logboek van de test-add-on. Verwacht de drie versies en
   `OLED text extension 0.1.1 ready; API port 34001`.
   Bij een fout: stop de test-add-on en start de originele opnieuw.
8. Controleer dat dashboard, ventilatoren en het normale OLED werken.
   Laat automatisch starten voor de testversie voorlopig uit.

Deze procedure volgt de officiële lokale-appinstallatie:
https://developers.home-assistant.io/docs/apps/tutorial/

## Bestaande instellingen meenemen (optioneel)

De nieuwe add-on heeft eigen opslag en begint anders met SunFounder-standaardinstellingen.
Lees vóór het stoppen van de originele add-on de configuratie:

```sh
curl --max-time 10 http://ORIGINAL_ADDON_HOST:34001/api/v1.0/get-config
```

Bewaar alleen het object onder `data` als `initial-config.json`, dus
`{"system":{...}}`, niet de omhullende `{"data":...,"status":true}`.
Plaats dit vóór de eerste start in de configuratiemap van de nieuwe add-on:
`/addon_configs/local_pironman5_text/initial-config.json` op de host (via Samba:
share `addon_configs`, map `local_pironman5_text`). Binnen de add-on is dit
`/config/initial-config.json`. De import gebeurt alleen zolang de nieuwe interne
`/data/config.json` nog niet bestaat. Het originele bestand wordt niet aangepast.
Je hoeft deze configuratie niet in de chat te delen.

## Eerste verbindingstest

De nieuwe add-on heeft een ANDERE hostnaam. Controleer deze op zijn informatiepagina.
Voor een lokale installatie wordt `local-pironman5-text` verwacht.
Vanaf de Home Assistant SSH-add-on:

```sh
curl --max-time 10 http://local-pironman5-text:34001/api/v1.0/test
curl --max-time 10 http://local-pironman5-text:34001/api/v1.0/get-oled-text
```

Vervang de hostnaam als Home Assistant een andere vermeldt. Poort 34001 is
standaard alleen intern bereikbaar; een extra poort op HOME_ASSISTANT_IP is niet nodig.
De API gebruikt, net als het originele dashboard, geen aparte authenticatie.
Publiceer deze niet op het internet.

## Node-RED

Importeer `node-red-oled.json` met Menu → Import → select a file en klik Deploy.
De flow is voor Node-RED als add-on op dezelfde Home Assistant-installatie.
Controleer de hostnaam in de function-node **BASE URL en JSON**.
Er zijn vier handmatige knoppen: tijdelijke tekst, blijvende tekst,
standaardscherm en tekststatus. Er wordt niets automatisch bij Deploy verstuurd.
De getoonde temperatuur/verbruik zijn voorbeeldwaarden, geen gekoppelde sensoren.

Voor een echte sensor kun je in een function-node bijvoorbeeld instellen:

```javascript
const value = Number(msg.payload);
if (!Number.isFinite(value)) return null;
msg.payload = {lines: ["Woonkamer", "Temperatuur: " + value.toFixed(1) + " C"], duration: 0};
msg.method = "POST";
msg.topic = "set-oled-text";
return msg;
```

Verbind die node met **BASE URL en JSON**. Gebruik de sensorwaarde als invoer.
Bij herstart verdwijnt een blijvend bericht; stuur dan de actuele waarde opnieuw.

## API

Basis: `http://local-pironman5-text:34001/api/v1.0/`

| Methode | Pad | Inhoud |
|---|---|---|
| POST | set-oled-text | `{"lines":["Hallo!"],"duration":30}` |
| POST | clear-oled-text | `{}` |
| GET | get-oled-text | geen |

Verstuur JSON met `Content-Type: application/json`. Maximaal vier regels,
80 tekens per regel vóór visuele inkorting, duration 0–86400 seconden.
Een geldig verzoek geeft HTTP 200 en `status:true`; dat bevestigt verwerking,
niet dat het fysieke display getest is. HTTP 400: ongeldige inhoud; 409:
OLED uit/niet klaar; 413: te groot; 503: geen OLED-object.

## Terugschakelen

Stop de test-add-on; zet diens automatisch starten/watchdog uit als je die had
ingeschakeld. Start de originele add-on en herstel diens eerdere startinstellingen.
De originele instellingen en opslag blijven behouden. Bestaande Node-RED-flows
naar `ORIGINAL_ADDON_HOST` bereiken weer de originele add-on. Zolang de test-add-on
draait, moeten ook eventuele RGB-flows naar de nieuwe hostnaam verwijzen.

## Verificatie en grenzen

Tien lokale tests geslaagd met de echte OLED-controllerbron van PM_Auto 1.2.5,
een gesimuleerde schermdriver en Flask 3.1.3. Getest: tijdelijk/blĳvend,
vervangen/wissen, verlopen, uitgeschakeld bij opstart en tijdens gebruik,
slapen, regelbreedte, API-validatie, berichtgrootte en tekenfouten.
De standaardtekenfunctie en hardware worden in deze tests vervangen door simulaties.
Flask in het originele image kan een andere versie zijn; containerintegratie,
S6-start/stop, AppArmor-toegang en het fysieke OLED moeten op de Pi worden getest.
Docker is niet beschikbaar in de bouwomgeving; er is geen ARM64-containerbouw uitgevoerd.

Het officiële basisimage is op 11 september 2026 gecontroleerd via het Docker-register:
Linux/ARM64, tag 1.2.6, digest
`sha256:f56b4661857afc90515969fd80cc6c4989aff70fb0732dde4a3b7089ee13bdca`.
De Dockerfile gebruikt die digest om wijzigingen aan de tag te vermijden.
De launcher controleert de drie pakketversies vóór het initialiseren van hardware.

Tests zelf uitvoeren met Python en Flask geïnstalleerd: `python tests/test_oled.py`.

## Broncode en licentie

De extensie en meegeleverde OLED-testfixture vallen onder GPL-2.0-only; zie LICENSE.
De OLED-fixture is ongewijzigde SunFounder-code uit commit
`1b8b4d05b50358eb09831066304d51ddec268d19`:
https://github.com/sunfounder/pm_auto/tree/1b8b4d05b50358eb09831066304d51ddec268d19

Overige basis:
https://github.com/sunfounder/pironman5/tree/1.2.6
https://github.com/sunfounder/pm_dashboard/tree/1.2.6
https://github.com/sunfounder/home-assistant-addon/tree/main/pironman5

De originele Python-bestanden in het image worden niet overschreven. Een launcher
verbindt een OLED-subklasse en drie nieuwe Flask-routes met de bestaande service.
