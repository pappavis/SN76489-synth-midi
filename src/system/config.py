# system/config.py
# Central configuration for the SN76489 MIDI synth (CircuitPython)

# I2C
I2C_FREQ = 100_000
PCF_ADDR = 0x20
OLED_ADDR = 0x3C  # common SSD1306 address

# Pins (set these to your actual ESP32-C2 board pins)
# NOTE: CircuitPython uses board.SCL / board.SDA for I2C by default.
# For control/strobe via PCF8574, we treat those as bits on the PCF port.
# Choose which PCF bit is used for WRITE STROBE (WE).
PCF_STROBE_BIT = 7  # P7 used as strobe by default (0..7)

# Strobe polarity
# If your SN76489 write enable is active-low, set True so pulse drives low then high.
STROBE_ACTIVE_LOW = True

# Timing (conservative; tune later)
DATA_SETTLE_US = 50
STROBE_PULSE_US = 50
POST_WRITE_US = 50

# Debug
DEBUG = True

# Test modes
# Set to one of: None, "pcf_counter", "sn_beep"
TEST_MODE = "pcf_counter"
