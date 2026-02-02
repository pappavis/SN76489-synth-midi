# SN76489 Emulator v0.05 (Python, MacOS)

Datum: 2 Februarie 2026  
Python: 3.12  
MacOS: 26.2  
Artefak: één Python-bestand: `sn76489_emulator.py`  
Gebaseer op: FS v1.6 + TS v1.4 (goedgekeur)

v0.05 voeg by (muzikaliteit & speelbaarheid):
- Polyfoniese voice allocation per chip (tone0/tone1/tone2)
- ADSR-lite envelope (Attack/Decay/Sustain/Release) via volume register-writes
- Pitch bend (±2 semitone) → period updates vir aktiewe stemme
- Nuwe tests: `--test chords`, `--test sweep`
- Uitgebreide `--dump-regs` (voice+envelope) en `--counters` (voices/env/pitchbend)

Bewus nie in v0.05:
- Geen voice stealing
- Geen vibrato/LFO
- Geen sample-accurate scheduling
- Geen VST/AU plugin

---

## Install notes (audio + MIDI libs)

Audio:
pip install numpy sounddevice

MIDI (CoreMIDI op Mac):
pip install python-rtmidi

---

## Gebruik / CLI examples

Basiese tests:
python sn76489_emulator.py --test beep
python sn76489_emulator.py --test noise --noise-mode white --noise-rate div32 --noise-seed 0x4000
python sn76489_emulator.py --test sequence --attack-ms 5 --decay-ms 80 --sustain-vol 8 --release-ms 120

Nuus (v0.05):
python sn76489_emulator.py --test chords --attack-ms 5 --decay-ms 60 --sustain-vol 8 --release-ms 180
python sn76489_emulator.py --test sweep --seconds 2

MIDI:
python sn76489_emulator.py --midi-list
python sn76489_emulator.py --midi-in --chips 2 --pan both --attack-ms 5 --decay-ms 60 --sustain-vol 8 --release-ms 160

Debug:
python sn76489_emulator.py --test chords --dump-regs --counters
python sn76489_emulator.py --midi-in --debug --counters

---

## Sanity check checklist (copy/paste)

1) Audio path:
python sn76489_emulator.py --test beep

2) Multi-chip + routing left:
python sn76489_emulator.py --test beep --chips 2 --pan left

3) Routing right:
python sn76489_emulator.py --test beep --chips 2 --pan right

4) Mixer/gain:
python sn76489_emulator.py --test beep --pan both --master-gain 0.15

5) Noise determinisme (run 2x, moet identies klink):
python sn76489_emulator.py --test noise --noise-mode white --noise-seed 0x4000 --noise-rate div32 --seconds 1
python sn76489_emulator.py --test noise --noise-mode white --noise-seed 0x4000 --noise-rate div32 --seconds 1

6) Sequence + ADSR-lite:
python sn76489_emulator.py --test sequence --attack-ms 5 --decay-ms 80 --sustain-vol 8 --release-ms 140

7) Akkoord (3 stemme) + ADSR-lite:
python sn76489_emulator.py --test chords --attack-ms 5 --decay-ms 60 --sustain-vol 8 --release-ms 180

8) Sweep (period updates):
python sn76489_emulator.py --test sweep --seconds 2

9) MIDI smoke test:
python sn76489_emulator.py --midi-list
python sn76489_emulator.py --midi-in
# stuur note-on/off vanuit Ableton/Logic, stop met Ctrl+C

Pass = hoorbare output waar verwag + geen crash/hang.  
Fail = geen geluid / crash / determinisme klink anders.

---

## Rollback hint na v0.04

Minimum rollback:
- hou `sn76489_emulator_v0.04.py` as known-good kopie
OF beter:
- tag jou git commits: v0.04 (known good), v0.05 (candidate)

As ’n sanity check faal: revert na v0.04 onmiddellik.