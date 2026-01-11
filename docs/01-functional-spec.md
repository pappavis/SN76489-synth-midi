# Stap 1 – Functionele specificaties
DIY USB-MIDI PSG-synth (SN76489 + ESP32-C2)

## 1. Hoofdfunctie
Een standalone USB-MIDI synthesizer die MIDI-noten omzet naar
klassieke PSG-audio via de SN76489, met regelbare mono-audio
op een koptelefoonuitgang.

## 2. Gebruikersperspectief
### Input
- USB MIDI device
- Note On / Off
- Velocity (optioneel)
- MIDI Channel

### Output
- Direct hoorbaar geluid
- Fysieke volumeregeling
- 3.5 mm TRS koptelefoon (dual-mono)

### Feedback
- OLED-display (SSD1306/1309-klasse)
- Toon van MIDI-status en actieve voices

## 3. Synth-gedrag
- 3 toonkanalen + 1 noise-kanaal
- Monofonisch per kanaal
- Geen envelopes of modulatie

## 4. Digitale keten
USB MIDI
→ ESP32-C2 (CircuitPython)
→ PCF8574
→ SN76489
→ analoge audio

## 5. Audio-pad
SN76489
→ filtering
→ volumepotmeter
→ audio-versterker
→ koptelefoon

## 6. Buiten scope
Geen presets, geen CC’s, geen stereo, geen batterij,
geen SMD, geen PCB-optimalisatie.

## 7. Meetbaarheid
Alles moet testbaar zijn op breadboard met scope,
multimeter en serial debug.

## 8. Succescriteria
Heldere scope, reproduceerbaar ontwerp,
en een solide basis voor stap 2.
