# Stap 8 – Test- en debug-strategie
DIY USB-MIDI PSG-synth (SN76489 + ESP32-C2)

Doel:
- Van “geen idee wat er mis is” naar **deterministisch debuggen**
- Elke keten (USB → I2C → PCF → SN → audio) afzonderlijk kunnen valideren
- Meetprocedures vastleggen met jouw apparatuur:
  - RIGOL DHO804 oscilloscoop
  - Aneng SZ02 multimeter
  - Riden RC6006 labvoeding (indien externe 5 V nodig)

Ontwerpregel:
> Als een stap faalt: ga niet verder. Fix eerst de vorige meetpunt-fase.

---

## 0. Debug-setup (altijd eerst)

### 0.1 Hardware-opstelling
- Tablet links (Stap 4 + blokdiagram)
- Breadboard midden
- Scope + multimeter rechts

### 0.2 Scope basisinstellingen (startpunt)
- Probe: 10×
- Bandwidth limit: aan (als je HF-ruis wil onderdrukken), anders uit voor oscillatie-detectie
- Coupling:
  - Digitaal: DC
  - Audio: AC (voor snelle sanity checks)
- Ground clip: zo kort mogelijk (liefst spring ground)

### 0.3 Multimeter checks vóór power-on
- Continuity: geen kortsluiting tussen +5 V en GND
- I2C lijnen niet hard aan GND of +5V (controle weerstand)

---

## 1. Fase MP0 – USB MIDI enumeratie

### Doel
ESP32-C2 verschijnt als USB device (later: MIDI).

### Test
- Sluit aan op host
- Controleer:
  - CircuitPython drive zichtbaar
  - Serial console werkt

### Pass criteria
- Device boot zonder reset-loop
- Serial output toont “BOOT/READY”

### Fail patterns
- Reset-loop → te hoge load op 3.3 V / verkeerde wiring
- Geen serial → USB/board issue of firmware corrupt

---

## 2. Fase MP1 – I2C-bus gezondheid (OLED + PCF)

### Doel
I2C scan ziet devices (PCF + OLED).

### Test (skeleton)
- `system/diagnostics.i2c_scan()`
- Verwachting: adressen zoals `0x20` (PCF), `0x3C` (OLED) mogelijk

### Pass criteria
- Scan consistent (zelfde addresses bij elke reboot)

### Fail patterns + acties
- Scan leeg:
  - check SDA/SCL pins
  - check pull-ups (4.7–10 kΩ naar +5 V_DIG)
  - check GND shared (star-point)
- Alleen OLED, geen PCF:
  - PCF adres jumper/pin fout
  - PCF verkeerd om / geen 5 V
- Flaky scan (soms wel soms niet):
  - draden te lang
  - slechte breadboard contact
  - pullups te zwak/sterk → probeer 4.7 kΩ

---

## 3. Fase MP2 – PCF8574 data toggling

### Doel
PCF outputs veranderen betrouwbaar (D0..D7).

### Test (skeleton)
- `TEST_MODE = "pcf_counter"`
- Scope op:
  - D0 (moet snel togglen)
  - D7 of andere bit (ook toggles)

### Pass criteria
- Strakke digitale blokgolven
- Geen “half levels” of zwevende lijnen

### Fail patterns + acties
- Lijnen blijven hoog/laag:
  - verkeerde PCF pin mapping
  - PCF niet powered
  - I2C writes falen (terug naar MP1)
- Rare rimpel/instabiel:
  - ground clip te lang
  - breadboard contact slecht

---

## 4. Fase MP3 – Strobe/WE pulses naar SN76489

### Doel
Write-strobe pulses zichtbaar en op juiste polariteit.

### Test
- Gebruik `sn_beep` of een simpele write-loop
- Scope op strobe-lijn (PCF bit die jij gekozen hebt)

### Pass criteria
- Duidelijke pulses bij elke `write_byte()`
- Polariteit klopt:
  - active-low: korte LOW pulse
  - active-high: korte HIGH pulse

### Fail patterns + acties
- Geen pulses:
  - strobe bit in config fout (`PCF_STROBE_BIT`)
  - strobe wired naar verkeerde SN pin
