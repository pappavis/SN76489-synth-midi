# Stap 6 – KiCad schema & PCB-aanpak
DIY USB-MIDI PSG-synth (SN76489 + ESP32-C2)

Doel van deze stap:
- Breadboard-ontwerp **1-op-1 vertalen** naar schema
- Geen nieuwe ideeën introduceren
- PCB zo ontwerpen dat fouten **moeilijk** worden

Ontwerpregel (hard):
> Wat niet bewezen is op breadboard, mag niet op de PCB.

---

## 1. Scope van de PCB (V1)

### Wat komt **wel** op de PCB
- ESP32-C2 (Wemos mini footprint of headers)
- PCF8574 (DIP)
- SN76489 (DIP)
- I2C OLED header
- Audio-versterker **Optie B (opamp-based)**
- Potmeter (board-mount of via header)
- 3.5 mm TRS jack
- Alle ontkoppeling en passives (THT)

### Wat komt **niet** op de PCB
- LM386 (blijft optioneel / extern)
- Batterij, laadcircuits
- Extra knoppen / encoders
- Stereo uitbreidingen
- “Handige extra headers” zonder bewezen nut

---

## 2. Schema-opbouw in KiCad (afdwingende volgorde)

### 2.1 Schema hiërarchie (aanrader)

Gebruik **hiërarchische sheets**:
Top.sch
├── Power.sch
├── MCU_USB.sch
├── I2C_Bus.sch
├── PSG_SN76489.sch
├── Audio_Amplifier_Opamp.sch
└── IO_Audio.sch

Waarom:
- Elk blok = 1 mentale eenheid
- Reviewbaar
- Makkelijk debuggen bij fouten

---

## 3. Power & ground schema (Power.sch)

### Netnamen (verplicht)
- +5V_DIG
- GND_DIG
- +5V_AUD
- GND_AUD

### Eisen
- +5V_DIG en +5V_AUD **pas samen** bij USB-entry
- GND_DIG en GND_AUD **pas samen** bij star-point
- Elk IC:
  - 100 nF keramisch direct bij VCC–GND
- Extra bulk:
  - 10–47 µF per sectie

---

## 4. MCU & USB (MCU_USB.sch)

### ESP32-C2 (Wemos mini)
- USB direct naar connector
- Geen extra ESD/filters in V1
- Headers voor:
  - SDA
  - SCL
  - debug GPIO (optioneel)

### Eisen
- Geen 5 V op GPIO’s
- I2C op vaste pins documenteren in schema-notes

---

## 5. I2C bus (I2C_Bus.sch)

### Componenten
- PCF8574
- OLED header

### Eisen
- Pull-ups: 4.7–10 kΩ naar +5V_DIG
- Netlabels:
  - SDA
  - SCL
- Adressen als tekst in schema (comment)

---

## 6. PSG-sectie (PSG_SN76489.sch)

### SN76489
- VCC = +5V_DIG
- Decoupling:
  - 100 nF direct
  - 10 µF bulk dichtbij

### Parallel bus
- D0..D7 expliciet gelabeld
- Control-lijn (WE / strobe) duidelijk benoemd

### Audio-out
- AC-koppeling **direct bij IC**
- Netlabel: `PSG_AUDIO_RAW`

---

## 7. Audio amplifier (Audio_Amplifier_Opamp.sch)

### Gebaseerd op Optie B
- Opamp: LM358 (DIP)
- Virtuele ground:
  - R-divider + buffer
  - Netlabel: `VREF_AUD`

### Netnamen
- `AUDIO_IN`
- `AUDIO_POST_POT`
- `AUDIO_L`
- `AUDIO_R`

### Eisen
- DC-blokkering vóór TRS jack
- Serie-R per kanaal

---

## 8. IO & Audio jack (IO_Audio.sch)

### Potmeter
- Mono, log
- Board-mount of header → kies één

### TRS jack
- Tip = AUDIO_L
- Ring = AUDIO_R
- Sleeve = GND_AUD

### Extra
- Bleeder resistors naar GND_AUD

---

## 9. PCB-layout strategie (belangrijker dan schema)

### 9.1 Plaatsing (volg breadboard-zones)
[ USB + MCU ] [ I2C + PCF ] [ SN76489 ] [ AUDIO ]

- Links → rechts
- Geen kruisende signaalpaden

### 9.2 Grounding
- Volledig ground plane
- Split via netnames (DIG/AUD)
- Star-point bij USB-entry

### 9.3 Routing-regels
- Audio sporen kort, breed, weg van I2C
- Geen digitale sporen onder opamp-inputs
- Decoupling caps <5 mm van IC-pins

---

## 10. Footprints & THT-keuzes

- Alles **through-hole**
- DIP-8 / DIP-16 waar mogelijk
- Headers i.p.v. direct solderen bij twijfel
- Potmeter en jack: mechanisch robuust

---

## 11. ERC / DRC checklist

Voor productie:
- [ ] ERC = 0 errors
- [ ] DRC = 0 errors
- [ ] Alle netlabels kloppen
- [ ] GND_DIG ≠ GND_AUD behalve star-point
- [ ] Audio nets niet per ongeluk op DIG-ground

---

## 12. Succescriteria Stap 6

Stap 6 is geslaagd als:
- Schema exact overeenkomt met breadboard
- PCB logisch “leesbaar” is zonder schema
- Audio- en digitale secties fysiek gescheiden zijn
- Geen “ik dacht dat het wel handig was”-beslissingen

---

## Volgende stap
**Stap 7 – Firmware-architectuur (CircuitPython)**

- USB MIDI handling
- Voice-allocatie
- SN76489 write-sequence
- Testmodes per meetpunt (MP0–MP6)

