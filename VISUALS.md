# Tekstgrootte, pictogrammen en animatie — versie 0.2.0

Alle opties gaan naar dezelfde POST `/api/v1.0/set-oled-text` met
`Content-Type: application/json`. Bestaande berichten werken zonder wijzigingen.

## Tekstgrootte

| font_size | Maximale regels |
|---|---|
| 8 (standaard) | 4 |
| 12 | 3 |
| 16 | 2 |
| 24 | 1 |

Meer regels dan passend bij de gekozen grootte geven HTTP 400, zonder het
bestaande bericht te vervangen. Te lange regels worden afgekort met `...`.
Tekst blijft beperkt tot printbare ASCII en het graadteken; pictogrammen worden
gekozen met `icon`, niet door emoji in tekst te zetten.

Voorbeeld:

```json
{"lines":["21.5 C"],"font_size":24,"duration":30}
```

## Pictogrammen

`icon` kan `home`, `heart`, `thermometer`, `bulb`, `check`, `warning`, `wifi`,
`fan` of `spinner` zijn. `null` of weglaten betekent geen pictogram.

Met tekst staat een 32 × 32 pictogram links; er blijft 88 pixels tekstbreedte over.
Zonder tekst wordt het pictogram 48 × 48 en gecentreerd.
De pictogrammen zijn nieuw getekend in code; er worden geen externe iconensets,
logo's, bestanden of URL's ingeladen.

```json
{"lines":["21.5 C","Binnen"],"font_size":16,"icon":"thermometer","duration":0}
```

## Animaties

| animation | Gedrag |
|---|---|
| none (standaard) | Stilstaand pictogram |
| blink | Pictogram om de seconde aan/uit; tekst blijft zichtbaar |
| pulse | Pictogram wordt in vier stappen groter/kleiner |
| spin | Draaiende fan of laadindicator; alleen met fan/spinner |

Een animatie vereist een `icon`. Het zijn eenvoudige ingebouwde animaties op de
bestaande hardwarecyclus, ongeveer **1 beeld per seconde**. Ze zijn stapsgewijs,
niet vloeiend zoals een video. Er is geen GIF-upload in deze versie.
De ventilatorcyclus wordt niet vertraagd met extra wachttijden en er wordt geen
tweede thread gestart die het OLED aanstuurt. Animatie draait alleen zolang het
bericht actief is. Een nieuw bericht begint opnieuw bij beeld 0.

```json
{"icon":"heart","animation":"pulse","duration":30}
```

```json
{"lines":["Even geduld"],"icon":"spinner","animation":"spin","duration":30}
```

`duration: 0` houdt de weergave actief tot vervangen/wissen/herstart/uitschakelen.
POST `clear-oled-text` herstelt het standaardscherm. GET `get-oled-text` meldt ook
de gekozen grootte, het pictogram en de animatie. Een bewust uitgeschakeld OLED
blijft uit en weigert nieuwe berichten met HTTP 409.

## Node-RED en bijwerken

Importeer [node-red-oled.json](node-red-oled.json). De flow heeft handmatige
voorbeeldknoppen voor alle groottes en verschillende pictogrammen/animaties.
Pas de hostnaam aan in **BASE URL en JSON** als deze niet `local-pironman5-text` is.

Bij installatie vanuit deze GitHub-repository: controleer updates in de
Home Assistant-add-onwinkel en werk de bestaande test-add-on bij naar 0.2.0.
Bij lokale installatie: vervang de bestanden onder `/addons/pironman5_text`
door de map uit het nieuwe pakket, controleer updates en kies Bijwerken.
Verwijder de add-on niet; zo blijft de interne configuratie behouden.
De originele SunFounder-add-on blijft uitgeschakeld.

Test daarna eerst een tekstbericht zonder extra opties, vervolgens grootte 24
en een pulserend hart. De lokale tests gebruiken het oorspronkelijke lettertype
en echte beeldbuffers, maar de nieuwe rendering en frames moeten nog op jouw
OLED worden bevestigd.

## Tests

Gebruik Python met Flask en Pillow (>=9.1). Stel `OLED_TEST_FONT` in op het pad
van een TrueType-lettertype (voor de exacte controle: Minecraftia-Regular.ttf
uit de genoemde SunFounder-commit). Zonder die variabele gebruiken tests
`DejaVuSans.ttf` als dat lettertype lokaal beschikbaar is.

Voer uit: `python tests/test_visuals.py`. Dit draait 18 tests, inclusief de 10
bestaande gevallen. Het lettertype wordt niet meegeleverd; de add-on gebruikt
het lettertype dat al in het originele basisimage aanwezig is.
