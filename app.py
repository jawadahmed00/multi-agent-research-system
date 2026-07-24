import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(page_title="Multi-Agent Research System", page_icon="🔎", layout="wide")

st.title("🔎 Multi-Agent Research System")
st.caption("Search agent → Reader agent → Writer → Critic")

# Keep results across reruns (e.g. when expanders are toggled)
if "state" not in st.session_state:
    st.session_state.state = None

with st.form("research_form"):
    topic = st.text_input("Research topic", placeholder="e.g. Impact of LLM agents on scientific research")
    submitted = st.form_submit_button("Run Research", use_container_width=True)

if submitted:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        status = st.status("Starting pipeline...", expanded=True)
        try:
            status.write("Step 1 — Search agent gathering information...")
            status.write("Step 2 — Reader agent scraping top source...")
            status.write("Step 3 — Writer drafting the report...")
            status.write("Step 4 — Critic reviewing the report...")

            state = run_research_pipeline(topic)
            st.session_state.state = state
            st.session_state.topic = topic

            status.update(label="Pipeline complete", state="complete", expanded=False)
        except Exception as e:
            status.update(label="Pipeline failed", state="error", expanded=True)
            st.error(f"Something went wrong: {e}")

state = st.session_state.state

if state:
    st.divider()
    st.subheader(f"Results for: {st.session_state.topic}")

    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["📄 Report", "🧐 Critic Feedback", "🔍 Search Results", "📚 Scraped Content"]
    )

    with tab_report:
        st.markdown(state.get("report", "No report generated."))

    with tab_feedback:
        st.markdown(state.get("feedback", "No feedback generated."))

    with tab_search:
        st.text(state.get("search_results", "No search results."))

    with tab_scraped:
        st.text(state.get("scraped_content", "No scraped content."))

    st.download_button(
        "Download Report (.md)",
        data=state.get("report", ""),
        file_name=f"{st.session_state.topic.strip().replace(' ', '_')}_report.md",
        mime="text/markdown",
        use_container_width=True,
    )