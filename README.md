# Stap 1 – Functionele specificaties  
**DIY USB-MIDI PSG-synth (SN76489 + ESP32-C2)**

# SN76489 USB-MIDI Synth (ESP32-C2)

Educatieve DIY USB-MIDI synthesizer gebaseerd op de SN76489 PSG,
aangestuurd via een ESP32-C2 met CircuitPython en een PCF8574
(I2C → parallel).

## Ontwerpfilosofie
- Eerst breadboard, dan PCB
- Alles meetbaar met scope en multimeter
- Geen SMD-componenten
- Focus op leerbaarheid en reproduceerbaarheid

## Signaalpad (verplicht)
ESP32-C2 (USB MIDI)
→ PCF8574
→ SN76489
→ analoge filtering
→ variabel mono volume
→ audio-versterker
→ 3.5 mm TRS koptelefoon (dual-mono)

## Projectstatus
- [x] Stap 1 – Functionele specificaties
- [ ] Stap 2 – Technische specificaties
- [ ] Stap 3 – Blokdiagram
- [ ] Stap 4 – Breadboard ontwerp
- [ ] Stap 5 – Audio-versterker evaluatie
- [ ] Stap 6 – KiCad schema & PCB
- [ ] Stap 7 – Firmware architectuur
- [ ] Stap 8 – Test & debug
- [ ] Stap 9 – Verbeteringen

➡️ Begin bij `docs/01-functional-spec.md`
sn76489-midi-synth/
├── README.md
├── docs/
│   ├── 01-functional-spec.md
│   ├── 02-technical-spec.md
│   ├── 03-block-diagram.md
│   ├── 04-breadboard-design.md
│   ├── 05-audio-options-evaluation.md
│   ├── 06-kicad-design.md
│   ├── 07-firmware-architecture.md
│   ├── 08-test-and-debug.md
│   └── 09-improvements-and-next-steps.md
├── hardware/
│   ├── breadboard/
│   └── pcb/
├── firmware/
│   ├── circuitpython/
│   └── tools/
└── media/
    ├── photos/
    └── scope-captures/

