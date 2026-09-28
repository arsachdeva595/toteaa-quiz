# Toteaa — "What should I wear?" quiz

An outfit quiz for Indian girls that suggests a Toteaa tote to go with every look. It's session-only: no accounts and no stored personal data.

## Phases

1. **Quiz:** occasion → who's there → desi/western → vibe → weather → limits → budget. Returns 3 outfits and a tote pairing.
2. **Upload mode:** a selfie in an outfit, a reference image, or a wardrobe photo. The app builds an outfit and suggests a tote or accessory. Images are processed in the browser or with a zero-retention API.
3. **Mix & match studio:** combine trending pieces, save a PNG locally, and share to socials.

## Repo layout

| Path | What |
|---|---|
| `research/01-outfit-data-enrichment-india.md` | Research: Indian-context questions, data sources and licensing, enrichment pipeline, privacy model |
| `data/taxonomy.json` | Controlled vocabulary: occasions, vibes, garments, fabrics, colours, dress-code colour rules, trend tags |
| `data/quiz-v1.json` | Phase 1 question flow and scoring weights |
| `data/schema/outfit.schema.json` | JSON Schema for an outfit record |
| `data/outfits.sample.json` | 10 hand-curated sample outfits in the schema |
