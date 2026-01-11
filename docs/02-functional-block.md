---

## 2. Interfaces per blok

### 2.1 USB → ESP32-C2
- Protocol: USB MIDI
- Inputs: MIDI Note On/Off, velocity, channel
- Output: geen (audio gaat analoog)
- Debug: USB serial (REPL/logging)

### 2.2 ESP32-C2 → I2C bus
- Bus: I2C, 100 kHz
- Devices op bus:
  - PCF8574 (parallel expander)
  - OLED display
- Eisen:
  - I2C mag synth timing niet blokkeren
  - OLED updates “low priority”

### 2.3 PCF8574 → SN76489 (parallel + control)
- Data: D0..D7 (8-bit)
- Control:
  - WE / strobe (write enable)
  - (eventueel CE, afhankelijk van SN76489 variant/board)
- Eisen:
  - Data moet stabiel zijn vóór de write-strobe
  - Geen bus-sharing in V1

### 2.4 SN76489 → Audio keten
- Output: mono analoog
- Vereist:
  - AC-koppeling
  - Basis filtering/ontkoppeling
  - Potmeter vóór versterker

### 2.5 Audio amp → TRS jack
- Output: dual-mono L/R (identiek signaal)
- Vereist:
  - DC-blokkering naar koptelefoon
  - serie-R per kanaal (stabiliteit/bescherming)

---

## 3. Timing & enable-volgorde (minimaal noodzakelijk)

Doel: betrouwbare writes naar SN76489 via PCF8574.

### 3.1 Write-sequence (abstract)
Voor elke SN76489 “byte write”:

1. **Zet data-byte** op PCF8574 outputs (D0..D7)
2. **Wacht korte settle-time** (microseconden-orde)
3. **Pulse WE/strobe** (actief laag of hoog afhankelijk van wiring)
4. **Wacht korte hold-time**
5. (optioneel) WE terug naar idle

Belangrijk:
- PCF8574 is I2C-gedreven → writes zijn relatief “traag”
- Dat is oké: SN76489 register writes hoeven niet snel, wél consistent

### 3.2 Update-rate (richtlijn)
- Note events: direct verwerken
- Pitch/volume: bij Note On/Off en (optioneel) aftertouch/velocity mapping
- OLED: max ~10 updates/sec (niet meer)

---

## 4. Voice-mapping (functionele routing)

### 4.1 Basis V1 voice policy
- 3 tone channels: CH0, CH1, CH2
- 1 noise channel: CH3

### 4.2 MIDI channel gedrag (V1)
- MIDI Channel bepaalt:
  - óf “part” selectie (bijv. ch1→tone, ch10→noise)
  - óf simpel: alle MIDI kanalen sturen dezelfde 3 tone voices (round-robin)
- Keuze wordt in firmware vastgelegd; hardware-onafhankelijk

### 4.3 Voice allocatie (simpel)
- Round-robin over CH0-CH2
- Note Off: mute kanaal als die noot actief was
- Noise kanaal: alleen op afgesproken MIDI channel of vaste note-range

---

## 5. Meetpunten (breadboard/debug-first)

### MP0 — USB enumeratie
- Verwachting: device verschijnt als USB MIDI
- Test: DAW/MIDI monitor ziet Note On/Off

### MP1 — I2C gezondheid
- Verwachting: OLED reageert, PCF8574 ACKt
- Test: I2C scan / simpele write test

### MP2 — PCF8574 outputs
- Verwachting: D0..D7 togglen bij writes
- Test: scope op 1–2 datalijnen + strobe

### MP3 — SN76489 control
- Verwachting: strobe pulses zichtbaar
- Test: scope op WE/strobe

### MP4 — SN76489 audio
- Verwachting: toon zichtbaar op scope (klein AC signaal)
- Test: scope AC-coupled, luister via tijdelijke versterker

### MP5 — Post-filter / potmeter wiper
- Verwachting: signaal amplitude verandert met pot
- Test: scope op wiper

### MP6 — Headphone out L/R
- Verwachting: L = R identiek (dual-mono)
- Test: scope op tip en ring, zelfde amplitude/fase

---

## 6. Faalmodi (wat er typisch misgaat)

- Geen geluid maar wel MIDI:
  - SN76489 krijgt geen writes (MP2/MP3 check)
- OLED werkt, maar SN76489 niet:
  - PCF8574 adres / wiring fout (MP1/MP2)
- Geluid maar veel ruis/piep:
  - grounding / decoupling / audio routing (MP4–MP6)
- Volume doet niks:
  - pot verkeerd aangesloten (MP5)

---

## 7. Succescriteria Stap 3

Stap 3 is geslaagd als:
- Elk blok een duidelijke in/uit interface heeft
- Write-volgorde expliciet is (data → settle → strobe)
- Meetpunten vastliggen en logisch zijn
- Breadboard-ontwerp direct uit dit blokdiagram volgt

---

## Volgende stap
**Stap 4 – Breadboard-ontwerp + meetplan**

- concrete module/IC plaatsing
- wiring-strategie (kort, logisch, meetbaar)
- eerste testprocedure van MP0 → MP6
