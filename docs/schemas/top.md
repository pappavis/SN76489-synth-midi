# ASCII “KiCad-style” wiring per sheet (Top + subsheets)
> **NOTE (belangrijk):** jij schreef **PCF9574AP**. In vrijwel alle hobby-modules en datasheets is dit **PCF8574 / PCF8574A / PCF8574AP** (zelfde functie; “A/AP” = ander I²C-adresbereik).  [oai_citation:0‡ti.com](https://www.ti.com/lit/ds/symlink/pcf8574.pdf?utm_source=chatgpt.com)  
> Hieronder ga ik uit van **PCF8574(AP)** als 8-bit I²C GPIO expander.

---

## Top.sch — systeem-overzicht (netten & blokken)
USB 5V/GND
│
├─────────────── +5V_IN ───────────────┐
│                                      │
└─────────────── GND_IN ───────────────┘
│  (STAR-POINT)
┌───────────┴───────────┐
│                       │
+5V_DIG                 +5V_AUD
GND_DIG                 GND_AUD

ESP32-S2 (USB MIDI + I2C master)
├── SDA ───────────────┐
└── SCL ───────────────┘
│
▼
PCF8574(AP)  (I2C→8-bit)
P0..P7 + (WE strobe bit)
│  D0..D7 + WE
▼
SN76489
│  PSG_AUDIO_RAW
▼
AC-koppeling → pot → opamp amp → dual-mono → TRS jack


---

## Power.sch — voeding & star-point

### Pinout / connectors
J1 POWER_IN (2-pin)
Pin1: +5V_IN
Pin2: GND_IN

### Net-splitsing (conceptueel)
+5V_IN  ──┬──> +5V_DIG
└──> +5V_AUD

GND_IN  ──┬──> GND_DIG
└──> GND_AUD

**PCB bedoeling:** +5V en GND splitsen in DIG/AUD en **maar op één punt** samenbrengen (star-point).

---
