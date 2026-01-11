# system/diagnostics.py
import time

def i2c_scan(i2c, debug=False):
    while not i2c.try_lock():
        pass
    try:
        addrs = i2c.scan()
    finally:
        i2c.unlock()
    if debug:
        print("I2C scan:", [hex(a) for a in addrs])
    return addrs

def pcf_counter_test(pcf, oled=None, debug=False, delay_ms=50):
    """Counts 0x00..0xFF on the PCF data bus (MP2 check)."""
    if oled:
        oled.show_lines(["TEST", "PCF counter"])
    for v in range(256):
        pcf.set_data(v)
        if debug and (v % 16 == 0):
            print("PCF data:", hex(v))
        time.sleep(delay_ms / 1000)

def sn_beep_test(sn, oled=None, debug=False):
    if oled:
        oled.show_lines(["TEST", "SN beep"])
    sn.beep(duration_ms=300)
    time.sleep(0.2)
    sn.beep(duration_ms=300)
