## I2C_Bus.sch — ESP32-S2 → PCF8574(AP) (+ OLED)

### I²C bus + pullups
SDA ──┬──────────> PCF8574 SDA
└──────────> OLED SDA
|
└─ R1 4k7 ──> +5V_DIG

SCL ──┬──────────> PCF8574 SCL
└──────────> OLED SCL
|
└─ R2 4k7 ──> +5V_DIG

PCF8574 VCC → +5V_DIG
PCF8574 GND → GND_DIG
OLED VCC    → +5V_DIG (of 3V3 als jouw display dat vereist)
OLED GND    → GND_DIG

### PCF8574(AP) pinout (DIP-16, functioneel)
*(Pin-nummers kunnen per fabrikant gelijk zijn, maar gebruik dit als “kaart” voor je wiring)*

### PCF8574(AP) pinout (DIP-16, functioneel)
*(Pin-nummers kunnen per fabrikant gelijk zijn, maar gebruik dit als “kaart” voor je wiring)*

PCF8574(AP) (DIP-16) — kernsignalen
SDA, SCL : I2C bus
A0,A1,A2 : adresselectie (naar GND of +5V_DIG)
P0..P7   : 8 GPIO’s → SN76489 data/strobe
INT      : (optioneel) interrupt naar MCU (niet nodig in V1)
VCC      : +5V_DIG
GND      : GND_DIG

### Parallel uit (PCF → SN)
**Aanbevolen mapping:**

PCF P0 → D0 (SN pin 1)
PCF P1 → D1 (SN pin 2)
PCF P2 → D2 (SN pin 3)
PCF P3 → D3 (SN pin 4)
PCF P4 → D4 (SN pin 5)
PCF P5 → D5 (SN pin 6)
PCF P6 → D6 (SN pin 7)
PCF P7 → D7 (SN pin 8)

WE_STROBE (PCF bit, vaak P7 of extra gating) → WE (SN pin 9)

