## Optie A — LM386 (baseline / budget / educatief)

Mono → power-amp → dual-mono L/R  
Doel: snel geluid uit een speaker-amp IC, maar met duidelijke nadelen voor koptelefoon.

### Status
✅ Snelste proof-of-concept  
⚠️ Ruisgevoelig / layout-kritisch  
⚠️ Niet ideaal als headphone driver (maar kan “werken” met beperkingen)

---

### 1. Conceptueel schema (tekstueel)

SN76489 audio out  
→ AC-koppeling (C_in)  
→ volumepotmeter (mono)  
→ LM386 input (pin 3)  
→ LM386 output (pin 5)  
→ uitgangsnetwerk (Zobel + decoupling)  
→ DC-blokkering naar koptelefoon L/R (dual-mono)  
→ 3.5 mm TRS jack

Belangrijk:
- LM386 is een **power amp** voor luidsprekers (typisch 8 Ω).
- Koptelefoon (16–64 Ω) is “mogelijk”, maar het gedrag is minder netjes.

---

### 2. Voeding & basisrandvoorwaarden

- VCC: **5 V** (kan ook hoger, maar jouw systeem is 5 V-gedreven)
- Decoupling direct bij IC:
  - 100 nF keramisch
  - 220–470 µF elco op de 5 V rail dichtbij de LM386

Eis:
- LM386 krijgt een eigen “power-eiland” op breadboard.
- Geen voeding via lange spaghetti-jumpers zonder bufferelco.

---

### 3. Gain (verwachte versterking)

LM386 gain:
- Default: **20×** (26 dB) zonder onderdelen tussen pin 1 en 8
- Met C_gain tussen pin 1 en 8: **tot 200×** (46 dB)

Aanbevolen voor deze toepassing:
- **Laat gain op 20×** (dus géén C_gain).
- Waarom: SN76489 is al ruisgevoelig, LM386 versterkt rommel graag mee.

Als het niveau te laag is:
- Eerst potmeter / inputniveau / filtering optimaliseren
- Pas als laatste overweeg je C_gain (en dan krijg je meestal ruis + instabiliteit erbij)

---

### 4. Ingangskoppeling & volumeregeling

- C_in: **100 nF – 1 µF** in serie naar LM386 input
- Potmeter: **10 kΩ log** (mono) als volumeregelaar vóór LM386
- Input bias/stabiliteit:
  - R_in = 10 kΩ–100 kΩ van input naar GND (optioneel, tegen zweven)

Praktisch startpunt:
- C_in = 100 nF of 220 nF
- Pot = 10 kΩ log

---

### 5. Uitgang naar koptelefoon (dual-mono)

LM386 output is biased (intern) en kan DC bevatten → **DC blokkeren**.

Per kanaal:
- C_outL = 220–470 µF in serie naar L
- C_outR = 220–470 µF in serie naar R

Aanbevolen extra bescherming:
- R_outL = 33–100 Ω serie naar L
- R_outR = 33–100 Ω serie naar R

Waarom:
- Beperkt stroom
- Minder kans op “schelle” vervorming
- Minder kans op instabiliteit bij vreemde loads/kabels

Bleeders:
- R_bleedL = 100 kΩ van L naar GND
- R_bleedR = 100 kΩ van R naar GND

---

### 6. Standaard stabiliteitsnetwerken (verplicht bij LM386)

**Bypass (ruisreductie)**
- Pin 7 → C_bypass = **10 µF** naar GND  
Dit kan ruis/hum merkbaar verminderen.

**Zobel netwerk (tegen oscillatie, output stabiliteit)**
- Vanaf output (pin 5) naar GND:
  - R_zobel = **10 Ω**
  - C_zobel = **47 nF**
  (in serie)

**Output snubber / extra**
- Soms helpt een kleine L (spoeltje) of serieweerstand; op breadboard liever R_out gebruiken.

---

### 7. Verwacht outputniveau

Bij 5 V:
- LM386 kan voldoende niveau leveren om koptelefoon luid te maken,
  maar headroom is beperkt en vervorming kan snel oplopen.

Praktische verwachting:
- Genoeg volume, maar eerder:
  - ruisvloer hoorbaar
  - “korrelig” bij hoge gain
  - sneller clippen

---

### 8. Ruis & brongevoeligheid

**Voordelen**
- Simpel
- Werkt snel
- Veel voorbeeldschakelingen

**Nadelen**
- Versterkt ruis en voeding-rommel makkelijk mee
- Gevoelig voor layout en ontkoppeling
- Kan “motorboaten” (laagfrequente oscillatie) bij slechte voeding/decoupling
- Niet ontworpen voor nette koptelefoonkwaliteit

---

### 9. Breadboard-risico’s

Waar het misgaat (klassiek LM386):
- Voedingsdraden te lang → oscillatie / motorboating
- Ontkoppeling te ver weg → brom/ruis
- Geen Zobel → HF-oscillatie
- Te hoge gain (C_gain geplaatst) → ruis + instabiliteit
- Audio-ground en digitale ground door elkaar → digitale piepjes

