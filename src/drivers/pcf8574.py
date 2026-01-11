# drivers/pcf8574.py
import time
try:
    from micropython import const
except Exception:
    def const(x): return x

class PCF8574:
    """Minimal PCF8574 driver for CircuitPython.
    Provides an 8-bit output port and a dedicated strobe pulse on a chosen bit.
    """

    def __init__(self, i2c, address=0x20, strobe_bit=7, active_low=True,
                 data_settle_us=50, strobe_pulse_us=50, post_write_us=50, debug=False):
        self.i2c = i2c
        self.address = address
        self.strobe_bit = strobe_bit
        self.active_low = active_low
        self.data_settle_us = data_settle_us
        self.strobe_pulse_us = strobe_pulse_us
        self.post_write_us = post_write_us
        self.debug = debug

        # Current output latch (8-bit)
        self._port = 0x00

        # Initialize strobe to idle state
        self._set_strobe(idle=True)
        self._write_port()

    def _write_port(self):
        # PCF8574 writes one byte to set port state
        data = bytes([self._port & 0xFF])
        while not self.i2c.try_lock():
            pass
        try:
            self.i2c.writeto(self.address, data)
        finally:
            self.i2c.unlock()

    def _set_strobe(self, idle: bool):
        mask = 1 << self.strobe_bit
        if self.active_low:
            # idle = high, active = low
            if idle:
                self._port |= mask
            else:
                self._port &= ~mask
        else:
            # idle = low, active = high
            if idle:
                self._port &= ~mask
            else:
                self._port |= mask

    def set_data(self, value: int):
        """Set D0..D7 (includes strobe bit; so we preserve strobe state explicitly)."""
        # Preserve strobe bit, replace the others
        strobe_mask = 1 << self.strobe_bit
        strobe_state = self._port & strobe_mask
        self._port = (value & 0xFF)
        # restore strobe state
        self._port = (self._port & ~strobe_mask) | strobe_state
        self._write_port()
        if self.data_settle_us:
            time.sleep(self.data_settle_us / 1_000_000)

    def pulse_strobe(self):
        """Pulse write enable/strobe."""
        self._set_strobe(idle=False)
        self._write_port()
        if self.strobe_pulse_us:
            time.sleep(self.strobe_pulse_us / 1_000_000)
        self._set_strobe(idle=True)
        self._write_port()
        if self.post_write_us:
            time.sleep(self.post_write_us / 1_000_000)

    def write(self, value: int):
        """Convenience: set data then pulse strobe."""
        self.set_data(value)
        self.pulse_strobe()

    def debug_port(self) -> int:
        return self._port & 0xFF
