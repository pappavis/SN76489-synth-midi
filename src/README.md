# CircuitPython Skeleton (SN76489 + PCF8574)



# Instructies
Hier is je minimale CircuitPython skeleton als ZIP (main.py + drivers + config + diagnostics):

Download sn76489_circuitpython_skeleton.zip￼

Gebruik (kort):
	1.	Unzip.
	2.	Kopieer de inhoud naar je CIRCUITPY drive.
	3.	Zet in system/config.py je PCF_ADDR en (indien nodig) PCF_STROBE_BIT.
	4.	Start met TEST_MODE = "pcf_counter" (scope op D0..D7 + strobe).
	5.	Daarna TEST_MODE = "sn_beep" (scope op strobe + audio out).

## Wat is dit?
Minimale bring-up firmware voor:
- I2C scan (MP1)
- PCF8574 data togglen (MP2)
- SN76489 byte writes + simpele beep (MP3/MP4)
- OLED status (optioneel; faalt veilig)

## Installatie (CircuitPython)
1. Flash CircuitPython op je ESP32-C2 board.
2. Kopieer de hele inhoud van deze map naar de CIRCUITPY drive.
3. Installeer (optioneel) OLED libs als je het display gebruikt:
   - adafruit_ssd1306.mpy
   - adafruit_display_text/
   - terminalio (meestal ingebouwd)

## Test modes
In `system/config.py`:
- `TEST_MODE = "pcf_counter"`  → PCF bus telt 0..255 (scope op D0..D7)
- `TEST_MODE = "sn_beep"`      → SN76489 korte beep
- `TEST_MODE = None`           → idle loop

## Belangrijk
- Dit skeleton bevat nog geen USB-MIDI parser.
- Eerst hardware brengen naar "beep" en "stabiele bus". Daarna MIDI laag toevoegen.
