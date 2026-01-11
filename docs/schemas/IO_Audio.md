# IO_Audio.sch — SN76489 audio → AC-koppeling → pot → amp → TRS

### SN audio-out + AC-koppeling (direct bij chip)

PSG_AUDIO_RAW
│
├──|| C_IN (C4) 1u–10u ──●──> AUDIO_IN
│                        │
│                      R_BIAS (R5) 100k
│                        │
GND_AUD ────────────────────┘

### Volumepot (extern via header J4)
J4 POT_VOL (3-pin)
Pin1: POT_TOP   ← AUDIO_IN
Pin2: POT_WIPER → AUDIO_POST_POT
Pin3: POT_GND   → GND_AUD

### Amp output naar dual-mono koptelefoon
AUDIO_AMP_OUT
├─ R_OUT_L (R6) 47Ω ──|| C_OUT_L (C5) 220–470u ──> AUDIO_L ──> TRS TIP
└─ R_OUT_R (R7) 47Ω ──|| C_OUT_R (C6) 220–470u ──> AUDIO_R ──> TRS RING

TRS SLEEVE → GND_AUD

(anti-plop)
AUDIO_L ── R_BLEED_L 100k ──> GND_AUD
AUDIO_R ── R_BLEED_R 100k ──> GND_AUD


# ASCII-schema — SN76489 → LM386 (gain = 20 dB) + “LM_AUDIO” output label

Gebaseerd op TI LM386 datasheet **minimum-parts** layout (Gain = 20 dB) met:
- **Zobel**: 10 Ω + 0.05 µF vanaf output naar GND
- **Output coupling**: 250 µF in serie naar de load  
 [oai_citation:0‡ti.com](https://www.ti.com/lit/ds/symlink/lm386.pdf?utm_source=chatgpt.com)

> Gain = **20 dB** bij LM386 wanneer **pins 1 en 8 open** blijven.  [oai_citation:1‡ti.com](https://www.ti.com/lit/ds/symlink/lm386.pdf?utm_source=chatgpt.com)

---

## 1) SN76489 audio-out → LM386 input (AC-koppeling)
SN76489 (pin 12) PSG_AUDIO_RAW
│
│   C_IN 1µF–10µF  (AC-koppeling; + richting SN als elco)
├──||───●──────────────> LM386 IN+ (pin 3)
│       │
│       R_BIAS 100k
│       │
GND_AUD──┴────────────────> LM386 GND (pin 4)  [en SN GND]

---

## 2) LM386 (PDIP-8) — minimum parts, gain = 20 dB

            LM386 (PDIP-8)
         ┌─────────────────────────┐
GAIN 1  1│                        8│  GAIN 2      (pins 1 & 8 OPEN → gain 20 dB)
IN-     2│                        7│  BYPASS      (optioneel: 10µF naar GND voor minder brom/ruis)
IN+     3│                        6│  +5V
GND     4│                        5│  OUT  =  LM_AUDIO
         └─────────────────────────┘

### Voeding + ontkoppeling (sterk aanbevolen, ook op breadboard)
+5V  ──┬──────────────> LM386 pin 6
│
├──|| 100n ─────> GND
└──|| 100µF ────> GND   (bulk dichtbij IC)



x
