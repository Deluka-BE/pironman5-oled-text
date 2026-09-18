# Pironman 5 direct bedienen in Home Assistant

Versie 0.1.0 voegt een **aangepaste Home Assistant-integratie** toe. Die praat
rechtstreeks met de bestaande Pironman-app op de interne Home Assistant-hostnaam.
Node-RED is hiervoor niet nodig en kan de gemaakte entiteiten daarna gewoon
gebruiken met standaard Home Assistant-acties.

Deze versie verandert niets aan OLED-tekening, animaties of de verversingssnelheid.

## Installeren via HACS

1. Installeer eerst de app **Pironman 5 OLED tekst (test)** uit deze repository
   en start hem.
2. Voeg in HACS deze GitHub-repository toe als **Integration**:
   `https://github.com/Deluka-BE/pironman5-oled-text`.
3. Installeer **Pironman 5 Control** en herstart Home Assistant.
4. Kies **Instellingen → Apparaten & diensten → Integratie toevoegen → Pironman 5 Control**.
5. Vul de hostnaam uit de appinformatie in, bijvoorbeeld
   `8639c588-pironman5-text`, en laat poort `34001` staan.

## Beschikbare entiteiten

- `light.pironman_5_rgb` — aan/uit, kleur, helderheid en RGB-effect.
- `select.pironman_5_rgb_effect` en `number.pironman_5_rgb_effect_speed`.
- `switch.pironman_5_oled` — fysieke OLED aan/uit.
- `text.pironman_5_oled_text` — stuur tekst; nieuwe regels worden OLED-regels.
- `select.pironman_5_oled_icon`, `select.pironman_5_oled_animation` en
  `select.pironman_5_oled_text_size` — wijzigen het actieve bericht.
- `number.pironman_5_oled_duration` — de resterende tijd van het actieve
  bericht; `0` houdt het bericht staan.
- `button.pironman_5_oled_clear` — terug naar het normale statusbeeld.

De exacte entiteitsnamen krijgen Home Assistant zelf bij de installatie. De
voorbeelden zijn de standaardnamen en kunnen afwijken als er al een Pironman
bestaat.

## Node-RED

Een gewone Home Assistant **action**-node is daarna genoeg. Bijvoorbeeld:

```yaml
action: light.turn_on
target:
  entity_id: light.pironman_5_rgb
data:
  rgb_color: [0, 170, 255]
  brightness_pct: 40
```

Voor de OLED-tekst kun je `text.set_value` met `value: "Hallo Flup!"` gebruiken.

