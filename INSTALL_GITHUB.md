# Installeren via GitHub en overstappen vanaf lokaal

## Toevoegen aan Home Assistant

[Voeg deze repository toe aan Home Assistant](https://my.home-assistant.io/redirect/supervisor_addon_repository/?repository=https%3A%2F%2Fgithub.com%2FDeluka-BE%2Fpironman5-oled-text)

Of handmatig:

1. Open **Instellingen → Add-ons (of Apps) → Winkel → ⋮ → Repositories**.
2. Voeg `https://github.com/Deluka-BE/pironman5-oled-text` toe.
3. Sluit het venster en vernieuw de winkel indien nodig.
4. Open **Pironman 5 OLED tekst (test)** onder de repository **Deluka's Home Assistant Apps**.
   Kies deze versie, niet dezelfde naam onder **Lokale add-ons**.
5. Klik **Installeren**. Home Assistant haalt de bestanden van GitHub en bouwt
   de ARM64-container op jouw Pi. Voor deze installatie hoef je geen ZIP te kopiëren.

De repository bevat de vereiste repository.yaml en een add-onmap met config.yaml
en Dockerfile. De GitHub-installatie op jouw Home Assistant moet nog worden bevestigd.

## Je bestaande lokale installatie behouden tijdens de overstap

De lokale en GitHub-versie zijn voor Home Assistant **twee afzonderlijke add-ons**.
De GitHub-versie neemt instellingen niet automatisch over.

1. Maak een back-up van je werkende lokale add-on. Laat die tijdens het installeren
   van de GitHub-versie nog draaien; start de nieuwe versie nog niet.
2. Wil je je instellingen meenemen? Lees ze uit via het dashboard of
   `GET http://local-pironman5-text:34001/api/v1.0/get-config`.
   Bewaar alleen het object onder `data` als `initial-config.json`.
3. Plaats dit vóór de eerste start in de configuratiemap van de NIEUWE add-on:
   `/addon_configs/<nieuwe-add-on-slug>/initial-config.json`.
   De slug heeft een repositoryprefix en eindigt op `_pironman5_text`; deze
   staat in de Home Assistant-URL van de informatiepagina van de nieuwe add-on.
   Gebruik dus niet de map `local_pironman5_text`.
   Dit is optioneel: zonder import start de nieuwe versie met standaardinstellingen.
4. Zet automatisch starten en Watchdog van de lokale versie uit en stop die.
   De oorspronkelijke SunFounder-add-on blijft ook uitgeschakeld.
5. Start de GitHub-versie. Controleer dashboard, ventilatoren en OLED.

Er mag slechts één Pironman-add-on tegelijk actief zijn.

## Node-RED opnieuw verbinden

Op de informatiepagina van de GitHub-versie staat **Hostnaam**. Vervang
`local-pironman5-text` door die hostnaam in de function-node **BASE URL en JSON**
en in eventuele RGB HTTP request-nodes. Poort 34001 en alle API-paden blijven gelijk.

Test de verbinding met `/api/v1.0/test`, stuur een kort tekstbericht en controleer
of daarna het standaardscherm terugkomt. Pas na een geslaagde test kun je
automatisch starten voor de GitHub-versie inschakelen.

## Volgende updates

Na deze overstap: **Winkel → ⋮ → Controleren op updates**, open de GitHub-versie
en kies **Bijwerken** zodra een hogere versie beschikbaar is.
Handmatig bestanden in /addons vervangen is dan niet meer nodig.
Toevoegen van alleen de repository zet de bestaande lokale installatie niet om.

## Terugschakelen

Stop de GitHub-versie en zet diens automatisch starten/Watchdog uit. Start de
bewaarde lokale versie en zet in Node-RED de hostnaam terug naar
`local-pironman5-text`. Je hoeft geen van beide add-ons te verwijderen.
