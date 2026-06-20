"""
audit_data.py — the verified audit data behind the SIGN Trust Audit Lab.

Every score here is taken directly from the thesis audit of nine cosmetic-surgery
clinic interfaces across South Korea, Türkiye and Colombia (six trust metrics,
expert-rated 1-5). Nothing is invented. The Lab computes a transparent composite
trust index from these raw scores and lets you ablate a modality to see how much
of the trust it was carrying.
"""

# Six audit metrics, in the order the score arrays use.
# (key, label, modality, SIGN pillar it primarily evidences [per thesis])
METRICS = [
    ("va", "Visual Aesthetics",          "visual",   "Sensitisation"),
    ("er", "Emotional Resonance",        "cultural", "Sensitisation"),
    ("cr", "Cultural Relevance",         "cultural", "Navigation"),
    ("cs", "Clarity of Services",        "textual",  "Guidance"),
    ("iq", "Imagery Quality & Strategy", "visual",   "Involvement"),
    ("pc", "Professional Credentials",   "textual",  "Guidance"),
]

# Modalities — colour is a data encoding, not decoration.
MODALITIES = {
    "visual":   ("Visual",            "#1C7A85", "layout, imagery, branding"),
    "textual":  ("Textual",           "#A9742B", "clarity, credentials, wording"),
    "cultural": ("Social & cultural",  "#7A5BA0", "emotional & cultural resonance"),
}

# SIGN pillar sub-principles (from the thesis 'pinwheel' model) — the named
# criteria each pillar was assessed against. Shown so the scoring reads as
# earned, not invented.
SIGN_PRINCIPLES = {
    "Sensitisation": ["cultural legibility", "relational sensitivity",
                      "emotionally resonant visuals", "empathic language",
                      "personalisation across touchpoints"],
    "Involvement":   ["participatory inclusion", "co-design & feedback loops",
                      "empowered decision-making", "scenario-driven message framing"],
    "Guidance":      ["clear information hierarchy & flow", "readable plain language",
                      "procedural transparency", "visual anchors for orientation",
                      "risk-explanation clarity"],
    "Navigation":    ["adaptive communication", "pre-arrival reassurance",
                      "journey-flow logic", "multilingual support"],
}

# Subjects: country averages + individual clinics. Scores follow METRICS order:
# [Visual Aesthetics, Emotional Resonance, Cultural Relevance,
#  Clarity of Services, Imagery Quality & Strategy, Professional Credentials]
SUBJECTS = [
    {"key": "kr_avg", "label": "South Korea — country average", "flag": "🇰🇷",
     "kind": "avg",    "scores": [4.07, 4.0, 3.6, 4.0, 4.0, 4.6]},
    {"key": "kr_line", "label": "The Line Plastic Surgery", "flag": "🇰🇷",
     "kind": "clinic", "scores": [4.0, 4.0, 3.2, 4.0, 4.0, 4.6]},
    {"key": "kr_jk", "label": "JK Plastic Surgery Center", "flag": "🇰🇷",
     "kind": "clinic", "scores": [4.2, 4.0, 3.8, 4.0, 4.0, 4.6]},
    {"key": "kr_id", "label": "ID Hospital", "flag": "🇰🇷",
     "kind": "clinic", "scores": [4.0, 4.0, 3.8, 4.0, 4.0, 4.6]},

    {"key": "tr_avg", "label": "Türkiye — country average", "flag": "🇹🇷",
     "kind": "avg",    "scores": [4.27, 4.27, 4.27, 4.47, 4.13, 4.6]},
    {"key": "tr_may", "label": "MAYCLINIK", "flag": "🇹🇷",
     "kind": "clinic", "scores": [4.0, 4.4, 4.2, 4.4, 4.0, 5.0]},
    {"key": "tr_care", "label": "Care in Turkey", "flag": "🇹🇷",
     "kind": "clinic", "scores": [4.4, 4.0, 4.4, 4.4, 4.0, 4.8]},
    {"key": "tr_est", "label": "Estetik International", "flag": "🇹🇷",
     "kind": "clinic", "scores": [4.4, 4.4, 4.2, 4.6, 4.4, 4.0]},

    {"key": "co_avg", "label": "Colombia — country average", "flag": "🇨🇴",
     "kind": "avg",    "scores": [4.4, 4.47, 4.27, 4.47, 4.47, 4.33]},
    {"key": "co_zam", "label": "Zamir Paez Plastic Surgeon", "flag": "🇨🇴",
     "kind": "clinic", "scores": [4.4, 4.2, 4.0, 4.4, 4.4, 4.0]},
    {"key": "co_prem", "label": "Premium Care Plastic Surgery", "flag": "🇨🇴",
     "kind": "clinic", "scores": [4.8, 5.0, 4.6, 4.6, 5.0, 4.8]},
    {"key": "co_juan", "label": "Juan Pablo Plastic Surgeon", "flag": "🇨🇴",
     "kind": "clinic", "scores": [4.0, 4.2, 4.2, 4.4, 4.0, 4.2]},
]

MAX_TOTAL = len(METRICS) * 5.0  # 30 — used to scale the composite to 0-100


def metric_indices(modality):
    return [i for i, m in enumerate(METRICS) if m[2] == modality]


def composite(scores, active):
    """Trust index 0-100. Each active metric contributes its raw score; a muted
    modality contributes nothing — so removing a strong channel costs more."""
    total = sum(scores[i] for i, m in enumerate(METRICS) if m[2] in active)
    return round(total / MAX_TOTAL * 100)


def modality_cost(scores, modality):
    """Points the composite loses if this modality is removed (= its contribution)."""
    full = composite(scores, set(MODALITIES))
    without = composite(scores, set(MODALITIES) - {modality})
    return full - without


def reading(subject, active):
    """Plain-language interpretation of the current ablation state."""
    scores = subject["scores"]
    offs = [m for m in MODALITIES if m not in active]
    full = composite(scores, set(MODALITIES))
    cur = composite(scores, active)
    if not offs:
        return ("All three signal channels active. Switch one off to test where this "
                "interface's trust is actually load-bearing.")
    if len(offs) == len(MODALITIES):
        return "Every channel muted — nothing remains to signal trust."
    if len(offs) == 1:
        mod = offs[0]
        label = MODALITIES[mod][0]
        cost = modality_cost(scores, mod)
        costs = {m: modality_cost(scores, m) for m in MODALITIES}
        ranks = sorted(costs, key=costs.get)
        # weakest underlying metric in this modality
        idx = metric_indices(mod)
        weak_i = min(idx, key=lambda i: scores[i])
        weak_name, weak_val = METRICS[weak_i][1], scores[weak_i]
        s = f"Muting the **{label.lower()}** channel costs **{cost} points**"
        if mod == ranks[-1]:
            s += " — the most load-bearing signal here."
        elif mod == ranks[0]:
            s += " — the least load-bearing signal here."
        else:
            s += "."
        if weak_val < 3.8:
            s += (f" It also holds this interface's weakest signal "
                  f"(*{weak_name}*, {weak_val}); trust here leans on its other channels rather "
                  f"than on cultural resonance — the misalignment the study highlights.")
        return s
    names = " and ".join(MODALITIES[m][0].lower() for m in offs)
    return (f"With the {names} channels muted, trust falls to **{cur}** "
            f"(−{full - cur}). What remains is what the surviving channel can carry alone.")
