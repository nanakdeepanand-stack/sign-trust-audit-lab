"""
streamlit_app.py - SIGN Trust Audit Lab

An interactive instrument accompanying the ICMI 2026 LBR paper. It reads a
clinic (or country) interface as a set of trust signals across three modalities
- visual, textual, social-cultural - using the study's real audit scores, and
lets you ABLATE a modality to see how much of the trust it was carrying. This
demonstrates the paper's central claim - trust depends on the alignment of
modalities, and breaks on misalignment - by interaction rather than assertion.

No API key required: every number is from the audit; the app is pure computation.
"""
import streamlit as st
import audit_data as A

st.set_page_config(page_title="SIGN Trust Audit Lab", page_icon="🔬", layout="wide")

# ------------------------------------------------------------------ styling
st.markdown("""
<style>
.block-container {padding-top: 2.2rem; max-width: 1050px;}
.metric-bar {height: 10px; border-radius: 5px; background: #eef2f1; overflow: hidden; margin: 3px 0 2px;}
.metric-fill {height: 100%; border-radius: 5px;}
.muted {opacity: .35;}
.pill {display:inline-block; padding:1px 8px; border-radius:6px; font-size:.7rem;
       color:#fff; font-weight:600;}
.small {font-size:.78rem; color:#5e6f72;}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------ sidebar
with st.sidebar:
    st.markdown("### 🔬 SIGN Trust Audit Lab")
    st.caption("Multimodal trust signalling - pre-visit interfaces")

    labels = {s["key"]: f"{s['flag']}  {s['label']}" for s in A.SUBJECTS}
    subj_key = st.selectbox("Interface to audit", [s["key"] for s in A.SUBJECTS],
                            format_func=lambda k: labels[k])
    subject = next(s for s in A.SUBJECTS if s["key"] == subj_key)

    st.markdown("---")
    st.markdown("**Ablation - mute a signal channel**")
    st.caption("Turn a modality off to see how many trust points depended on it.")
    active = set()
    for mod, (label, color, _) in A.MODALITIES.items():
        on = st.toggle(label, value=True, key=f"tog_{mod}")
        if on:
            active.add(mod)
        st.caption(f"removing this costs −{A.modality_cost(subject['scores'], mod)} pts")

    st.markdown("---")
    st.caption("Scores: expert audit (PURE method, 1–5) of nine clinics. "
               "Composite = sum of active metric scores ÷ 30 × 100.")

# ------------------------------------------------------------------ header + index
st.markdown("## SIGN Trust Audit Lab")
st.caption(f"Auditing **{subject['label']}** - trust signalled across three modalities.")

full = A.composite(subject["scores"], set(A.MODALITIES))
cur = A.composite(subject["scores"], active)
delta = cur - full

c1, c2 = st.columns([1, 2.4])
with c1:
    st.metric("Trust index", f"{cur}/100",
              delta=(None if delta == 0 else f"{delta} from ablation"),
              delta_color="inverse")
with c2:
    st.markdown(f"<div style='padding-top:.4rem'>{A.reading(subject, active)}</div>",
                unsafe_allow_html=True)

st.markdown("")

# ------------------------------------------------------------------ modality columns
cols = st.columns(3)
for col, (mod, (label, color, blurb)) in zip(cols, A.MODALITIES.items()):
    on = mod in active
    with col:
        head = f"<span class='pill' style='background:{color}'>{label}</span>"
        if not on:
            head += " <span class='small'>· muted</span>"
        st.markdown(head, unsafe_allow_html=True)
        st.markdown(f"<div class='small'>{blurb}</div>", unsafe_allow_html=True)
        for i, m in enumerate(A.METRICS):
            if m[2] != mod:
                continue
            score = subject["scores"][i]
            pct = score / 5 * 100
            cls = "metric-fill" + ("" if on else " muted")
            st.markdown(
                f"<div style='margin-top:8px'><div class='small'>{m[1]} "
                f"<b>{score}</b> <span style='color:#9aa'>· {m[3]}</span></div>"
                f"<div class='metric-bar'><div class='{cls}' "
                f"style='width:{pct}%; background:{color}'></div></div></div>",
                unsafe_allow_html=True,
            )

# ------------------------------------------------------------------ grounding
st.markdown("")
with st.expander("How these scores are grounded (SIGN pillars & method)"):
    st.markdown(
        "Each interface was scored 1–5 on six trust metrics across five sections "
        "(homepage, about/team, international support, services, testimonials). "
        "Metrics are grouped here by the **modality** they primarily express; each also "
        "evidences a **SIGN pillar**, assessed against these named sub-principles:"
    )
    pcols = st.columns(2)
    for i, (pillar, principles) in enumerate(A.SIGN_PRINCIPLES.items()):
        with pcols[i % 2]:
            st.markdown(f"**{pillar}**")
            st.markdown("\n".join(f"- {p}" for p in principles))
    st.caption("Heatmap colour bands in the thesis are normalised per clinic; this Lab "
               "uses the raw 1–5 scores, which are directly comparable across interfaces.")

st.caption("Pre-visit trust analysis · research prototype, not medical or clinical advice.")
