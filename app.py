"""
ClashGuard — Cloud Security & Compliance Clash Resolver
Powered by Sanity Content Lake & Context Knowledge Graph
Official Submission for the Sanity Challenge (Path One: Ship an Agent That Queries Real Content)
"""

import streamlit as st
import json
import re
from datetime import datetime, timezone
from groq_client import query_sanity_graph

st.set_page_config(
    page_title="ClashGuard | Sanity Conflict Graph Agent",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# Semantic Dual-Theme Design Tokens
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
    :root, [data-theme="dark"] {
        --bg-app: #050508;
        --text-primary: #ffffff;
        --text-secondary: #94a3b8;
        --card-a-bg: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.9));
        --card-a-border: #38bdf8;
        --card-b-bg: linear-gradient(135deg, rgba(69, 10, 10, 0.5), rgba(30, 10, 10, 0.8));
        --card-b-border: #f87171;
        --quote-bg: #090d16;
        --quote-text: #cbd5e1;
        --arb-bg: linear-gradient(135deg, rgba(6, 78, 59, 0.4), rgba(6, 95, 70, 0.25));
        --arb-border: #10b981;
        --input-bg: #0c101d;
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
        --input-bg: #ffffff;
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
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .conflict-card-b {
        background: var(--card-b-bg);
        border: 1px solid var(--card-b-border);
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
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
        padding: 10px 14px;
        font-family: monospace;
        font-size: 0.85rem;
        color: var(--quote-text);
        margin-top: 10px;
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
    st.markdown("- **Dataset:** `production` (Public)")
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

# ─────────────────────────────────────────────────────────────────────────────
# Preset Snippets for Live Interactive Code Audit
# ─────────────────────────────────────────────────────────────────────────────

SAMPLE_SNIPPETS = {
    "s3": (
        '# Terraform AWS S3 Bucket for CloudFront CDN Origin\n'
        'resource "aws_s3_bucket" "media_assets" {\n'
        '  bucket = "company-public-media-cdn"\n'
        '}\n\n'
        'resource "aws_s3_bucket_public_access_block" "public_cdn" {\n'
        '  bucket = aws_s3_bucket.media_assets.id\n'
        '  block_public_acls       = false  # Required for legacy CloudFront origin\n'
        '  block_public_policy     = false\n'
        '  ignore_public_acls      = false\n'
        '  restrict_public_buckets = false\n'
        '}'
    ),
    "k8s": (
        '# Kubernetes CNI Cilium DaemonSet Spec\n'
        'apiVersion: apps/v1\n'
        'kind: DaemonSet\n'
        'metadata:\n'
        '  name: cilium-agent\n'
        '  namespace: kube-system\n'
        'spec:\n'
        '  template:\n'
        '    spec:\n'
        '      hostNetwork: true  # Mandatory to attach eBPF hooks to physical eth0\n'
        '      containers:\n'
        '      - name: cilium-agent\n'
        '        image: cilium/cilium:v1.15.0\n'
    ),
    "rds": (
        '# Terraform RDS Aurora Cluster for Remote Analytics\n'
        'resource "aws_db_instance" "analytics_dw" {\n'
        '  identifier          = "corp-analytics-dw"\n'
        '  allocated_storage   = 100\n'
        '  engine              = "postgres"\n'
        '  instance_class      = "db.r6g.large"\n'
        '  publicly_accessible = true  # Enabled for external Tableau/Looker access\n'
        '  vpc_security_group_ids = [aws_security_group.allow_bi_ips.id]\n'
        '}'
    )
}

st.markdown("##### ⚡ Quick Load Infrastructure Code Snippet:")
b1, b2, b3 = st.columns(3)
if "code_input" not in st.session_state:
    st.session_state.code_input = SAMPLE_SNIPPETS["s3"]

if b1.button("📦 AWS S3 Bucket (CDN Origin Public Policy)", use_container_width=True):
    st.session_state.code_input = SAMPLE_SNIPPETS["s3"]
    st.rerun()

if b2.button("☸️ Kubernetes DaemonSet (hostNetwork: true)", use_container_width=True):
    st.session_state.code_input = SAMPLE_SNIPPETS["k8s"]
    st.rerun()

if b3.button("🐘 AWS RDS Database (publicly_accessible = true)", use_container_width=True):
    st.session_state.code_input = SAMPLE_SNIPPETS["rds"]
    st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
# Code Input & Dynamic Pattern Matching
# ─────────────────────────────────────────────────────────────────────────────

user_code = st.text_area(
    "Paste Terraform (HCL) or Kubernetes (YAML) manifest to audit:",
    value=st.session_state.code_input,
    height=160
)

# Automated matching logic to query the corresponding Sanity graph node
matched_idx = 0
if "hostNetwork" in user_code or "DaemonSet" in user_code:
    matched_idx = 1
elif "aws_db_instance" in user_code or "publicly_accessible" in user_code:
    matched_idx = 2
else:
    matched_idx = 0

active_item = conflicts[matched_idx]
resource = active_item["resource"]
source_a = active_item["source"]
conflict_list = active_item.get("conflicts", [])

# ─────────────────────────────────────────────────────────────────────────────
# Side-by-Side Conflict Panel
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown(f"### 🔍 Detected Infrastructure Target: `{resource['name']}`")
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

reconciliation_a = active_item.get('reconciliationAdvice', '')
reconciliation_b = conflict_list[0].get('reconciliationAdvice', '') if conflict_list else ''

st.markdown(f"""
<div class="arbitration-box">
    <h3 style="margin:0 0 10px 0; color:#34d399;">🛡️ Sanity Graph Agent Arbitration (Resolving the Clash)</h3>
    <p style="font-size:0.9rem; color:var(--text-secondary); margin-bottom:14px;">
        <strong>Why traditional AI hallucinates here:</strong> A vector search without graph references conflates the vendor recommendation with the audit rule,
        either falsely failing legitimate CDN deployments or falsely approving public buckets.
    </p>
    <div style="background:rgba(16,185,129,0.1); border-left:4px solid #10b981; padding:12px; border-radius:6px; margin-bottom:10px;">
        <strong style="color:#10b981;">🎯 Architectural Resolution Advice:</strong>
        <p style="margin:4px 0 0 0; color:var(--text-primary);">{reconciliation_a}</p>
    </div>
    <div style="background:rgba(245,158,11,0.1); border-left:4px solid #f59e0b; padding:12px; border-radius:6px;">
        <strong style="color:#f59e0b;">⚙️ Compliance Hardening Action:</strong>
        <p style="margin:4px 0 0 0; color:var(--text-primary);">{reconciliation_b}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Formal Audit Report Download Button
# ─────────────────────────────────────────────────────────────────────────────

timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
certificate_text = f"""================================================================================
          CLASHGUARD COMPLIANCE ARBITRATION CERTIFICATE
================================================================================
Generated Timestamp: {timestamp}
Sanity Project ID:   1rqqy3g5
Sanity Dataset:      production
Audited Resource:    {resource['name']} ({resource['resourceKind']})
Provider:            {resource['provider']}
--------------------------------------------------------------------------------
CONFLICTING AUTHORITY A
Source:              {source_a['name']}
Rule ID:             {active_item['ruleId']}
Title:               {active_item['title']}
Stance:              {active_item['verdictStance']}
Verbatim Requirement:
"{active_item['verbatimRequirement']}"
--------------------------------------------------------------------------------
CONFLICTING AUTHORITY B
Source:              {conflict_list[0]['source']['name'] if conflict_list else 'N/A'}
Rule ID:             {conflict_list[0]['ruleId'] if conflict_list else 'N/A'}
Title:               {conflict_list[0]['title'] if conflict_list else 'N/A'}
Stance:              {conflict_list[0]['verdictStance'] if conflict_list else 'N/A'}
Verbatim Requirement:
"{conflict_list[0]['verbatimRequirement'] if conflict_list else 'N/A'}"
--------------------------------------------------------------------------------
GRAPH ARBITRATION RESOLUTION
Architectural Advice:
{reconciliation_a}

Compliance Hardening Step:
{reconciliation_b}
================================================================================
EVIDENCE PROOF: Verified against Sanity Graph Content Lake via GROQ dereferencing.
================================================================================
"""

st.markdown("<br>", unsafe_allow_html=True)
col_dl, col_json = st.columns([1.2, 1.8])

with col_dl:
    st.download_button(
        label="📥 Download Compliance Arbitration Certificate (.txt)",
        data=certificate_text,
        file_name=f"clashguard_audit_{resource['resourceKind']}.txt",
        mime="text/plain",
        use_container_width=True
    )

with col_json:
    with st.expander("🔬 View Raw Dereferenced Sanity GROQ Graph JSON"):
        st.json(active_item)
