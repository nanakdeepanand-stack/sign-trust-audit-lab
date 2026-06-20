# SIGN Trust Audit Lab

An interactive instrument accompanying the ICMI 2026 Late-Breaking Results paper
*"Multimodal Trust Signalling in Pre-Visit Healthcare Interfaces."*

It reads a clinic (or country) interface as trust signals across three modalities
— **visual, textual, social-cultural** — using the study's **real audit scores**
(nine cosmetic-surgery clinics across South Korea, Türkiye and Colombia, six
metrics, expert-rated 1–5). Switch a modality **off** (ablation) and watch the
composite trust index change: this demonstrates the paper's central claim —
*trust depends on the alignment of modalities and breaks on misalignment* — by
interaction rather than assertion.

No API key, no external calls — every number is from the audit, so it runs
anywhere.

## Run it locally
From the folder containing these files:

```bash
python3 -m streamlit run streamlit_app.py
```

It opens at `http://localhost:8501`. Pick an interface in the sidebar, then mute
a channel and read the interpretation.

## What's inside
- `streamlit_app.py` - the Lab UI.
- `audit_data.py` - the verified audit scores, modality grouping, SIGN
  sub-principles, and the scoring/ablation functions.
- `requirements.txt` - one dependency (Streamlit).

## How it's grounded
- Six metrics (Visual Aesthetics, Emotional Resonance, Cultural Relevance,
  Clarity of Services, Imagery Quality & Strategy, Professional Credentials),
  grouped by the modality they primarily express.
- Composite trust index = sum of active metric scores ÷ 30 × 100. A muted
  modality contributes nothing, so removing a **strong** channel costs more — and
  removing a **weak** one (e.g. Korea's cultural channel) reveals where trust was
  never built.
- SIGN pillar sub-principles (from the thesis pinwheel model) are listed in the
  app's "How these scores are grounded" panel.

## Deploy to the web (optional, for the paper's code link)
Push this folder to a GitHub repo, then connect it at
[share.streamlit.io](https://share.streamlit.io) → it builds a public URL you can
paste into the paper. For double-blind review, host in an **anonymous** repo.

*Research prototype - pre-visit trust analysis, not medical or clinical advice.*