Kort: LM386 op breadboard is vaak “een les in grounding”.

---

### 10. PCB-layout aandachtspunten

- **Heel korte** decoupling-loop VCC ↔ GND bij IC
- Output trace weg van input trace (geen feedback via koppeling)
- Ster-ground: audio retour niet door MCU groundsporen
- Zobel dicht bij output-pin en ground return
- Pin 7 bypass cap dichtbij pin 7

LM386 is berucht: layout bepaalt of het stil is of een zender.

---

### 11. Waarom deze optie kan falen (eerlijk)

- **Oscillatie** (HF) → hiss / warmte / rare vervorming
- **Motorboating** → “woef-woef” op lage frequentie
- **Brom** door ground loops
- **Clippen** door beperkte headroom op 5 V
- **Koptelefoon mismatch**: te hard, te ruw, te veel ruis

---

### 12. Meetplan (verplicht)

**Multimeter**
- +5 V rail: 4.9–5.1 V
- Controleer dat pin 6 stabiel 5 V ziet (geen dips bij audio)

**Oscilloscoop**
1. Meet output op pin 5 zonder load:
   - Kijk of er HF-oscillatie “haar” zichtbaar is
2. Meet met koptelefoon aangesloten:
   - Kijk of de golf instort / asymmetrisch wordt
3. Meet voeding bij LM386:
   - Kijk naar dips en rimpel tijdens audio (motorboating herken je zo)

**Luistertest**
- Volume dicht → ruisvloer checken
- Volume open → check op brom, piep, “woef”-oscillatie

---

### 13. Start-BOM (THT-only)

- LM386 (DIP-8)
- Weerstanden:
  - 10 Ω (Zobel)
  - 33–100 Ω ×2 (R_out L/R)
  - 100 kΩ ×2 (R_bleed L/R)
  - (optioneel) 10–100 kΩ (R_in naar GND)
- Condensatoren:
  - 100 nF (VCC decouple)
  - 220–470 µF (VCC bulk dichtbij IC)
  - 10 µF (pin 7 bypass)
  - 47 nF (Zobel)
  - 100 nF–1 µF (C_in)
  - 220–470 µF ×2 (C_out L/R)
- Potmeter: 10 kΩ log (mono)
- 3.5 mm TRS jack (THT)

---

### 14. Wanneer kiezen (beslisregel)

Kies Optie A als:
- Je vandaag nog geluid wil en bereid bent ruis/layout-issues te debuggen
- Je educatief wil ervaren waarom LM386 “tricky” is

Kies Optie B als:
- Je een stabiele eindoplossing wil die echt koptelefoonvriendelijk is
- Je controle wil over gain en ruis


---

## Optie A vs Optie B — Vergelijkingsmatrix

| Aspect | Optie A — LM386 | Optie B — Opamp-based |
|------|------------------|-----------------------|
| Primair doel | Speaker amp hergebruikt voor audio | Headphone-geschikte line/driver |
| Complexiteit | Laag (op papier) | Middel |
| Aantal onderdelen | Laag | Middel |
| Voeding | 5 V single-supply | 5 V single-supply |
| Gain-controle | Beperkt (20× / 200×) | Volledig instelbaar |
| Ruisvloer | Hoog / wisselend | Laag / voorspelbaar |
| Bromgevoeligheid | Hoog | Laag |
| Oscillatie-risico | Hoog (layout-kritisch) | Laag–middel |
| Breadboard-geschiktheid | ⚠️ Fragiel | ✅ Goed |
| Koptelefoon-geschikt | ⚠️ Matig | ✅ Ja |
| Output-impedantie | Laag maar ongecontroleerd | Gecontroleerd (R_out) |
| DC-beveiliging | Vereist extra aandacht | Ingebouwd via C_out |
| Debugbaarheid | Lastig (veel bijeffecten) | Goed (meetbaar per blok) |
| Educatieve waarde | “Waarom dit fout kan gaan” | “Zo bouw je het netjes” |
| Kans op succes V1 | ⚠️ 50/50 | ✅ Hoog |
| Geschikt als eindoplossing | ❌ Nee | ✅ Ja |

---

### Samenvattende beslisregel

- **Optie A (LM386)**  
  Gebruik als:
  - snelle proof-of-concept  
  - educatief experiment  
  - je expliciet wilt leren *waarom* dit IC vaak problemen geeft  

- **Optie B (Opamp-based)**  
  Gebruik als:
  - stabiele breadboard-validatie  
  - koptelefoon primaire output is  
  - je richting een nette PCB-oplossing werkt  

**Ontwerpkeuze V6 (aanbevolen):**  
➡️ *Optie B is het hoofdpad.*  
➡️ *Optie A blijft referentie / vergelijking.*

---
