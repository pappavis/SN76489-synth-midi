# drivers/sn76489.py
# Minimal SN76489 driver that writes bytes via a PCF8574 parallel bridge.
import time

class SN76489:
    def __init__(self, pcf, debug=False):
        self.pcf = pcf
        self.debug = debug

    def write_byte(self, value: int):
        """Write a raw byte to the SN76489."""
        if self.debug:
            print("SN76489 write:", hex(value & 0xFF))
        self.pcf.write(value & 0xFF)

    def mute_all(self):
        """Best-effort mute: set volumes to max attenuation for channels 0-3."""
        # Latch/volume bytes: 1ccc vvvv (0x90/0xB0/0xD0/0xF0 base)
        for ch in range(4):
            self.write_byte(0x90 | (ch << 5) | 0x0F)

    def beep(self, note_byte_sequence=None, duration_ms=300):
        """Simple beep test: writes a fixed tone + volume. Not musically accurate yet.
        This is for MP3/MP4 bring-up only.
        """
        # Minimal: set channel 0 volume to loud (0x00) and set some tone value.
        # SN76489 tone uses 10-bit divider written as latch + data.
        # We'll use a hardcoded divider. You can tune later.
        divider = 0x100  # placeholder
        # Latch tone for ch0: 1 0 c c dddd  (0x80 base), lower 4 bits
        latch = 0x80 | (0 << 5) | (divider & 0x0F)
        data  = (divider >> 4) & 0x3F  # 6 bits
        self.write_byte(latch)
        self.write_byte(data)
        # Volume ch0: base 0x90, atten 0..15 (0 loud, 15 mute)
        self.write_byte(0x90 | 0x00)
        time.sleep(duration_ms / 1000)
        self.write_byte(0x90 | 0x0F)
