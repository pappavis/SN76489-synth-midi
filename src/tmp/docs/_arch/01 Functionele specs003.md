# Funksionele Spesifikasie (FS) v1.6  
## SN76489 PSG Emulasie in Python (MacOS)

**Datum:** 2 Februarie 2026  
**Status:** FS v1.6 (verfyn ná goedgekeurde v0.04)  
**Doelplatform:** MacOS 26.2  
**Python:** 3.12  
**Huidige stabiele weergawe:** v0.04 ✅  

---

## 0. Konteks & Status

SN76489 Emulator v0.04 is **stabiel en goedgekeur** met:

- Volledige SN76489 register-gedrewe emulasie
- Multi-chip engine (1–128 chips)
- Stereo routing (left / right / both)
- Mixer + master gain model
- Deterministiese noise (rate + seed)
- Envelope engine (attack/decay via volume-writes)
- CoreMIDI input (MacOS)
- Streng sanity checks + rollbackstrategie
- Alles in **één Python-bestand**

v0.05 fokus nou op **muzikaliteit & speelbaarheid**.

---

## 1. Doel (v1.6)

Bou SN76489 verder uit van ’n tegnies-korrekte emulator na ’n **speelbare musikale engine**, geskik vir:

- Live MIDI speel
- Akkoorde en melodieë
- Minder artefakte (clicks, abrupt mutes)
- Mensliker klank binne SN76489-beperkings

**Belangrik:**  
Alle klank bly **register-gedrewe**. Geen direkte DSP of shortcuts.

---

## 2. Scope

### 2.1 In scope vir v0.05 (Pad A)

- Polyfoniese voice allocation oor tone0 / tone1 / tone2
- Verbeterde envelope (ADSR-lite)
- Pitch bend ondersteuning (beperk, SN76489-realistisch)
- Verbeterde MIDI speelbaarheid
- Per-chip musikale gedrag

### 2.2 Uitdruklik buite scope vir v0.05

- VST/AU plugin
- Sample-accurate MIDI scheduling
- Effects (reverb, delay, filters)
- Grafiese UI

---

## 3. Runtime modes / CLI (NUUT, eksplisiet)

Die engine moet steeds **CLI-first** bly vir toetsbaarheid, regressie en Copilot-validasie.

### 3.1 Test modes

- `--test beep`  
  Basiese audio sanity test (tone0, vaste frekwensie)

- `--test noise`  
  Noise kanaal toets (white / periodic, rate, seed)

- `--test sequence`  
  Speel ’n vaste note-reeks (melodie / arpeggio)

- `--test chords` (opsioneel)  
  Speel ’n akkoord:
  - tone0 = grondnoot
  - tone1 = terts
  - tone2 = kwint  
  Toets polyfonie en mixing

- `--test sweep` (opsioneel)  
  Pitch sweep op een tone-kanaal  
  Toets period update stabiliteit

---

### 3.2 Debug & Inspectie modes

- `--dump-regs`  
  Toon:
  - alle SN76489 registers
  - afgeleide state (frekwensies, noise mode)
  - voice allocation (v0.05)

- `--counters`  
  Toon:
  - register writes
  - render calls
  - frames gegenereer
  - MIDI events
  - envelope steps

- `--debug` (rate-limited)  
  Mens-leesbare debug output vir:
  - MIDI events
  - voice allocation
  - envelope transitions

---

## 4. Gebruikersverhaal (v0.05)

> “Ek wil SN76489 kan speel soos ’n instrument:  
> akkoorde, note met sustain, pitch bends,  
> sonder clicks en sonder dat ek oor registers hoef te dink.”

---

## 5. Hoofdfokus: Pad A — v0.05 Muzikaliteit & Speelbaarheid

### 5.1 Voice Allocation (polyfonie per chip)

**Doel**  
Gebruik **alle drie tone-kanale** van ’n chip vir akkoorde en polyfonie.

**Vereistes**
- Elke chip het 3 stemme:
  - tone0
  - tone1
  - tone2
- MIDI Note On:
  - kies eerste beskikbare stem
  - eenvoudige round-robin of first-free algoritme
- MIDI Note Off:
  - stem word vrygestel
- Geen voice stealing in v0.05

---

### 5.2 Envelope Uitbreiding (ADSR-lite)

**Doel**  
Meer musikale note, minder harde artefakte.

**Vereistes**
- Attack
- Decay
- Sustain (NUUT)
- Release (NUUT)

**Beperkings**
- Slegs volume register writes
- 4-bit volume (0–15)
- Geen DSP-envelopes

---

### 5.3 Pitch Bend (beperk)

- MIDI Pitch Bend ondersteuning
- Beperk reeks (bv. ±2 semitone)
- Pas tone period aan
- Geen vibrato of LFO

---

### 5.4 MIDI Speelbaarheid

Verbeterings bo v0.04:
- Akkoorde moontlik
- Sustain hou note
- Minder “chip clicks”
- Meer intuïtiewe DAW-respons

---

## 6. Debug & Kwaliteit (v0.05)

- Voice allocation sigbaar in `--dump-regs`
- Envelope state per stem (opsioneel)
- Counters:
  - voices_used
  - env_steps
- Alle v0.04 sanity checks bly geldig

---

## 7. Toekomstige Uitbreidings (Pad B, C, D)

### Pad B — Retro-authenticiteit
- VGM playback
- Clock-gedrag verfyning
- Hardware quirks
- Golden audio regressie

### Pad C — AI / Copilot Vergelyking
- Copilot implementeer selfde FS/TS
- Vergelyk klank, stabiliteit, foute
- Dokumentasie van AI-faalpatrone

### Pad D — Hardware Brug
- Python engine as golden reference
- MIDI/VGM → regte SN76489
- ESP32 + KiCad
- Software ↔ hardware validasie

---

## 8. Sanity Checks (v0.05)

Bestaande v0.04 checks plus:
- Akkoord test (3 note gelyk)
- Sustain test
- Release test
- Pitch bend stabiliteit

---

## 9. Plaas, Refleksie & Cleanup Checklist

### 9.1 Plaas
- Commit
- Tag known-good
- Geen feature creep

### 9.2 Refleksie
- Bly ons SN76489-getrou?
- Maak dit speel lekkerder?
- Is dit toetsbaar?

### 9.3 Cleanup
- Alle CLI flags gebruik
- Geen dooie code
- Registers bly bron van waarheid
- Copilot-vriendelik

---

## 10. Aanvaaringskriteria vir v0.05

v0.05 is suksesvol as:
- Polyfonie oor 3 tone-kanale werk
- ADSR-lite hoorbaar musikaler is
- Pitch bend werk sonder glitches
- MIDI speel voel instrumenteel
- Geen regressie teen v0.04

---

## 11. Vervolgstappe

Kies een:

1. **FS v1.6 verder verfyn**  
2. **FS v1.6 goedkeur** → Tegniese Spesifikasie (TS v1.4)  
3. **Eers refleksie / cleanup** (v0.04 → v0.05 checklist)

---
