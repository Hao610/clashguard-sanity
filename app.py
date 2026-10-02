"""
ClashGuard — Cloud Security & Compliance Clash Resolver
Powered by Sanity Content Lake & Context Knowledge Graph
Official Submission for the Sanity Challenge (Path One: Ship an Agent That Queries Real Content)
"""

import streamlit as st
import time
from groq_client import query_sanity_graph

st.set_page_config(
    page_title="ClashGuard | Sanity Conflict Graph Agent",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Semantic Dual-Theme Design Tokens
st.markdown("""
<style>
    :root, [data-theme="dark"] {
        --bg-app: #050508;
        --text-primary: #ffffff;
        --text-secondary: #94a3b8;
        --card-a-bg: linear-gradient(135deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.8));
        --card-a-border: #3b82f6;
        --card-b-bg: linear-gradient(135deg, rgba(69, 10, 10, 0.4), rgba(30, 10, 10, 0.7));
        --card-b-border: #ef4444;
        --quote-bg: #090d16;
        --quote-text: #cbd5e1;
        --arb-bg: linear-gradient(135deg, rgba(6, 78, 59, 0.35), rgba(6, 95, 70, 0.2));
        --arb-border: #10b981;
    }

    @media (prefers-color-scheme: light) {
        :root:not([data-theme="dark"]) {
            --bg-app: #f8fafc;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --card-a-bg: #eff6ff;
            --card-a-border: #60a5fa;
            --card-b-bg: #fef2f2;
            --card-b-border: #f87171;
            --quote-bg: #ffffff;
            --quote-text: #1e293b;
            --arb-bg: #f0fdf4;
            --arb-border: #34d399;
        }
    }

    [data-theme="light"], .stApp[data-theme="light"] {
        --bg-app: #f8fafc;
        --text-primary: #0f172a;
        --text-secondary: #475569;
        --card-a-bg: #eff6ff;
        --card-a-border: #60a5fa;
        --card-b-bg: #fef2f2;
        --card-b-border: #f87171;
        --quote-bg: #ffffff;
        --quote-text: #1e293b;
        --arb-bg: #f0fdf4;
        --arb-border: #34d399;
    }

    .stApp { 
        background-color: var(--bg-app) !important; 
        color: var(--text-primary) !important;
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 900;
        background: linear-gradient(90deg, #f59e0b 0%, #ef4444 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }
    .hero-sub {
        font-size: 1.0rem;
        color: var(--text-secondary) !important;
        margin-bottom: 20px;
    }
    .conflict-card-a {
        background: var(--card-a-bg);
        border: 1px solid var(--card-a-border);
        border-radius: 12px;
        padding: 18px;
    }
    .conflict-card-b {
        background: var(--card-b-bg);
        border: 1px solid var(--card-b-border);
        border-radius: 12px;
        padding: 18px;
    }
    .arbitration-box {
        background: var(--arb-bg);
        border: 1px solid var(--arb-border);
        border-radius: 12px;
        padding: 20px;
        margin-top: 15px;
    }
    .evidence-quote {
        background: var(--quote-bg);
        border-left: 3px solid #64748b;
        padding: 8px 12px;
        font-family: monospace;
        font-size: 0.85rem;
        color: var(--quote-text);
        margin-top: 8px;
        border-radius: 4px;
        border: 1px solid rgba(100, 116, 139, 0.2);
    }
</style>
<script>
    (function() {
        function checkTheme() {
            try {
                const targetDoc = window.parent.document || document;
                const stApp = targetDoc.querySelector('.stApp') || document.querySelector('.stApp');
                const isLight = targetDoc.body.classList.contains('light-theme') || 
                               (stApp && window.getComputedStyle(stApp).backgroundColor.includes('255, 255, 255'));
                const themeVal = isLight ? "light" : "dark";
                document.documentElement.setAttribute("data-theme", themeVal);
                if (stApp) stApp.setAttribute("data-theme", themeVal);
            } catch(e) {}
        }
        checkTheme();
        try {
            const targetDoc = window.parent.document || document;
            const observer = new MutationObserver(checkTheme);
            observer.observe(targetDoc.body, { attributes: true, attributeFilter: ['class', 'style'] });
        } catch(e) {}
    })();
</script>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## ⚖️ **ClashGuard**")
    st.caption("`Autonomous Cloud Compliance Conflict Resolver`")
    
    st.info(
        "**💡 Why Keyword Search Fails:**\n\n"
        "When Terraform docs say a config is standard, but CIS Benchmark rates it Critical, "
        "a traditional search returns contradictory answers. "
        "\n\n**ClashGuard queries a Sanity Graph** where conflicting authorities are modeled as interconnected nodes."
    )
    
    st.markdown("---")
    st.markdown("### 🗄️ **Sanity Project Info**")
    st.markdown("- **Project ID:** `1rqqy3g5`")
    st.markdown("- **Dataset:** `production`")
    st.markdown("- **Query Engine:** GROQ Graph Dereferencing (`->`)")
    st.markdown("- **Graph Documents:** 15 Nodes (Sources, Rules, Resources)")
    st.markdown("---")
    st.caption("🏆 Built for The Sanity Challenge (DEV.to 2026)")

# ─────────────────────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────────────────────

st.markdown('<div class="hero-title">⚖️ ClashGuard: When Compliance Frameworks Disagree</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">An AI agent that resolves Terraform vs. CIS vs. PCI-DSS security clashes using Sanity\'s structured knowledge graph.</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Fetch Live Graph Data
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=60)
def load_graph():
    return query_sanity_graph()

conflicts = load_graph()

# Resource Selector
resource_options = [f"{item['resource']['name']} ({item['resource']['resourceKind']})" for item in conflicts]
selected_idx = st.selectbox("🎯 Select a Cloud Resource Under Audit:", range(len(resource_options)), format_func=lambda i: resource_options[i])

active_item = conflicts[selected_idx]
resource = active_item["resource"]
source_a = active_item["source"]
conflict_list = active_item.get("conflicts", [])

# ─────────────────────────────────────────────────────────────────────────────
# Side-by-Side Conflict Panel
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(f"### 🔍 Auditing Target: `{resource['name']}`")
st.caption(f"Risk Surface: {resource.get('riskSurface')}")

col_a, col_vs, col_b = st.columns([1.8, 0.4, 1.8])

with col_a:
    st.markdown(f"""
    <div class="conflict-card-a">
        <h4 style="margin:0; color:#38bdf8;">📄 Source A: {source_a['shortCode']}</h4>
        <p style="margin:4px 0; font-size:0.85rem; color:var(--text-secondary);"><strong>Authority:</strong> {source_a['name']} ({source_a['authorityType']})</p>
        <p style="margin:4px 0; font-size:0.9rem;"><strong>Rule ID:</strong> <code>{active_item['ruleId']}</code></p>
        <p style="margin:4px 0; font-weight:600;">{active_item['title']}</p>
        <p style="margin:4px 0;"><strong>Stance:</strong> <span style="background:#0369a1; color:#fff; padding:2px 6px; border-radius:4px; font-size:0.8rem;">{active_item['verdictStance']}</span></p>
        <div class="evidence-quote">"{active_item['verbatimRequirement']}"</div>
    </div>
    """, unsafe_allow_html=True)

with col_vs:
    st.markdown("<br><br><br><h2 style='text-align: center; color: #ef4444;'>⚡ VS ⚡</h2>", unsafe_allow_html=True)

with col_b:
    if conflict_list:
        conf_b = conflict_list[0]
        source_b = conf_b["source"]
        st.markdown(f"""
        <div class="conflict-card-b">
            <h4 style="margin:0; color:#f87171;">🛑 Source B: {source_b['shortCode']}</h4>
            <p style="margin:4px 0; font-size:0.85rem; color:var(--text-secondary);"><strong>Authority:</strong> {source_b['name']} ({source_b['authorityType']})</p>
            <p style="margin:4px 0; font-size:0.9rem;"><strong>Rule ID:</strong> <code>{conf_b['ruleId']}</code></p>
            <p style="margin:4px 0; font-weight:600;">{conf_b['title']}</p>
            <p style="margin:4px 0;"><strong>Stance:</strong> <span style="background:#b91c1c; color:#fff; padding:2px 6px; border-radius:4px; font-size:0.8rem;">{conf_b['verdictStance']} ({conf_b['enforcementLevel']})</span></p>
            <div class="evidence-quote">"{conf_b['verbatimRequirement']}"</div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Graph-Derived Reconciliation & Audit Arbitration
# ─────────────────────────────────────────────────────────────────────────────

st.markdown(f"""
<div class="arbitration-box">
    <h3 style="margin:0 0 10px 0; color:#34d399;">🛡️ Sanity Graph Agent Arbitration (Resolving the Clash)</h3>
    <p style="font-size:0.9rem; color:var(--text-secondary); margin-bottom:14px;">
        <strong>Why traditional AI hallucinates here:</strong> A vector search without graph references conflates the vendor recommendation with the audit rule,
        either falsely failing legitimate CDN deployments or falsely approving public buckets.
    </p>
    <div style="background:rgba(16,185,129,0.1); border-left:4px solid #10b981; padding:12px; border-radius:6px; margin-bottom:10px;">
        <strong style="color:#10b981;">🎯 Architectural Resolution Advice:</strong>
        <p style="margin:4px 0 0 0; color:var(--text-primary);">{active_item.get('reconciliationAdvice', '')}</p>
    </div>
    <div style="background:rgba(245,158,11,0.1); border-left:4px solid #f59e0b; padding:12px; border-radius:6px;">
        <strong style="color:#f59e0b;">⚙️ Compliance Hardening Action:</strong>
        <p style="margin:4px 0 0 0; color:var(--text-primary);">{conflict_list[0].get('reconciliationAdvice', '') if conflict_list else ''}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Raw GROQ Graph Proof
# ─────────────────────────────────────────────────────────────────────────────

with st.expander("🔬 View Raw Dereferenced Sanity GROQ JSON"):
    st.json(active_item)
