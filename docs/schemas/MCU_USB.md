
## MCU_USB.sch — ESP32-S2 header naar I²C (en power)

> ESP32-S2 pin-nummers verschillen per board. Dit is **functionele pinout** (headers).  
> Jij koppelt hier alleen: **+5V_IN, GND_IN, SDA, SCL**.

J2 ESP32-S2 HDR (voorbeeld 1x06)
1: +5V_IN   (van USB 5V)
2: GND_IN
3: SDA      (I2C data)
4: SCL      (I2C clock)
5: GPIOx    (optioneel, later)
6: GPIOy    (optioneel, later)

Netten:
J2.1 → +5V_IN
J2.2 → GND_IN
J2.3 → SDA
J2.4 → SCL

