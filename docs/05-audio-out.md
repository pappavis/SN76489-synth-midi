# Stap 5 – Audio-versterkeropties (evaluatie)

Deze stap vergelijkt en borgt mogelijke audio-eindtrappen voor de
SN76489 USB-MIDI synth.

Ontwerpregel (afdwingend):
- Eerst breadboard valideren
- Daarna pas PCB
- Alles meetbaar met scope en multimeter
- Koptelefoon is primaire load

---

## Optie A — LM386 (baseline / educatief)
*(Nog uit te werken)*

Gebruik:
- Snelle proof-of-concept
- Leren waarom dit vaak ruisgevoelig is

---

## Optie B — Opamp-based headphone driver (AANBEVOLEN)

Mono → gebufferd → dual-mono L/R  
Single-supply 5 V met virtuele ground (Vref)

### Status
✅ Technisch verankerd  
✅ Breadboard-geschikt  
✅ Lage ruis, voorspelbaar gedrag  

---

### 1. Conceptueel schema (tekstueel)

SN76489 audio out  
→ AC-koppeling  
→ bias naar Vref (virtuele ground)  
→ opamp gain stage (niet-inverterend)  
→ serieweerstanden  
→ DC-blokkering  
→ dual-mono L/R  
→ 3.5 mm TRS koptelefoon

Audio werkt rond Vref (~2.5 V), niet rond echte ground.

---

### 2. Aanbevolen opamp (THT)

**LM358 (DIP-8)**  
- Werkt op 5 V single-supply  
- Overal verkrijgbaar  
- Acceptabele prestaties voor V1

Opmerking:
- Niet audiofiel
- Kan bij lage impedanties vervormen
- Goed genoeg om het concept te bewijzen

---

### 3. Virtuele ground (Vref)

#### Basis
- R1 = 10 kΩ → +5 V  
- R2 = 10 kΩ → GND  
- Vref ≈ 2.5 V  
- Cref = 47–100 µF naar GND  

#### Aanbevolen
- Buffer Vref met tweede opamp (volger)
- Voorkomt instorten van referentie bij belasting

Zonder stabiele Vref:
→ brom  
→ asymmetrische clipping  
→ onvoorspelbaar gedrag

---

### 4. Ingangskoppeling & bias

- C_in = 1 µF (film of elco)
- R_bias = 100 kΩ van opamp + ingang naar Vref

High-pass:
- f_c ≈ 1.6 Hz  
- Geen hoorbaar laagverlies

---

### 5. Gain-instelling

Niet-inverterend:

Gain = 1 + (Rf / Rg)

Startwaarden:
- Rg = 10 kΩ  
- Rf = 100 kΩ  
- Gain ≈ 11×

Aanpasbaar:
- Te luid / clipping → Rf verlagen (bijv. 47 kΩ)

---

### 6. Uitgang naar koptelefoon (dual-mono)

Per kanaal:
- R_out = 47 Ω (serie)
- C_out = 220–470 µF (DC-blokkering)
- R_bleed = 100 kΩ naar GND

Waarom:
- Bescherming opamp
- Minder ploppen
- Stabiliteit bij pluggen

---

### 7. Verwacht outputniveau

Indicatief:
- SN76489: ~200 mVpp
- Na versterking: ~2.2 Vpp (intern)
- Op koptelefoon: ~1 Vpp AC

Voldoende luid voor 16–64 Ω koptelefoons  
Volume wordt geregeld **vóór** de versterker (potmeter).

---

### 8. Ruis & kwaliteit

**Voordelen**
- Veel stiller dan LM386
- Gain exact instelbaar
- Geen “motorboating”

**Risico’s**
- LM358 beperkte output-drive
- Slechte Vref → hoorbare ellende
- Breadboard-parasieten → oscillatie

---

### 9. Breadboard-risico’s

- Lange draden op opamp-inputs
- Geen lokale 100 nF ontkoppeling
- Vergeten Cref of C_out
- Geen R_out → HF-oscillatie

---

### 10. PCB-layout aandachtspunten

- Vref als apart analoog eiland
- Ster-ground (audio ≠ MCU retour)
- Decoupling direct bij opamp
- Geen digitale sporen onder audio-inputs

---

### 11. Waarom deze optie kan falen

- Onvoldoende output-drive bij lage impedantie
- Virtuele ground instort
- Te hoge gain → clipping
- Oscillatie door layout of breadboard

---

### 12. Meetplan (verplicht)

**Multimeter**
- +5 V rail: 4.9–5.1 V
- Vref: ~2.5 V stabiel
- Opamp output idle: ~2.5 V

**Oscilloscoop**
- SN76489 audio: klein AC-signaal
- Opamp output: groter signaal rond Vref
- Jack-tip na C_out: AC rond 0 V
- Controle op HF-oscillatie

**Luistertest**
- Volume dicht: bijna stil
- Volume open: helder, geen brom of piep

---

### 13. Start-BOM (THT-only)

- LM358 (DIP-8)
- Weerstanden:
  - 10 kΩ ×2 (Vref)
  - 10 kΩ (Rg)
  - 100 kΩ ×2 (Rf, R_bias)
  - 47 Ω ×2 (R_out)
  - 100 kΩ ×2 (R_bleed)
- Condensatoren:
  - 100 nF ×1 (ontkoppeling)
  - 47–100 µF ×1 (Cref)
  - 1 µF ×1 (C_in)
  - 220–470 µF ×2 (C_out)
- Potmeter: 10–50 kΩ log (mono)
- 3.5 mm TRS jack (THT)

---

## Optie C — Dedicated headphone amp IC
*(Nog uit te werken)*

---