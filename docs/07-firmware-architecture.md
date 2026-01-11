# Stap 7 – Firmware-architectuur (CircuitPython)
DIY USB-MIDI PSG-synth (SN76489 + ESP32-C2)

Doel:
- Firmware opdelen in **begrijpelijke, testbare lagen**
- Hardware abstraheren (I2C, PCF8574, SN76489)
- Debug en test mogelijk maken per meetpunt (MP0–MP6)

Ontwerpregel:
> Firmware mag nooit “slim” zijn waar hardware dat al afdwingt.

---

## 1. Architectuur-overzicht

### Hoofdstructuur
main.py
│
├── midi/
│   ├── usb_midi.py
│   └── note_mapper.py
│
├── drivers/
│   ├── pcf8574.py
│   ├── sn76489.py
│   └── oled_status.py
│
├── audio/
│   └── voice_allocator.py
│
├── system/
│   ├── config.py
│   └── diagnostics.py
│
└── test_modes.py

Elke map = één verantwoordelijkheid.

---

## 2. main.py (orchestratie)

### Verantwoordelijkheden
- Initialisatie van alle subsystemen
- Hoofdloop
- Foutafhandeling (fail-safe gedrag)

### Gedrag
- Start altijd op, ook zonder MIDI
- OLED toont status (“BOOT”, “MIDI OK”, “NO MIDI”)
- Testmodus kan geforceerd worden (bijv. via flag in config)

Pseudo-flow:
boot →
init I2C →
init PCF →
init SN76489 →
init OLED →
init MIDI →
enter main loop

---

## 3. USB MIDI laag (`midi/usb_midi.py`)

### Taken
- USB MIDI device openen
- MIDI messages parsen
- Alleen relevante events doorgeven:
  - Note On
  - Note Off
  - (optioneel) velocity

### Eisen
- Niet blokkeren
- Geen audio-logica hier
- “Dode” MIDI events negeren

Output (event-object):
{
type: NOTE_ON / NOTE_OFF,
note: 0–127,
velocity: 0–127,
channel: 0–15
}

Meetpunt:
- **MP0**: MIDI events zichtbaar via debug print

---

## 4. Voice-mapping & allocatie (`audio/voice_allocator.py`)

### Taken
- MIDI note → SN76489 voice
- Round-robin allocatie over 3 toonkanalen
- Noise-kanaal apart behandelen

### Simpele V1-logica
- 3 tone voices: CH0, CH1, CH2
- Nieuwe Note On:
  - wijs eerst vrije voice toe
  - anders: round-robin overschrijven
- Note Off:
  - mute voice als noot matcht

### Output
- Abstract “voice command”, geen hardware-kennis:

set_voice(channel, frequency, volume)
mute_voice(channel)

---

## 5. SN76489 driver (`drivers/sn76489.py`)

### Taken
- Vertaal abstracte voice-commando’s naar PSG writes
- Bereken frequentie → registerwaarden
- Volume mapping (optioneel via velocity)

### Interface
- `write_byte(value)`
- `set_tone(channel, freq)`
- `set_volume(channel, level)`
- `mute(channel)`

### Eisen
- Geen MIDI-kennis
- Geen I2C-kennis
- Alleen “ik wil deze byte schrijven”

Meetpunt:
- **MP3**: strobe pulses zichtbaar
- **MP4**: audio op output

---

## 6. PCF8574 driver (`drivers/pcf8574.py`)

### Taken
- I2C-communicatie met PCF8574
- 8-bit parallel data aanbieden
- Control-lijnen beheren (WE/strobe)

### Interface
- `set_data(byte)`
- `pulse_write()`
- `write(byte)` (combinatie van bovenstaand)

### Timing
- Simpel, conservatief:
  - set data
  - korte delay (µs–ms orde)
  - pulse strobe
  - delay

Meetpunt:
- **MP2**: D0–D7 togglen zichtbaar

---

## 7. OLED status (`drivers/oled_status.py`)

### Taken
- Minimale statusweergave
- Geen grafische fratsen

### Weergavevoorbeelden
- BOOT
- MIDI OK
- MIDI CH: 1
- ACTIVE VOICES: 2

### Eisen
- Updates max ~10 Hz
- OLED mag nooit MIDI of audio blokkeren

Meetpunt:
- **MP1**: OLED reageert op statuswijziging

---

## 8. Configuratie (`system/config.py`)

### Bevat
- I2C-adressen
- MIDI-kanaal-instellingen
- Testmode flags
- Debug verbosity

Voorbeeld:

I2C_FREQ = 100_000
PCF_ADDR = 0x20
OLED_ADDR = 0x3C
DEBUG = True

---

## 9. Diagnostics & testmodes (`system/diagnostics.py`, `test_modes.py`)

### Doel
- Hardware testen zonder MIDI
- Meetpunten afdwingen

### Testmodes (V1)
- Test 1: PCF8574 teller (0x00 → 0xFF)
- Test 2: SN76489 vaste toon (“beep”)
- Test 3: Volume sweep
- Test 4: OLED status cycling

Meetpunten:
- MP2 → MP6 zonder DAW of MIDI-controller

---

## 10. Fail-safe gedrag (belangrijk)

- Geen MIDI → geen crash
- OLED fout → audio blijft werken
- PCF fout → duidelijke debugmelding
- Onverwachte fout → systeem blijft in loop

Geen watchdogs of RTOS in V1.

---

## 11. Succescriteria Stap 7

Stap 7 is geslaagd als:
- Elke laag afzonderlijk te testen is
- Hardware-drivers geen MIDI-logica bevatten
- MIDI-code geen hardware-details kent
- Testmodes MP0–MP6 onafhankelijk afdwingbaar zijn

---

## Volgende stap
**Stap 8 – Test- en debug-strategie**

- Concrete meetprocedures
- Verwachte golfvormen
- “Als X niet werkt, check Y”

