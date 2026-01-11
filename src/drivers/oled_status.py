# drivers/oled_status.py
# Minimal OLED status wrapper. Safe fallback if OLED lib is unavailable.
import time

class OLEDStatus:
    def __init__(self, i2c, address=0x3C, debug=False):
        self.i2c = i2c
        self.address = address
        self.debug = debug
        self._ready = False
        self._init_display()

    def _init_display(self):
        try:
            import adafruit_ssd1306
            self.display = adafruit_ssd1306.SSD1306_I2C(128, 64, self.i2c, addr=self.address)
            self.display.fill(0)
            self.display.show()
            self._ready = True
        except Exception as e:
            self._ready = False
            self.display = None
            if self.debug:
                print("OLED disabled:", e)

    @property
    def ready(self):
        return self._ready

    def show_lines(self, lines):
        """Display up to ~6 lines. If OLED not present, just prints."""
        if not isinstance(lines, (list, tuple)):
            lines = [str(lines)]
        if not self._ready:
            if self.debug:
                print("OLED:", " | ".join(lines))
            return
        try:
            import terminalio
            from adafruit_display_text import label
            from adafruit_display_text import wrap_text_to_lines

            self.display.fill(0)
            y = 0
            for line in lines[:6]:
                text_area = label.Label(terminalio.FONT, text=str(line), x=0, y=y+8, color=1)
                self.display.show(text_area)
                y += 10
            self.display.show()
        except Exception as e:
            if self.debug:
                print("OLED draw error:", e)

    def splash(self, title="BOOT", delay_s=0.2):
        self.show_lines([title])
        time.sleep(delay_s)
