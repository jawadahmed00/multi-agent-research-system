import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(page_title="Multi-Agent Research System", page_icon="🔎", layout="wide")

# ---------------------------------------------------------------------------
# Futuristic theme — exaggerated cyberpunk / HUD style
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Space+Grotesk:wght@400;500;600;700&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.stApp {
    background:
        linear-gradient(rgba(0,245,212,0.05) 1px, transparent 1px) 0 0 / 40px 40px,
        linear-gradient(90deg, rgba(0,245,212,0.05) 1px, transparent 1px) 0 0 / 40px 40px,
        radial-gradient(circle at 15% 10%, rgba(0,245,212,0.12) 0%, transparent 40%),
        radial-gradient(circle at 85% 15%, rgba(155,93,229,0.14) 0%, transparent 40%),
        radial-gradient(circle at 50% 90%, rgba(241,91,181,0.10) 0%, transparent 45%),
        #020308;
    color: #e6f1ff;
}

.scan-bar {
    height: 3px;
    width: 100%;
    background: linear-gradient(90deg, transparent, #00f5d4, #00bbf9, #9b5de5, #f15bb5, transparent);
    background-size: 200% auto;
    animation: scan 4s linear infinite;
    margin-bottom: 1.2rem;
    border-radius: 3px;
}
@keyframes scan { to { background-position: 200% center; } }

.hero-wrap { text-align: center; margin-bottom: 1.5rem; }
.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: 3.4rem;
    letter-spacing: 0.03em;
    background: linear-gradient(90deg, #00f5d4, #00bbf9, #9b5de5, #f15bb5, #00f5d4);
    background-size: 300% auto;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: shine 6s linear infinite;
    text-shadow: 0 0 60px rgba(0,245,212,0.25);
}
@keyframes shine { to { background-position: 300% center; } }
.hero-sub {
    color: #8ab6d6;
    font-size: 1.05rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.3rem;
    font-family: 'Share Tech Mono', monospace;
}

.tag-row { display: flex; justify-content: center; gap: 0.6rem; flex-wrap: wrap; margin: 1.2rem 0 1.8rem 0; }
.tag-pill {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.08em;
    padding: 6px 16px;
    border-radius: 999px;
    text-transform: uppercase;
    border: 1px solid;
    animation: pulse-glow 3s ease-in-out infinite;
}
.tag-cyan   { color: #00f5d4; border-color: rgba(0,245,212,0.5); background: rgba(0,245,212,0.08); box-shadow: 0 0 12px rgba(0,245,212,0.25); }
.tag-blue   { color: #00bbf9; border-color: rgba(0,187,249,0.5); background: rgba(0,187,249,0.08); box-shadow: 0 0 12px rgba(0,187,249,0.25); }
.tag-purple { color: #9b5de5; border-color: rgba(155,93,229,0.5); background: rgba(155,93,229,0.08); box-shadow: 0 0 12px rgba(155,93,229,0.25); }
.tag-pink   { color: #f15bb5; border-color: rgba(241,91,181,0.5); background: rgba(241,91,181,0.08); box-shadow: 0 0 12px rgba(241,91,181,0.25); }
@keyframes pulse-glow { 0%,100% { filter: brightness(1); } 50% { filter: brightness(1.35); } }

.stat-strip {
    display: flex; justify-content: center; gap: 2.5rem; flex-wrap: wrap;
    margin-bottom: 1.8rem; font-family: 'Share Tech Mono', monospace;
}
.stat-item { text-align: center; }
.stat-value { font-size: 1.4rem; font-weight: 700; color: #00f5d4; text-shadow: 0 0 10px rgba(0,245,212,0.5); }
.stat-label { font-size: 0.7rem; color: #6b8ba8; letter-spacing: 0.1em; text-transform: uppercase; }
.status-dot { display:inline-block; width:8px; height:8px; border-radius:50%; background:#00f5d4; box-shadow:0 0 8px #00f5d4; margin-right:6px; animation: blink 1.4s infinite; }
@keyframes blink { 0%,100% { opacity: 1; } 50% { opacity: 0.3; } }

.pipeline-row { display: flex; justify-content: center; align-items: center; gap: 0.5rem; margin: 1.5rem 0 2rem 0; flex-wrap: wrap; }
.pipe-node {
    font-family: 'Share Tech Mono', monospace;
    text-align: center;
    padding: 14px 18px;
    border-radius: 14px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(0,245,212,0.3);
    min-width: 130px;
    box-shadow: 0 0 18px rgba(0,245,212,0.12);
}
.pipe-node .icon { font-size: 1.6rem; display:block; margin-bottom: 4px; }
.pipe-node .label { font-size: 0.75rem; color: #cfe8ff; text-transform: uppercase; letter-spacing: 0.05em; }
.pipe-arrow { font-size: 1.4rem; color: #00f5d4; text-shadow: 0 0 10px #00f5d4; }

div[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(0, 245, 212, 0.3);
    border-radius: 20px;
    padding: 2rem 2.2rem;
    box-shadow: 0 0 40px rgba(0, 245, 212, 0.1), inset 0 0 25px rgba(0, 187, 249, 0.04);
    backdrop-filter: blur(12px);
}

.stTextInput input {
    background: rgba(255,255,255,0.05) !important;
    color: #e6f1ff !important;
    border: 1px solid rgba(0, 245, 212, 0.35) !important;
    border-radius: 10px !important;
    font-family: 'Share Tech Mono', monospace !important;
}

div[data-testid="column"] .stButton button {
    background: rgba(255,255,255,0.04) !important;
    color: #8ab6d6 !important;
    border: 1px dashed rgba(0,187,249,0.4) !important;
    border-radius: 999px !important;
    font-size: 0.78rem !important;
    padding: 4px 14px !important;
    box-shadow: none !important;
}
div[data-testid="column"] .stButton button:hover {
    color: #00f5d4 !important;
    border-color: #00f5d4 !important;
    transform: none !important;
}

.stFormSubmitButton button, .stDownloadButton button {
    background: linear-gradient(90deg, #00f5d4, #00bbf9, #9b5de5) !important;
    background-size: 200% auto !important;
    color: #020308 !important;
    font-weight: 800 !important;
    font-family: 'Orbitron', sans-serif !important;
    letter-spacing: 0.05em;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 0 25px rgba(0, 245, 212, 0.45);
    transition: all 0.2s ease;
}
.stFormSubmitButton button:hover, .stDownloadButton button:hover {
    background-position: 100% center !important;
    transform: translateY(-3px) scale(1.01);
    box-shadow: 0 0 40px rgba(0, 245, 212, 0.75);
}

.stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: 1px solid rgba(255,255,255,0.08); }
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.03);
    border-radius: 12px 12px 0 0;
    padding: 12px 20px;
    color: #8ab6d6;
    font-weight: 700;
    font-family: 'Orbitron', sans-serif;
    font-size: 0.85rem;
}
.stTabs [aria-selected="true"] {
    background: rgba(0, 245, 212, 0.14) !important;
    color: #00f5d4 !important;
    border-bottom: 3px solid #00f5d4 !important;
    box-shadow: 0 -6px 20px rgba(0,245,212,0.15);
}

.result-panel {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(0, 187, 249, 0.25);
    border-radius: 16px;
    padding: 1.6rem;
    margin-top: 0.6rem;
    line-height: 1.7;
    box-shadow: inset 0 0 30px rgba(0,187,249,0.04);
}

div[data-testid="stStatusWidget"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(155, 93, 229, 0.4);
    border-radius: 16px;
    box-shadow: 0 0 25px rgba(155,93,229,0.15);
}

hr, [data-testid="stDivider"] { border-color: rgba(0, 245, 212, 0.25) !important; }

h3 { color: #00f5d4 !important; text-shadow: 0 0 14px rgba(0, 245, 212, 0.4); font-family: 'Orbitron', sans-serif !important; }

.footer-tag {
    text-align: center;
    margin-top: 2.5rem;
    padding-top: 1rem;
    border-top: 1px dashed rgba(0,245,212,0.2);
    font-family: 'Share Tech Mono', monospace;
    color: #4d6c85;
    font-size: 0.75rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="scan-bar"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="hero-wrap">
    <div class="hero-title">MULTI-AGENT RESEARCH SYSTEM</div>
    <div class="hero-sub">Autonomous Intelligence &nbsp;//&nbsp; Deep Research Pipeline</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="tag-row">
    <span class="tag-pill tag-cyan">⚡ AI-Powered</span>
    <span class="tag-pill tag-blue">🕸️ Multi-Agent</span>
    <span class="tag-pill tag-purple">🧠 LLM Orchestration</span>
    <span class="tag-pill tag-pink">📡 Live Web Data</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stat-strip">
    <div class="stat-item"><div class="stat-value">4</div><div class="stat-label">Active Agents</div></div>
    <div class="stat-item"><div class="stat-value">99.2%</div><div class="stat-label">Uptime</div></div>
    <div class="stat-item"><div class="stat-value"><span class="status-dot"></span>Online</div><div class="stat-label">System Status</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="pipeline-row">
    <div class="pipe-node"><span class="icon">🛰️</span><span class="label">Search</span></div>
    <span class="pipe-arrow">➜</span>
    <div class="pipe-node"><span class="icon">📡</span><span class="label">Read</span></div>
    <span class="pipe-arrow">➜</span>
    <div class="pipe-node"><span class="icon">✍️</span><span class="label">Write</span></div>
    <span class="pipe-arrow">➜</span>
    <div class="pipe-node"><span class="icon">🧠</span><span class="label">Critique</span></div>
</div>
""", unsafe_allow_html=True)

if "state" not in st.session_state:
    st.session_state.state = None

with st.form("research_form"):
    topic = st.text_input("🎯 RESEARCH TOPIC", placeholder="e.g. Impact of LLM agents on scientific research")

    st.markdown('<div style="font-size:0.75rem;color:#6b8ba8;letter-spacing:0.08em;margin:6px 0;">QUICK SUGGESTIONS (VISUAL ONLY)</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.button("🤖 AI Agents", use_container_width=True)
    c2.button("🧬 Biotech", use_container_width=True)
    c3.button("🌐 Web3", use_container_width=True)
    c4.button("🚀 Space Tech", use_container_width=True)

    submitted = st.form_submit_button("🚀 LAUNCH RESEARCH", use_container_width=True)

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

state = st.session_state.state

if state:
    st.divider()
    st.subheader(f"📊 RESULTS — {st.session_state.topic}")

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
        "⬇️ DOWNLOAD REPORT (.md)",
        data=state.get("report", ""),
        file_name=f"{st.session_state.topic.strip().replace(' ', '_')}_report.md",
        mime="text/markdown",
        use_container_width=True,
    )

st.markdown('<div class="footer-tag">Multi-Agent Research System &nbsp;//&nbsp; Powered by LangGraph + LangChain</div>', unsafe_allow_html=True)