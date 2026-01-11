# SN76489 IC Pinout (DIP-16)

Nette, breadboard- en KiCad-vriendelijke ASCII-weergave van de **klassieke TI SN76489**.

# Pinout
---

## Pin-functie overzicht (praktisch)

### Data bus
- **D0–D7 (pins 1–8)**  
  8-bit parallel data-bus  
  → afkomstig van **PCF8574**

---

### Control-signalen
- **WE (pin 9)** – *Write Enable*  
  - Korte puls per register-write  
  - Polariteit afhankelijk van wiring  
  - **Meest kritische signaal**

- **CLK (pin 10)** – *Clock input*  
  - Sommige chips/modules: **interne clock**  
  - Andere: **externe clock vereist** (typisch ±3.58 MHz)

- **CE (pin 11)** – *Chip Enable*  
  - Meestal **actief LOW**  
  - Vaak permanent LOW vastgelegd in V1

---

### Audio & voeding
- **AUDIO OUT (pin 12)**  
  - Mono analoog audio  
  - **Altijd AC-koppelen direct bij de chip**

- **+5V (pin 13)**  
  - Digitale voeding  
  - Verplicht:
    - 100 nF keramisch
    - 10 µF elco  
    (zo dicht mogelijk bij de pin)

- **GND (pin 14)**  
  - Digitale ground

---

### Overig
- **NC (pins 15–16)**  
  - Niet aangesloten

---

## Ontwerp-waarschuwing (belangrijk)

> **80 % van “geen geluid” bugs bij de SN76489 zit in:**
>
> - verkeerde **WE-polariteit**
> - ontbrekende of verkeerde **CLK**
> - **CE** per ongeluk niet actief

Controleer deze drie altijd **eerst met de scope** voordat je audio of firmware verdenkt.

---

# ASCII-schema — PCF8574 → SN76489 wiring

Dit document toont **exact** hoe je de **PCF8574 (I²C → parallel expander)** koppelt aan de  
**SN76489 PSG**, geschikt voor **breadboard**, **KiCad** en **firmware-afstemming**.

---

## 1. Overzicht (conceptueel)

ESP32 (I2C)
│
│  SDA / SCL
▼
┌───────────┐        8-bit parallel + strobe        ┌────────────┐
│ PCF8574   │ ───────────────────────────────────▶ │ SN76489    │
│ I2C exp.  │                                      │ PSG        │
└───────────┘                                      └────────────┘

---

## 2. Bit-voor-bit mapping (aanbevolen)

### PCF8574 → SN76489 data- en control-lijnen
PCF8574                          SN76489 (DIP-16)
────────                          ───────────────

P0  ───────────────────────────▶  D0   (pin 1)
P1  ───────────────────────────▶  D1   (pin 2)
P2  ───────────────────────────▶  D2   (pin 3)
P3  ───────────────────────────▶  D3   (pin 4)
P4  ───────────────────────────▶  D4   (pin 5)
P5  ───────────────────────────▶  D5   (pin 6)
P6  ───────────────────────────▶  D6   (pin 7)
P7  ───────────────────────────▶  D7   (pin 8)

WE_STROBE (PCF bit) ───────────▶  WE   (pin 9)
> 💡 **Aanbevolen keuze:** gebruik **PCF8574 P7 als WE**  
> → eenvoudig te maskeren en pulsen in firmware.

---

## 3. Control- en vaste pinnen (V1-afspraak)

SN76489 pin 11 (CE)   ─────────▶  GND_DIG   (altijd enabled)
SN76489 pin 10 (CLK)  ─────────▶  externe clock of module-clock
SN76489 pin 13 (+5V)  ─────────▶  +5V_DIG
SN76489 pin 14 (GND)  ─────────▶  GND_DIG

- **CE**: vast aan GND (geen software-control in V1)
- **CLK**: afhankelijk van chip/module (interne of externe clock)

---

## 4. Volledig ASCII-overzicht (breadboard-vriendelijk)
PCF8574                         SN76489
┌──────────┐                   ┌─────────────────┐
│ P0   ────┼──────────────────▶│ D0          16 │ NC
│ P1   ────┼──────────────────▶│ D1          15 │ NC
│ P2   ────┼──────────────────▶│ D2          14 │ GND
│ P3   ────┼──────────────────▶│ D3          13 │ +5V
│ P4   ────┼──────────────────▶│ D4          12 │ AUDIO OUT
│ P5   ────┼──────────────────▶│ D5          11 │ CE ──┐
│ P6   ────┼──────────────────▶│ D6          10 │ CLK  │
│ P7   ────┼─────┐             │ D7           9 │ WE ◀─┘
└──────────┘     │             └─────────────────┘
└── WE_STROBE

---

## 5. Firmware-implicatie (essentieel)

### Write-sequence (PCF8574 → SN76489)

```python
pcf.set_data(byte)     # zet D0..D7
pcf.pulse_strobe()    # pulse WE

Stappen:
	1.	Data-byte op P0–P7
	2.	Korte settle-tijd
	3.	WE-puls (actief LOW of HIGH)
	4.	Write voltooid

