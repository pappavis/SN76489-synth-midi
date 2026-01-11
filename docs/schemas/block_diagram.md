# End-to-end verbindingen (gevraagd expliciet)

## 1) ESP32-S2 → PCF8574(AP)

ESP32 SDA ───────────────> PCF SDA
ESP32 SCL ───────────────> PCF SCL
+5V_IN  ────────────────> +5V_DIG → PCF VCC
GND_IN  ────────────────> GND_DIG → PCF GND
SDA/SCL pullups: 4k7 naar +5V_DIG

## 2) PCF8574(AP) → SN76489
PCF P0..P7 ─────────────> SN D0..D7 (pins 1..8)
PCF WE_STROBE ──────────> SN WE (pin 9)
SN CE (pin 11) ─────────> GND_DIG
SN CLK (pin 10) ─────────> SN_CLK (extern of module)

## 3) SN76489 → audio-architectuur
SN AUDIO OUT (pin 12) ──> PSG_AUDIO_RAW
PSG_AUDIO_RAW ── C_IN ──> AUDIO_IN ──> pot ──> AUDIO_POST_POT ──> opamp ──> AUDIO_AMP_OUT
AUDIO_AMP_OUT ──> (R_OUT + C_OUT) ──> TRS TIP/RING (dual-mono)
TRS SLEEVE ──> GND_AUD
