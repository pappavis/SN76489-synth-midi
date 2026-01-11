# Audio_Amplifier_Opamp.sch — (Optie B) opamp + VREF

> In V1 doen we **mono** versterking en daarna split naar dual-mono.

### Voeding & referentie
+5V_AUD ────────────────┐
│
R3 10k
│
├─────> VREF_AUD (≈2.5V) ──|| C3 47u ──> GND_AUD
│
R4 10k
│
GND_AUD ─────────────────┘

### Signaal (block-level)
**Netten die hier “vast” moeten zijn:**
- `+5V_AUD`, `GND_AUD`, `VREF_AUD`
- `AUDIO_POST_POT` (in)
- `AUDIO_AMP_OUT` (uit)