- Puls is omgekeerd:
  - `STROBE_ACTIVE_LOW` verkeerd

---

## 5. Fase MP4 – SN76489 audio out (raw)

### Doel
PSG produceert toon/noise.

### Test
- Scope AC-coupled op SN audio out
- Verwachting:
  - klein AC signaal (tientallen tot honderden mVpp)

### Pass criteria
- Toon zichtbaar én verandert bij writes
- Geen grote DC-offset naar buiten toe (AC-coupling gebruik je later)

### Fail patterns + acties
- Flatline:
  - SN krijgt geen writes → terug naar MP2/MP3
  - SN clock ontbreekt (als jouw variant externe clock nodig heeft)
  - SN voeding/decoupling fout
- Heel veel HF-rommel:
  - grounding fout
  - te lange audio-draad
  - ontbrekende decoupling bij SN

---

## 6. Fase MP5 – Potmeter werking (wiper)

### Doel
Amplitude moet netjes mee veranderen.

### Test
- Scope op wiper van pot
- Draai pot van min → max

### Pass criteria
- Signaal amplitude verandert vloeiend
- Min stand: bijna nul

### Fail patterns + acties
- Geen verandering:
  - pot verkeerd aangesloten (wiper verwisseld)
  - signaal niet door pot maar omheen

---

## 7. Fase MP6 – Headphone out L/R dual-mono

### Doel
Tip en ring zijn identiek (dual-mono), geen DC op uitgang.

### Test
- Scope op tip en ring (AC coupled)
- Vergelijk amplitude en fase
- Multimeter DC meting op tip/ring t.o.v. sleeve:
  - moet ~0 V zijn (door C_out)

### Pass criteria
- L = R (zelfde golf)
- DC ~0 V

### Fail patterns + acties
- DC aanwezig:
  - C_out ontbreekt of verkeerd gepolariseerd
- Eén kanaal dood:
  - wiring jack fout
  - serie-R of C_out onderbroken

---

## 8. Audio kwaliteit debug (ruis, brom, piep)

### 8.1 Brom (50 Hz / 100 Hz)
Oorzaken:
- ground loop
- voeding ripple
Acties:
- star-ground check
- extra bulk cap bij audio sectie
- audio ground apart houden

### 8.2 Digitale piep (I2C/clock bleed)
Oorzaken:
- audio draden dicht langs SDA/SCL
- ground shared returns
Acties:
- fysiek scheiden (Stap 4 zones)
- kortere audio input
- Vref en opamp decoupling verbeteren (Optie B)

### 8.3 Oscillatie (hiss, ultrasonisch, warmte)
Oorzaken:
- output capacitieve load
- geen serie-R
Acties:
- R_out (47 Ω) per kanaal
- scope bandwidth open om “haar” te zien

---

## 9. Debug logging (firmware)

### Richtlijn
- Debug prints alleen op state-changes (niet elke sample)
- OLED updates max ~10 Hz

Aanbevolen logging regels:
- BOOT
- I2C scan result
- PCF init OK
- SN init OK
- TEST MODE actief

---

## 10. “Als X, check Y” cheat-sheet

- **Geen I2C scan** → check pullups, SDA/SCL, GND
- **PCF toggles niet** → terug naar I2C, check PCF addr
- **Strobe ontbreekt** → check strobe bit/polariteit
- **Wel strobe, geen audio** → check SN voeding/clock/audio pin
- **Audio ok, volume doet niks** → pot wiring
- **Audio ok, ruis/brom** → grounding + decoupling + routing (Stap 4)

---

## 11. Succescriteria Stap 8

Stap 8 is geslaagd als:
- Jij elke fout kunt herleiden tot één blok
- Je meetpunten MP0–MP6 kunt afvinken
- Je “random proberen” niet meer nodig hebt

---

## Volgende stap
**Stap 9 – Verbeter-voorstellen + vervolgvragen**

- Wat kan beter na eerste metingen?
- Wat verdient PCB-optimalisatie?
- Welke audio-optie wordt definitief?
