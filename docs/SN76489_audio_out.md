# ASCII-schema — SN76489 audio-out + AC-koppeling (V1)

Doel:
- SN76489 **mono audio** netjes uit de chip halen
- **DC blokkeren** en ruis/rommel beperken
- Signaal correct aanbieden aan:
  - volumepot (vóór versterker)
  - versterker (Optie B aanbevolen)
  - dual-mono koptelefoon-out

---

## 1. Minimalistisch en werkend (V1 “bring-up”)

Dit is de snelste variant die meestal meteen geluid geeft.

SN76489
AUDIO OUT (pin 12)
│
│   C_IN 1µF–10µF  (AC-koppeling, + richting chip bij elco)
├──||───●───────────────> naar volumepot “TOP”
│       │
│       R_BIAS 100k
│       │
GND ─────┴────────────────> GND_AUD

**Wat dit doet**
- `C_IN` blokkeert DC uit de chip
- `R_BIAS` voorkomt zweven/ploppen en definieert impedantie

**Startwaarden**
- `C_IN = 1 µF` (film als je hebt, anders elco)
- `R_BIAS = 100 kΩ`

---

## 2. Aanbevolen V1 audio-pad (met volumepot vóór amp)

SN76489 pin 12 (AUDIO)
│
│  C_IN 1µF–10µF
├──||───────●───────────────> POT_TOP
│           │
│           R_BIAS 100k
│           │
GND_AUD────────┴────────────────> POT_GND

### Volumepot (mono, 10k–50k log)
POT_TOP  o—–> audio in
POT_WIPER o––> AUDIO_POST_POT (naar versterker)
POT_GND  o—–> GND_AUD

**Praktisch advies**
- Potmeter: **10 kΩ log** is een goede default
- Wiper is je meetpunt **MP5**

---

## 3. Optie B ingang (opamp met virtuele ground) — correct koppelen

Als je Optie B gebruikt (opamp + Vref), dan wil je de input **rond Vref biasen**.

AUDIO_POST_POT
│
│  C_OPIN 100n–1µF   (AC-koppeling naar opamp-input)
├──||──●──────────────> opamp + input
│      │
│      R_TO_VREF 100k
│      │
VREF_AUD (2.5V) ———> (virtuele ground)

**Waarom**  
- Opamp kan niet onder 0 V op single-supply  
- Dus je centreert audio rond **VREF_AUD**

---

## 4. Koptelefoon dual-mono uitgang (na versterker, DC-safe)

Na de versterker wil je **geen DC** naar je koptelefoon.

AMP_OUT
│
├─ R_OUT_L 47Ω ──|| C_OUT_L 220–470µF ──> TIP (L)
│
└─ R_OUT_R 47Ω ──|| C_OUT_R 220–470µF ──> RING (R)

SLEEVE –––––––––––––––––> GND_AUD

(aanrader tegen plop)
TIP  ── R_BLEED_L 100k ──> GND_AUD
RING ── R_BLEED_R 100k ──> GND_AUD

**Startwaarden**
- `R_OUT = 47 Ω`
- `C_OUT = 220 µF` (32 Ω → fc ~ 22 Hz)  
  Wil je meer laag: `470 µF`
- `R_BLEED = 100 kΩ`

---

## 5. Waar het vaak fout gaat (snelle checklist)

- ❌ `C_IN` te ver van SN76489 → pikt digitale rommel op  
  ✅ zet `C_IN` fysiek **dicht bij pin 12**
- ❌ audio ground via digitale ground terug  
  ✅ `GND_AUD` star-point bij power entry
- ❌ geen bias/bleeder → ploppen, zweven  
  ✅ `R_BIAS` en `R_BLEED` plaatsen
- ❌ DC naar koptelefoon  
  ✅ altijd `C_OUT` in serie naar L/R

---

## 6. Meetpunten (scope)

- **MP4:** direct op SN76489 pin 12 → klein AC signaal  
- **MP5:** pot-wiper → amplitude verandert met pot  
- **MP6:** tip en ring → identiek, DC ~ 0 V

---

## Aanbevolen componenten (THT)

- C_IN: 1 µF (film) of elco
- R_BIAS: 100 kΩ
- Pot: 10–50 kΩ log
- R_OUT: 47 Ω (2×)
- C_OUT: 220–470 µF (2×)
- R_BLEED: 100 kΩ (2×)

---

Als je wilt, maak ik hierna ook een **ASCII “layout hint”** (waar je C_IN en R_BIAS fysiek op breadboard moet zetten om digitale piep te vermijden).
