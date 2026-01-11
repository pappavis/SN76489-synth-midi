# main.py
import time
import board
import busio

from system import config
from system.diagnostics import i2c_scan, pcf_counter_test, sn_beep_test
from drivers.pcf8574 import PCF8574
from drivers.sn76489 import SN76489
from drivers.oled_status import OLEDStatus

def log(*args):
    if config.DEBUG:
        print(*args)

def init_i2c():
    i2c = busio.I2C(board.SCL, board.SDA, frequency=config.I2C_FREQ)
    # Wait for I2C to become ready
    t0 = time.monotonic()
    while not i2c.try_lock():
        if time.monotonic() - t0 > 2:
            break
    try:
        # quick unlock if we locked
        if i2c.try_lock():
            i2c.unlock()
    except Exception:
        pass
    return i2c

def main():
    log("BOOT")
    i2c = init_i2c()

    # OLED is optional; it must never block the system
    oled = OLEDStatus(i2c, address=config.OLED_ADDR, debug=config.DEBUG)
    oled.splash("BOOT")

    addrs = i2c_scan(i2c, debug=config.DEBUG)
    oled.show_lines(["I2C scan OK", " ".join([hex(a) for a in addrs[:4]])])

    # PCF8574 (required for SN76489 writes)
    pcf = PCF8574(
        i2c,
        address=config.PCF_ADDR,
        strobe_bit=config.PCF_STROBE_BIT,
        active_low=config.STROBE_ACTIVE_LOW,
        data_settle_us=config.DATA_SETTLE_US,
        strobe_pulse_us=config.STROBE_PULSE_US,
        post_write_us=config.POST_WRITE_US,
        debug=config.DEBUG
    )

    # SN76489 driver (bridged via PCF)
    sn = SN76489(pcf, debug=config.DEBUG)
    sn.mute_all()

    # Test modes for bring-up
    if config.TEST_MODE == "pcf_counter":
        log("Running PCF counter test (MP2)")
        pcf_counter_test(pcf, oled=oled, debug=config.DEBUG, delay_ms=50)
    elif config.TEST_MODE == "sn_beep":
        log("Running SN beep test (MP3/MP4)")
        sn_beep_test(sn, oled=oled, debug=config.DEBUG)
    else:
        oled.show_lines(["READY", "Waiting MIDI..."])
        log("READY (no MIDI implemented in this skeleton)")
        while True:
            time.sleep(0.5)

if __name__ == "__main__":
    main()
