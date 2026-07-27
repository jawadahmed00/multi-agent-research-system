import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(page_title="Multi-Agent Research System", page_icon="🔎", layout="wide")

# ---------------------------------------------------------------------------
# Futuristic theme
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Space+Grotesk:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.stApp {
    background: radial-gradient(circle at 20% 20%, #0d1b2a 0%, #050914 45%, #020308 100%);
    color: #e6f1ff;
}

/* Hero header */
.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: 3rem;
    text-align: center;
    background: linear-gradient(90deg, #00f5d4, #00bbf9, #9b5de5, #f15bb5);
    background-size: 300% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: shine 6s linear infinite;
    margin-bottom: 0;
}
@keyframes shine {
    to { background-position: 300% center; }
}
.hero-sub {
    text-align: center;
    color: #8ab6d6;
    font-size: 1.05rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 0.2rem;
    margin-bottom: 2rem;
}

/* Glass card container for the form */
div[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(0, 245, 212, 0.25);
    border-radius: 18px;
    padding: 1.8rem 2rem;
    box-shadow: 0 0 30px rgba(0, 245, 212, 0.08), inset 0 0 20px rgba(0, 187, 249, 0.03);
    backdrop-filter: blur(10px);
}

.stTextInput input {
    background: rgba(255,255,255,0.05) !important;
    color: #e6f1ff !important;
    border: 1px solid rgba(0, 245, 212, 0.3) !important;
    border-radius: 10px !important;
}

/* Buttons */
.stButton button, .stFormSubmitButton button, .stDownloadButton button {
    background: linear-gradient(90deg, #00f5d4, #00bbf9) !important;
    color: #020308 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    letter-spacing: 0.03em;
    box-shadow: 0 0 20px rgba(0, 245, 212, 0.35);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton button:hover, .stFormSubmitButton button:hover, .stDownloadButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 0 30px rgba(0, 245, 212, 0.6);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.03);
    border-radius: 10px 10px 0 0;
    padding: 10px 18px;
    color: #8ab6d6;
    font-weight: 600;
}
.stTabs [aria-selected="true"] {
    background: rgba(0, 245, 212, 0.12) !important;
    color: #00f5d4 !important;
    border-bottom: 2px solid #00f5d4 !important;
}

/* Content panels */
.result-panel {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(0, 187, 249, 0.2);
    border-radius: 14px;
    padding: 1.5rem;
    margin-top: 0.5rem;
    line-height: 1.6;
}

/* Status / spinner box */
div[data-testid="stStatusWidget"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(155, 93, 229, 0.35);
    border-radius: 14px;
}

hr, [data-testid="stDivider"] {
    border-color: rgba(0, 245, 212, 0.2) !important;
}

/* Section subheader glow */
h3 { color: #00f5d4 !important; text-shadow: 0 0 12px rgba(0, 245, 212, 0.35); }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown('<div class="hero-title">MULTI-AGENT RESEARCH SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Search &nbsp;→&nbsp; Read &nbsp;→&nbsp; Write &nbsp;→&nbsp; Critique</div>', unsafe_allow_html=True)

if "state" not in st.session_state:
    st.session_state.state = None

# ---------------------------------------------------------------------------
# Input form
# ---------------------------------------------------------------------------
with st.form("research_form"):
    topic = st.text_input("RESEARCH TOPIC", placeholder="e.g. Impact of LLM agents on scientific research")
    submitted = st.form_submit_button("🚀 Launch Research", use_container_width=True)

if submitted:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        status = st.status("Initializing agent pipeline...", expanded=True)
        try:
            status.write("🛰️ Step 1 — Search agent gathering intelligence...")
            status.write("📡 Step 2 — Reader agent extracting deep content...")
            status.write("✍️ Step 3 — Writer agent drafting the report...")
            status.write("🧠 Step 4 — Critic agent reviewing the output...")

            state = run_research_pipeline(topic)
            st.session_state.state = state
            st.session_state.topic = topic

            status.update(label="✅ Pipeline complete", state="complete", expanded=False)
        except Exception as e:
            status.update(label="❌ Pipeline failed", state="error", expanded=True)
            st.error(f"Something went wrong: {e}")

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
state = st.session_state.state

if state:
    st.divider()
    st.subheader(f"📊 Results — {st.session_state.topic}")

    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["📄 Report", "🧐 Critic Feedback", "🔍 Search Results", "📚 Scraped Content"]
    )

    with tab_report:
        st.markdown(f'<div class="result-panel">{state.get("report", "No report generated.")}</div>', unsafe_allow_html=True)

    with tab_feedback:
        st.markdown(f'<div class="result-panel">{state.get("feedback", "No feedback generated.")}</div>', unsafe_allow_html=True)

    with tab_search:
        st.markdown(f'<div class="result-panel"><pre style="white-space:pre-wrap;">{state.get("search_results", "No search results.")}</pre></div>', unsafe_allow_html=True)

    with tab_scraped:
        st.markdown(f'<div class="result-panel"><pre style="white-space:pre-wrap;">{state.get("scraped_content", "No scraped content.")}</pre></div>', unsafe_allow_html=True)

    st.download_button(
        "⬇️ Download Report (.md)",
        data=state.get("report", ""),
        file_name=f"{st.session_state.topic.strip().replace(' ', '_')}_report.md",
        mime="text/markdown",
        use_container_width=True,
    )