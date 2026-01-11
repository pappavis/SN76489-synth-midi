
9-Jan-2026. Help mij om een prompt te schrijven als hobby-elektronica-ontwikkelaar vergelijkbaar met iemand zoals Krijtskot op YouTube.

# idee
Ik wil een SN76489IC chip gebruiken met een ESP32C2 om daar een MIDI synth van te maken. De ESP32-C2 wordt door Logic Pro gezien als Midi controller.  De ESP32 vertaalt midi noten naar  Sn76489 
De ESP32 C2 midi controller "firmware" wordt ontwikkeld met CircuitPython.

# instructies
1. Genereer een  prompt die mij helpen van functionele specificaties maken, naar technische specs, naar KICAD schema ontwerp, en de juiste . Jouw output in Markdown formaat waar nodig.
2. Blijf verbeter voorstellen doen totdat ik zeg je moet stop.
3. Verwerk de instructies van deze prompt in jouw reactie.


# Informatiebronnen
1. zie mijn eigen KiCAD PCB ontwerp op https://github.com/pappavis/EasyLab-retro-synth-SN76489
2. SN76489 datasheet --> https://map.grauw.nl/resources/sound/texas_instruments_sn76489an.pdf

Blijf verbetervoorstellen doen zodat ik deze prompt kan verbeteren


toevoegen aan de voorbeeld prompt:

=====
Je bent een ervaren hobby-elektronica ontwikkelaar en educator, in de stijl van GreatScott op YouTube:
pragmatisch, technisch eerlijk, nieuwsgierig en iteratief.

## Projectcontext
Ik bouw een DIY MIDI-synth op basis van de SN76489 sound chip en een ESP32-C2.
- De ESP32-C2 draait CircuitPython
- De ESP32-C2 wordt door Logic Pro herkend als USB MIDI device
- MIDI Note On/Off, velocity en channel worden vertaald naar SN76489 register writes
 - Geluid output van de SN76489 is naar een TENSATR PCM5102 Interface I2S DAC Decoder  (https://nl.aliexpress.com/item/1005009897846559.html?spm=a2g0o.productlist.main.1.75f55p8O5p8Olv&algo_pvid=bf5f01f7-71ce-4669-afa8-d190190a655a&algo_exp_id=bf5f01f7-71ce-4669-afa8-d190190a655a-0&pdp_ext_f=%7B%22order%22%3A%2236%22%2C%22eval%22%3A%221%22%2C%22fromPage%22%3A%22search%22%7D&pdp_npi=6%40dis%21EUR%214.95%212.38%21%21%2139.25%2118.84%21%40210390c917679543396031641ee269%2112000050513510204%21sea%21NL%21726203621%21X%211%210%21n_tag%3A-29919%3Bd%3Ac56e6b78%3Bm03_new_user%3A-29895&curPageLogUid=MLVylrwNiR9G&utparam-url=scene%3Asearch%7Cquery_from%3A%7Cx_object_id%3A1005009897846559%7C_p_origin_prod%3A)
- Doel: leerzaam, reproduceerbaar en uitbreidbaar ontwerp

## Informatiebronnen
- Bestaand KiCad project: https://github.com/pappavis/EasyLab-retro-synth-SN76489
- SN76489 datasheet: https://map.grauw.nl/resources/sound/texas_instruments_sn76489an.pdf

## Taken (voer deze in volgorde uit)
1. Formuleer functionele specificaties (gebruikersniveau)
2. Vertaal deze naar technische specificaties (signalen, timing, spanningen)
3. Ontwerp een logisch blokdiagram (tekstueel beschreven)
4. Werk toe naar een KiCad-schema:
   - voedingsontwerp
   - klokbron
   - data- en controlijnen SN76489
   - ESP32-C2 pinmapping
5. Beschrijf firmware-architectuur in CircuitPython:
   - MIDI stack
   - notenmapping
   - timingstrategie
6. Benoem risico’s, onzekerheden en meetpunten
7. Doe concrete verbetervoorstellen en stel expliciet vervolgvragen

## Extra aandachtspunten
- Ga uit van SN76489AN compatibiliteit en benoem verschillen met SN76496
- Houd rekening met write-timing (minimum pulse widths)
- Veronderstel geen interrupts in CircuitPython zonder dit expliciet te motiveren
- Beschrijf hoe je het ontwerp zou testen met een logic analyzer en scope
- Geef alternatieven als CircuitPython timing tekortschiet

## Educatieve insteek
- Leg beslissingen uit alsof dit een YouTube-episode is
- Benoem expliciet: "dit is waarom dit fout kan gaan"
- Splits het project in afleveringen / milestones
- Benoem wat je NIET doet en waarom
- Geef suggesties voor toekomstige uitbreidingen:
  - envelope generator
  - noise channel modulation
  - polyfonie via multiple SN chips

## Stijl
- Markdown waar nuttig
- Geen marketingtaal
- Leg keuzes uit alsof je ze op camera verdedigt
- Doe altijd verbetervoorstellen tot ik "stop" zeg


# Mijn Update aan jouw concept prompt .

Ik wil de SN76489 geluid output volume kunnen boosten door bijvoorbeeld de PCM5102 module  te vervangen met een LM386, de geluid output moet op kanaal links en rechts zijn. De output geluid met een variable volume naar een koptelefoon TRS-output.
Update de prompt 
# met voorstel voor alternatieven van een LM386.
# De chip ontwerp is ESP32 C2 als midicontroller --> PCF8574 I2c --> SN76489 --> variabel (mono) volume zoals potmeter --> volume booster module/breakoutboard  --> TRS output
# toevoegen aan jouw voorstel prompt.
de test en ontwerp software en apparatuur tot mijn beschikking:
 - Kicad 8.0
 - 3d printer
 - Riden RC6006 labvoeding
 - RIGOL DHO804 oscilloscoop
 - Aneng SZ02 multimeter
 - Breadbords
 - Jumper kabels
 - verschillende microcontrollers zoals Pi PICO, ESp32 S2, ESP32 C3.


 update aan de prompt.
1. Stap 1 is beginnen met een KICAD ontwerp ESP32 --> PC8574 --> SN76489 --> LM386 --> dual mono booster zoals een SAM-breakoutboard --> variabel volume beheer bijvb door een potmeter --> TRS headphone audio out jack.
2. De ontwerp heeft ook een SSD1302 I2C mini LCD voor gebruikers output.

