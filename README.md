# Deluka's Home Assistant Apps

Een eigen collectie apps voor de Home Assistant-winkel.

[![Repository toevoegen aan Home Assistant](https://my.home-assistant.io/badges/supervisor_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_addon_repository/?repository=https%3A%2F%2Fgithub.com%2FDeluka-BE%2Fpironman5-oled-text)

Voeg deze repository eenmaal toe. In de winkel verschijnt daarna de groep
**Deluka's Home Assistant Apps**. Staat de repository al in je winkel?
Kies **Winkel → ⋮ → Controleren op updates** en vernieuw de pagina.

| App | Wat doet deze? | Platform |
| --- | --- | --- |
| [Pironman 5 OLED tekst (test)](pironman5_text/DOCS.md) | Eigen tekst, tekstgroottes, pictogrammen en animaties op het OLED; RGB-bediening blijft beschikbaar. | Raspberry Pi / aarch64 |
| [Calories Club Node-RED Bridge](calories-club-bridge/DOCS.md) | OAuth- en MCP-bridge tussen Node-RED en Calories Club. | aarch64, amd64 |

Dit is een aanvullende repository: de apps verschijnen nadat je de repository
hebt toegevoegd, niet automatisch in iedere Home Assistant-installatie.

## Bestaande installaties

Toevoegen of verversen van de repository verandert je geïnstalleerde apps niet.
Een lokale app of een app uit een andere repository is een afzonderlijke
installatie. Instellingen en OAuth-aanmeldingen worden niet automatisch overgezet.
Een werkende Calories Club-installatie uit de oorspronkelijke repository mag
daar blijven; opnieuw installeren is niet nodig. Start geen tweede bridge op
dezelfde hostpoort. Voor Pironman: volg de [overstaphandleiding](INSTALL_GITHUB.md)
en laat slechts één app tegelijk de hardware bedienen.

## Onderhoud en bronnen

Nieuwe Home Assistant-apps kunnen als eigen map aan deze collectie worden toegevoegd.
Losse Node-RED-flows en andere bestanden zijn geen zelfstandige winkelapps.

Calories Club Bridge 0.4.4 is overgenomen uit
[de eigen bronrepository](https://github.com/Deluka-BE/calories-club-node-red-bridge/tree/766b6a089f8d4ec5673a5f1a1b63fe9248f73378/calories-club-bridge).
De acht tekstbestanden zijn ongewijzigd overgenomen; deze collectie gebruikt
een eigen pictogram. Wijzigingen in de bronrepository worden niet automatisch
gesynchroniseerd: een volgende versie moet ook hier worden bijgewerkt.
De container wordt geleverd door de in de Dockerfile vermelde bridge-image.

De informatie over SunFounder en GPLv2 hieronder betreft de Pironman-uitbreiding.
De winkelpictogrammen zijn voor deze collectie getekend en gebruiken geen
SunFounder- of Calories Club-logo.

---

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

## Installatie via GitHub

[![Repository toevoegen aan Home Assistant](https://my.home-assistant.io/badges/supervisor_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_addon_repository/?repository=https%3A%2F%2Fgithub.com%2FDeluka-BE%2Fpironman5-oled-text)

**Al lokaal geïnstalleerd?** Volg [overstappen van lokaal naar GitHub](INSTALL_GITHUB.md).
Alleen de repository toevoegen zet je bestaande installatie niet om.

## Rechtstreeks bedienen vanuit Home Assistant

Wil je RGB en OLED als gewone Home Assistant-entiteiten gebruiken, zonder een
verplichte Node-RED-flow? Installeer de meegeleverde integratie volgens
[Pironman direct bedienen in Home Assistant](PIRONMAN_HOME_ASSISTANT.md).
Deze integratie verandert niets aan de bestaande OLED-rendering.


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
