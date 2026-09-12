# Pironman 5 OLED tekst voor Home Assistant

Een community-uitbreiding voor de SunFounder Pironman 5-add-on: stuur maximaal
vier regels tekst vanuit Node-RED naar het OLED. RGB-bediening blijft beschikbaar.
Dit is geen officiële SunFounder-release.

Dit project is niet verbonden aan of goedgekeurd door SunFounder. Zie
[bronvermelding en wijzigingen](NOTICE.md). De oorspronkelijke auteurs behouden
hun rechten; deze uitbreiding wordt onder GPLv2 aangeboden, zonder garantie.

## Functies

- Tijdelijke meldingen en blijvende tekst.
- Automatisch terug naar het standaardscherm of handmatig wissen.
- HTTP-API en een [Node-RED-voorbeeldflow](node-red-oled.json).
- Respecteert een bewust uitgeschakeld scherm.

Versie **0.2.0**: tekstgroottes 8/12/16/24, negen pictogrammen en animaties.
Zie [opties en voorbeelden](VISUALS.md). Achttien lokale tests slagen.
Een eerste gebruiker heeft in versie 0.1.1
tekstweergave en terugkeer naar het standaardscherm op een Pi bevestigd.

## Installatie

Voeg de URL van deze repository toe via de Home Assistant-add-onwinkel →
⋮ → Repositories. Installeer daarna **Pironman 5 OLED tekst (test)**.
Stop vóór het starten de originele Pironman-add-on en schakel daar Watchdog en
automatisch starten uit. Laat nooit beide tegelijk dezelfde hardware bedienen.

De [uitgebreide handleiding](LEESMIJ.md) beschrijft ook lokale installatie,
instellingen overnemen, de API en terugschakelen.

**Let op:** bij installatie via GitHub wijkt de interne hostnaam af van
`local-pironman5-text`. Gebruik de hostnaam op de informatiepagina van de
geïnstalleerde add-on en pas deze aan in de Node-RED-function-node.

## Tests en licentie

Installeer Flask en Pillow in een Python-omgeving en voer `python tests/test_visuals.py` uit.
Zie VISUALS.md voor het instellen van het testlettertype.
De tests simuleren hardware; ze vervangen geen praktijktest op een Raspberry Pi.

GPL-2.0-only, zie [LICENSE](LICENSE). Gebaseerd op SunFounder pironman5 1.2.6,
pm_auto 1.2.5 en pm_dashboard 1.2.6. Bronverwijzingen staan in de handleiding.
