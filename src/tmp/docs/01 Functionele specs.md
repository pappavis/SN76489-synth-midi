Hier is FS v1.6 volledig hergenereerd, opgeschoond en kopieer-plak-klaar voor GitHub als .md.
Ik heb Pad A (v0.05 Muzikaliteit & speelbaarheid) volledig geïntegreerd, én expliciet Pad B, C, D benoemd zoals gevraagd, plus een nieuw hoofdstuk voor plaats, reflectie & cleanup.

Je kunt dit 1-op-1 in GitHub zetten.

⸻


# Funksionele Spesifikasie (FS) v1.6  
## SN76489 PSG Emulasie in Python (MacOS)

**Datum:** 2 Februarie 2026  
**Status:** FS v1.6 (uitgebreid ná goedgekeurde v0.04)  
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
- Per-chip musikale gedrag (nie net “beep engine” nie)

### 2.2 Uitdruklik buite scope vir v0.05

- VST/AU plugin
- Sample-accurate MIDI scheduling
- Effects (reverb, delay, filters)
- Grafiese UI

---

## 3. Gebruikersverhaal (v0.05)

> “Ek wil SN76489 kan speel soos ’n instrument:  
> akkoorde, note met sustain, pitch bends,  
> sonder clicks en sonder dat ek oor registers hoef te dink.”

---

## 4. Hoofdfokus: Pad A — v0.05 Muzikaliteit & Speelbaarheid

### 4.1 Voice Allocation (polyfonie per chip)

#### Doel
Gebruik **alle drie tone-kanale** van ’n chip om akkoorde en polyfonie moontlik te maak.

#### Vereistes
- Elke chip het 3 stemme:
  - tone0
  - tone1
  - tone2
- MIDI Note On:
  - kies eerste beskikbare stem
  - eenvoudige round-robin of first-free algoritme
- MIDI Note Off:
  - stem word vrygestel
- Geen voice stealing in v0.05 (later moontlik)

#### Belangrik
- Stem-toewysing is **logies**, nie hardware-magic nie
- Register writes bly per tone-kanaal

---

### 4.2 Envelope Uitbreiding (ADSR-lite)

#### Doel
Meer musikale note, minder harde artefakte.

#### Vereistes (v0.05)
- Attack (bestaand)
- Decay (bestaand)
- Sustain (NUUT)
- Release (NUUT)

#### Beperkings
- Alles via **volume register writes**
- 4-bit volume domein (0–15)
- Geen modulering buite SN76489 model

CLI uitbreiding (voorstel):
- `--attack-ms`
- `--decay-ms`
- `--sustain-vol`
- `--release-ms`

---

### 4.3 Pitch Bend (beperk)

#### Doel
Basiese expressie vir MIDI controllers.

#### Vereistes
- Ondersteun MIDI Pitch Bend
- Beperk reeks (bv. ±2 semitone)
- Pas tone period aan (nie volume nie)

#### Beperkings
- Geen sample-accurate sweeps
- Geen vibrato/LFO (later)

---

### 4.4 MIDI Speelbaarheid

Verbeterings bo v0.04:
- Akkoorde moontlik
- Note hou (sustain)
- Minder “chip clicks”
- Meer intuïtiewe response vanuit DAW

---

## 5. Debug & Kwaliteit (v0.05)

- Voice allocation status in `--dump-regs`
- Envelope state per stem (opsioneel)
- Counters:
  - voices_used
  - voice_steals (indien later)
- Alle v0.04 sanity checks bly geldig

---

## 6. Toekomstige Uitbreidings (NUUT, eksplisiet)

### Pad B — Retro-authenticiteit
- VGM playback
- Clock-gedrag verfyning
- Hardware quirks (TI vs Sega)
- Golden audio regression hashes

### Pad C — AI / Copilot Vergelyking
- Copilot implementeer selfde FS/TS
- Vergelyk:
  - API korrektheid
  - klankstabiliteit
  - foutpatrone
- Dokumentasie: “Waar AI’s faal by emulator-ontwerp”

### Pad D — Hardware Brug
- Python engine as “golden reference”
- MIDI/VGM → regte SN76489 chip
- ESP32 firmware + KiCad ontwerp
- Software ↔ hardware validasie

---

## 7. Sanity Checks (v0.05 uitbreiding)

Bestaande v0.04 checks bly geldend, plus:

- Akkoord test (3 note gelyk)
- Sustain test (note hou sonder artefakte)
- Release test (gladde afsterf)
- Pitch bend hoorbaar maar stabiel

---

## 8. Plaas, Refleksie & Cleanup Checklist (NUUT)

Hierdie hoofstuk is **bewus nie-tegnies**, maar noodsaaklik vir kwaliteit.

### 8.1 Plaas (pause)

Voor elke nuwe iterasie:
- Stop
- Commit huidige werk
- Merk “known good”
- Moenie momentum bo stabiliteit kies nie

---

### 8.2 Refleksie

Vrae om te beantwoord:
- Is hierdie uitbreiding regtig nodig?
- Bly ons binne SN76489 se karakter?
- Maak dit die instrument **lekkerder** om te speel?

---

### 8.3 Cleanup Checklist

Voor volgende weergawe:
- Alle sanity checks slaag
- Geen ongebruikte CLI flags
- Debug output is leesbaar
- Registers bly bron van waarheid
- Code bly verstaanbaar vir Copilot én mens

---

## 9. Aanvaaringskriteria vir v0.05

v0.05 is suksesvol as:

- Polyfonie oor 3 tone-kanale werk
- ADSR-lite hoorbaar musikaler is
- Pitch bend werk sonder glitches
- MIDI speel voel “instrumenteel”
- Geen regressie teen v0.04

---

## 10. Vervolgstappe

Kies een:

1. **FS v1.6 verfyn**  
   → “FS pas aan: …”

2. **FS v1.6 goedkeur**  
   → Ek skryf **Tegniese Spesifikasie (TS v1.4)** vir v0.05

3. **Eers refleksie / cleanup**  
   → Ek maak ’n v0.04 → v0.05 voorbereidings-checklist

---


⸻

👉 Jou beurt
Wil jy:
	•	FS v1.6 goedkeur,
	•	eers verfyn, of
	•	kort pas op die plaas doen voor TS v1.4?