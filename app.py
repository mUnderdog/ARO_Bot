# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import os
import time
import html as _html
from dotenv import load_dotenv

# Load .env BEFORE importing project modules so config.py picks up keys
load_dotenv(override=True)

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ARO Bot — Automated Research & Outreach",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

:root {
    --bg:        #0d1117;
    --card:      #161b22;
    --input:     #1c2230;
    --accent:    #4f8ef7;
    --alight:    #79aaff;
    --green:     #3fb950;
    --yellow:    #e3b341;
    --red:       #f85149;
    --muted:     #8b949e;
    --border:    #30363d;
    --radius:    12px;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg) !important;
    color: #e6edf3 !important;
}

/* Hide chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: #e6edf3 !important; }

/* sidebar brand */
.brand {
    text-align: center;
    padding: 1.6rem 0 0.6rem;
}
.brand-title {
    font-size: 1.7rem;
    font-weight: 700;
    background: linear-gradient(135deg, #4f8ef7, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1.2;
}
.brand-sub {
    font-size: 0.68rem !important;
    color: var(--muted) !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 4px !important;
}

/* status pill */
.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 0.3rem 0.85rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    margin: 0.6rem auto 0;
}
.status-ready  { background: rgba(63,185,80,.12);  border:1px solid rgba(63,185,80,.3);  color: #3fb950; }
.status-run    { background: rgba(79,142,247,.12); border:1px solid rgba(79,142,247,.3); color: #79aaff; }
.status-done   { background: rgba(63,185,80,.16);  border:1px solid rgba(63,185,80,.4);  color: #3fb950; }
.status-err    { background: rgba(248,81,73,.12);  border:1px solid rgba(248,81,73,.3);  color: #f85149; }
.pulse {
    width: 7px; height: 7px; border-radius: 50%;
    background: currentColor;
    animation: pulse 1.5s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.35} }

/* section divider */
.sec {
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin: 1.2rem 0 0.35rem;
    padding-bottom: 0.3rem;
    border-bottom: 1px solid var(--border);
}

/* inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput input {
    background: var(--input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 0.82rem !important;
    transition: border-color .2s, box-shadow .2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(79,142,247,.2) !important;
}

/* run button */
.stButton > button {
    background: linear-gradient(135deg,#4f8ef7,#7c6be8) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    width: 100% !important;
    padding: 0.6rem 1.4rem !important;
    transition: opacity .2s, transform .15s !important;
    letter-spacing: 0.03em;
}
.stButton > button:hover  { opacity:.85!important; transform:translateY(-2px)!important; }
.stButton > button:active { transform:translateY(0)!important; }

/* download button */
.stDownloadButton > button {
    background: linear-gradient(135deg,#3fb950,#2ea043) !important;
    color:#fff!important; border:none!important;
    border-radius:8px!important; font-weight:600!important; width:100%!important;
    transition: opacity .2s, transform .15s !important;
}
.stDownloadButton > button:hover { opacity:.85!important; transform:translateY(-2px)!important; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg,#0f2038,#1a1145 50%,#0d2a20);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2.2rem 2.6rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content:''; position:absolute; top:-70px; right:-70px;
    width:220px; height:220px;
    background: radial-gradient(circle,rgba(79,142,247,.15),transparent 70%);
    border-radius:50%;
}
.hero::after {
    content:''; position:absolute; bottom:-50px; left:-50px;
    width:160px; height:160px;
    background: radial-gradient(circle,rgba(124,107,232,.12),transparent 70%);
    border-radius:50%;
}
.hero h2 {
    font-size:1.85rem!important; font-weight:700!important; margin-bottom:.3rem!important;
    background:linear-gradient(90deg,#79aaff,#c084fc);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.hero p { color:var(--muted)!important; font-size:.9rem!important; max-width:600px; margin:0; }

/* chips row */
.chips { display:flex; gap:.7rem; margin-top:1.1rem; flex-wrap:wrap; }
.chip {
    background:rgba(255,255,255,.05); border:1px solid var(--border);
    border-radius:20px; padding:.25rem .85rem;
    font-size:.75rem; color:var(--muted);
    display:flex; align-items:center; gap:.4rem;
    transition: border-color .2s, background .2s;
}
.chip:hover { background:rgba(79,142,247,.08); border-color:rgba(79,142,247,.4); }
.dot { width:7px; height:7px; border-radius:50%; display:inline-block; }

/* ── Metrics bar ── */
.metrics {
    display:flex; gap:1rem; margin-bottom:1.4rem; flex-wrap:wrap;
}
.metric-card {
    flex:1; min-width:120px;
    background:var(--card); border:1px solid var(--border); border-radius:10px;
    padding:.9rem 1.1rem;
    transition: border-color .2s, transform .15s;
}
.metric-card:hover { border-color:var(--accent); transform:translateY(-2px); }
.metric-val { font-size:1.5rem; font-weight:700; color:#e6edf3; line-height:1; }
.metric-label { font-size:.72rem; color:var(--muted); margin-top:.25rem; text-transform:uppercase; letter-spacing:.06em; }

/* ── Company card ── */
.ccard {
    background:var(--card); border:1px solid var(--border); border-radius:var(--radius);
    padding:1.3rem 1.5rem; margin-bottom:1.1rem;
    transition:border-color .2s, transform .15s, box-shadow .2s;
    position:relative;
}
.ccard:hover {
    border-color:var(--accent)!important;
    transform:translateY(-2px);
    box-shadow:0 8px 30px rgba(79,142,247,.1);
}
.ccard-num {
    position:absolute; top:.9rem; right:1.1rem;
    background:rgba(79,142,247,.12); border:1px solid rgba(79,142,247,.25);
    color:var(--alight); font-size:.68rem; font-weight:600;
    border-radius:20px; padding:.12rem .55rem;
}
.ccard h3 { margin:0 0 .7rem!important; font-size:1.05rem!important; font-weight:600!important; }
.badge {
    display:inline-block; border-radius:5px; font-size:.68rem;
    font-weight:600; padding:.1rem .5rem; margin-right:.3rem; margin-bottom:.3rem;
    text-transform:uppercase; letter-spacing:.06em;
}
.badge-blue { background:rgba(79,142,247,.12); color:var(--alight); border:1px solid rgba(79,142,247,.25); }
.badge-green { background:rgba(63,185,80,.1); color:#3fb950; border:1px solid rgba(63,185,80,.25); }
.research-box {
    background:#0d1117; border:1px solid var(--border); border-radius:8px;
    padding:.85rem 1rem; font-size:.83rem; color:var(--muted);
    line-height:1.65; margin:.65rem 0; white-space:pre-wrap;
}
.email-box {
    background:#0a1f1a; border:1px solid rgba(63,185,80,.25); border-radius:8px;
    padding:.85rem 1rem; font-size:.8rem; font-family:'Fira Code',monospace;
    color:#b5ead6; line-height:1.65; white-space:pre-wrap;
}

/* ── Log console ── */
.console {
    background:#07090d; border:1px solid var(--border); border-radius:10px;
    padding:1rem 1.2rem; font-family:'Fira Code',monospace;
    font-size:.78rem; max-height:260px; overflow-y:auto; line-height:1.75;
}
.log-ok   { color:#3fb950; }
.log-info { color:var(--alight); }
.log-warn { color:var(--yellow); }
.log-err  { color:var(--red); }

/* ── Tabs ── */
[data-testid="stTabBar"] button { font-weight:500!important; font-size:.85rem!important; }
[data-testid="stTabBar"] button[aria-selected="true"] {
    color:var(--accent)!important; border-bottom-color:var(--accent)!important;
}

/* ── Empty state ── */
.empty {
    text-align:center; padding:3.5rem 2rem; color:var(--muted);
}
.empty .ico { font-size:3rem; margin-bottom:.8rem; }
.empty h3   { font-size:1.05rem!important; margin:.4rem 0!important; }
.empty p    { font-size:.83rem!important; margin:0; }

/* ── Banner ── */
.banner-ok  {
    background:rgba(63,185,80,.08); border:1px solid rgba(63,185,80,.3);
    border-radius:10px; padding:.85rem 1.2rem; color:#3fb950;
    font-weight:500; margin-bottom:1.1rem; font-size:.88rem;
}
.banner-err {
    background:rgba(248,81,73,.08); border:1px solid rgba(248,81,73,.3);
    border-radius:10px; padding:.85rem 1.2rem; color:var(--red);
    font-weight:500; margin-bottom:1.1rem; font-size:.88rem;
}

/* progress bar */
[data-testid="stProgress"] > div > div {
    background:linear-gradient(90deg,#4f8ef7,#7c6be8)!important; border-radius:8px!important;
}

/* expander */
.streamlit-expanderHeader {
    background:var(--card)!important; border:1px solid var(--border)!important;
    border-radius:8px!important; font-weight:500!important; font-size:.85rem!important;
}

/* selectbox */
[data-baseweb="select"] > div {
    background:var(--input)!important; border:1px solid var(--border)!important;
    border-radius:8px!important;
}

/* sidebar footer */
.sf {
    text-align:center; color:var(--muted); font-size:.68rem;
    padding:.8rem 0 .4rem; border-top:1px solid var(--border);
    margin-top:1.4rem;
}
</style>
""", unsafe_allow_html=True)

# ── Import pipeline (keys already loaded from .env above) ─────────────────────
try:
    from utils.search     import search_companies
    from utils.researcher import research_company
    from utils.writer     import write_email
    _import_ok = True
    _import_err = ""
except Exception as _ie:
    _import_ok = False
    _import_err = str(_ie)

# ── Session state defaults ─────────────────────────────────────────────────────
for k, v in {
    "results":  [],
    "logs":     [],
    "running":  False,
    "done":     False,
    "status":   "ready",   # ready | running | done | error
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def log(msg, level="ok"):
    prefix = {"ok":"✔","info":"ℹ","warn":"⚠","err":"✖"}.get(level,"•")
    st.session_state.logs.append((level, f"[{prefix}] {msg}"))

# ── Pipeline ───────────────────────────────────────────────────────────────────
def run_pipeline(query, num_results, researcher_prompt, email_prompt):
    st.session_state.results = []
    st.session_state.logs    = []
    st.session_state.done    = False
    st.session_state.status  = "running"

    from config import GEMINI_API_KEY

    if not GEMINI_API_KEY:
        log("GEMINI_API_KEY not found in .env — LLM features will fail.", "err")
        st.session_state.status = "error"
        return

    with st.status("⚙️ Pipeline running…", expanded=True) as status_box:
        st.write(f'🔍 Searching for: **{query}**')
        log(f'Searching: "{query}"', "info")
        try:
            companies = search_companies(query)[:num_results]
            st.write(f"✅ Found **{len(companies)}** compan{'y' if len(companies)==1 else 'ies'}: {', '.join(companies)}")
            log(f"Found {len(companies)} compan{'y' if len(companies)==1 else 'ies'}: {', '.join(companies)}", "ok")
        except Exception as e:
            st.error(f"Search failed: {e}")
            log(f"Search failed: {e}", "err")
            st.session_state.status = "error"
            status_box.update(label="❌ Search failed", state="error")
            return

        results = []
        total = len(companies)
        prog  = st.progress(0, text="Starting…")
        for i, name in enumerate(companies, 1):
            prog.progress(int((i - 1) / total * 100), text=f"[{i}/{total}] Researching {name}…")
            log(f"[{i}/{total}] Researching: {name}", "info")
            st.write(f"🔎 [{i}/{total}] Researching **{name}**…")
            try:
                info = research_company(name, researcher_prompt)
                log(f"Research done for {name}", "ok")
            except Exception as e:
                info = f"Research failed: {e}"
                log(f"Research error — {name}: {e}", "err")

            prog.progress(int((i - 0.5) / total * 100), text=f"[{i}/{total}] Drafting email for {name}…")
            log(f"[{i}/{total}] Drafting email for: {name}", "info")
            st.write(f"✉️ [{i}/{total}] Drafting cold email for **{name}**…")
            try:
                email = write_email(info, email_prompt)
                log(f"Email drafted for {name}", "ok")
            except Exception as e:
                email = f"Email generation failed: {e}"
                log(f"Email error — {name}: {e}", "err")

            results.append({"company": name, "research": info, "email": email})
            st.session_state.results = results  # live update

        prog.progress(100, text="Done!")

        try:
            os.makedirs("data", exist_ok=True)
            pd.DataFrame(results).to_csv("data/leads.csv", index=False, encoding="utf-8")
            log("leads.csv saved to data/", "ok")
            st.write("💾 Results saved to `data/leads.csv`")
        except Exception as e:
            log(f"CSV save error: {e}", "warn")

        st.session_state.done   = True
        st.session_state.status = "done"
        log(f"Pipeline complete — {len(results)} companies processed 🎉", "ok")
        status_box.update(label=f"✅ Pipeline complete — {len(results)} companies processed!", state="complete")


# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:

    # ── Brand ──
    status = st.session_state.status
    pill_class = {"ready":"status-ready","running":"status-run","done":"status-done","error":"status-err"}.get(status,"status-ready")
    pill_label = {"ready":"Ready","running":"Running…","done":"Complete","error":"Error"}.get(status,"Ready")
    st.markdown(f"""
    <div class="brand">
        <div class="brand-title">🎓 ARO Bot</div>
        <div class="brand-sub">Automated Research & Outreach</div>
        <div style="text-align:center;margin-top:.6rem;">
            <span class="status-pill {pill_class}">
                <span class="pulse"></span>{pill_label}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Env status ──
    from config import GEMINI_API_KEY, GOOGLE_API_KEY, GOOGLE_CSE_ID
    gemini_ok = bool(GEMINI_API_KEY)
    google_ok = bool(GOOGLE_API_KEY and GOOGLE_CSE_ID)

    st.markdown('<div class="sec">🔐 Environment Status</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(
            f'<div style="font-size:.75rem;padding:.35rem .6rem;border-radius:6px;'
            f'background:{"rgba(63,185,80,.1)" if gemini_ok else "rgba(248,81,73,.1)"};'
            f'border:1px solid {"rgba(63,185,80,.3)" if gemini_ok else "rgba(248,81,73,.3)"};'
            f'color:{"#3fb950" if gemini_ok else "#f85149"};text-align:center;">'
            f'{"✔" if gemini_ok else "✖"} Gemini</div>', unsafe_allow_html=True)
    with col_b:
        st.markdown(
            f'<div style="font-size:.75rem;padding:.35rem .6rem;border-radius:6px;'
            f'background:{"rgba(63,185,80,.1)" if google_ok else "rgba(227,179,65,.1)"};'
            f'border:1px solid {"rgba(63,185,80,.3)" if google_ok else "rgba(227,179,65,.3)"};'
            f'color:{"#3fb950" if google_ok else "#e3b341"};text-align:center;">'
            f'{"✔" if google_ok else "⚠"} Google</div>', unsafe_allow_html=True)

    if not gemini_ok:
        st.warning("Add GEMINI_API_KEY to your `.env` file.", icon="⚠️")

    # ── Search config ──
    st.markdown('<div class="sec">🔍 Search Configuration</div>', unsafe_allow_html=True)
    query = st.text_input(
        "Search Query",
        value="AI startups in Noida",
        placeholder="e.g. fintech startups in Bangalore",
        key="query_input",
    )
    num_results = st.number_input(
        "Max Companies", min_value=1, max_value=10, value=3, step=1,
        key="num_results_input",
    )

    # ── Prompts ──
    st.markdown('<div class="sec">📝 Prompts (Optional Override)</div>', unsafe_allow_html=True)
    with open("prompts/researcher.txt", encoding="utf-8") as f:
        default_researcher = f.read()
    with open("prompts/email_writer.txt", encoding="utf-8") as f:
        default_email = f.read()

    with st.expander("✏️ Researcher Prompt"):
        researcher_prompt = st.text_area("res_prompt", value=default_researcher,
                                         height=150, label_visibility="collapsed",
                                         key="res_prompt_input")
    with st.expander("✏️ Email Writer Prompt"):
        email_prompt = st.text_area("email_prompt", value=default_email,
                                    height=150, label_visibility="collapsed",
                                    key="email_prompt_input")

    st.markdown("<br>", unsafe_allow_html=True)
    run_clicked = st.button("🚀 Run Pipeline", key="run_btn", use_container_width=True)

    if st.session_state.results and st.session_state.done:
        if st.button("🔄 Reset", key="reset_btn", use_container_width=True):
            st.session_state.results = []
            st.session_state.logs    = []
            st.session_state.done    = False
            st.session_state.status  = "ready"
            st.rerun()

    st.markdown('<div class="sf">ARO Bot v1.0 · Gemini Flash · For freshers 🎓</div>',
                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# MAIN — trigger pipeline
# ══════════════════════════════════════════════════════════════
# ── Show import error if utils failed to load ─────────────────────────────────
if not _import_ok:
    st.error(f"⚠️ Failed to import pipeline utilities: `{_import_err}`"
             f"\n\nCheck that all dependencies are installed (`pip install -r requirements.txt`).")

if run_clicked:
    if not _import_ok:
        st.error("Cannot run — pipeline utilities failed to import. See error above.")
    elif not query.strip():
        st.error("Please enter a search query.")
    elif not gemini_ok:
        st.error("GEMINI_API_KEY is missing from .env — cannot run.")
    else:
        run_pipeline(query.strip(), int(num_results), researcher_prompt, email_prompt)
        st.rerun()

# ── Hero banner ───────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h2>🎓 ARO Bot — Automated Research & Outreach</h2>
    <p>Discover AI/tech companies, auto-research them with Gemini, and generate
       personalised cold emails — all in one click. Built to help freshers land their first internship or job.</p>
    <div class="chips">
        <div class="chip"><span class="dot" style="background:#4f8ef7"></span>Google Search API</div>
        <div class="chip"><span class="dot" style="background:#a78bfa"></span>Gemini Flash</div>
        <div class="chip"><span class="dot" style="background:#3fb950"></span>Smart Email Drafting</div>
        <div class="chip"><span class="dot" style="background:#e3b341"></span>CSV Export</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Metrics row ───────────────────────────────────────────────
results = st.session_state.results
n_companies = len(results)
n_emails    = sum(1 for r in results if r.get("email") and "failed" not in r["email"].lower())
log_count   = len(st.session_state.logs)

st.markdown(f"""
<div class="metrics">
    <div class="metric-card">
        <div class="metric-val">{n_companies}</div>
        <div class="metric-label">Companies Found</div>
    </div>
    <div class="metric-card">
        <div class="metric-val">{n_emails}</div>
        <div class="metric-label">Emails Drafted</div>
    </div>
    <div class="metric-card">
        <div class="metric-val">{log_count}</div>
        <div class="metric-label">Log Events</div>
    </div>
    <div class="metric-card">
        <div class="metric-val">{'✔' if st.session_state.done else '–'}</div>
        <div class="metric-label">Pipeline Status</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────
tab_res, tab_log, tab_export = st.tabs(["📋 Results", "🖥️ Log Console", "📤 Export"])

# ── Results ───────────────────────────────────────────────────
with tab_res:
    if not results:
        st.markdown("""
        <div class="empty">
            <div class="ico">🔭</div>
            <h3>No results yet</h3>
            <p>Configure your query in the sidebar and click <b>Run Pipeline</b>.</p>
        </div>""", unsafe_allow_html=True)
    else:
        if st.session_state.done:
            st.markdown(f'<div class="banner-ok">✅ Pipeline complete — {len(results)} companies processed.</div>',
                        unsafe_allow_html=True)
        for i, r in enumerate(results, 1):
            safe_company  = _html.escape(r["company"])
            safe_research = _html.escape(r["research"]).replace("\n", "<br>")
            safe_email    = _html.escape(r["email"]).replace("\n", "<br>")
            st.markdown(f"""
            <div class="ccard">
                <span class="ccard-num">#{i}</span>
                <h3>🏢 {safe_company}</h3>
                <span class="badge badge-blue">Research</span>
                <span class="badge badge-green">Email Draft</span>
                <div class="research-box">{safe_research}</div>
                <p style="font-size:.73rem;color:#8b949e;margin:.5rem 0 .2rem;">✉️ Drafted Cold Email</p>
                <div class="email-box">{safe_email}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Log Console ───────────────────────────────────────────────
with tab_log:
    logs = st.session_state.logs
    if not logs:
        st.markdown("""
        <div class="empty">
            <div class="ico">🖥️</div>
            <h3>Console is empty</h3>
            <p>Run the pipeline to see live logs here.</p>
        </div>""", unsafe_allow_html=True)
    else:
        cls_map = {"ok":"log-ok","info":"log-info","warn":"log-warn","err":"log-err"}
        lines   = "".join(f'<div class="{cls_map.get(l,"")}">{m}</div>' for l, m in logs)
        st.markdown(f'<div class="console">{lines}</div>', unsafe_allow_html=True)

        # Copy-friendly raw text
        with st.expander("📄 View raw log text"):
            st.text("\n".join(m for _, m in logs))

# ── Export ────────────────────────────────────────────────────
with tab_export:
    if not results:
        st.markdown("""
        <div class="empty">
            <div class="ico">📂</div>
            <h3>Nothing to export</h3>
            <p>Run the pipeline first to generate leads.</p>
        </div>""", unsafe_allow_html=True)
    else:
        df = pd.DataFrame(results)
        st.markdown("### 📊 Leads Preview")
        st.dataframe(df[["company"]].rename(columns={"company":"Company"}),
                     use_container_width=True, hide_index=True)

        csv_bytes   = df.to_csv(index=False, encoding="utf-8").encode("utf-8")
        email_dump  = ("\n\n" + "="*60 + "\n\n").join(
                          f"Company: {r['company']}\n\n{r['email']}" for r in results)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.download_button("⬇️ Download leads.csv",  data=csv_bytes,
                               file_name="leads.csv", mime="text/csv",
                               key="dl_csv", use_container_width=True)
        with c2:
            st.download_button("📧 Download Emails (.txt)", data=email_dump.encode("utf-8"),
                               file_name="drafted_emails.txt", mime="text/plain",
                               key="dl_txt", use_container_width=True)

        st.markdown("""
        <div style="margin-top:1rem;padding:.9rem 1.2rem;background:var(--card);
                    border:1px solid var(--border);border-radius:10px;
                    font-size:.8rem;color:var(--muted);">
            📁 Results are also auto-saved to <code>data/leads.csv</code> in your project folder.
        </div>""", unsafe_allow_html=True)
