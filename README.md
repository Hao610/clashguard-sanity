# ⚖️ ClashGuard

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Powered by: Sanity Content Lake](https://img.shields.io/badge/Backend-Sanity%20Content%20Lake-F03E2F?logo=sanity)](https://www.sanity.io/)
[![Query Engine: GROQ Graph](https://img.shields.io/badge/Query-GROQ%20Graph%20Dereference-3B82F6)](https://www.sanity.io/docs/groq)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?logo=python)](https://www.python.org/)

> **When Terraform says compliant but CIS Benchmark says critical:**  
> An autonomous AI compliance conflict resolver powered by Sanity Content Lake and GROQ graph dereferencing.

*Official Submission for [The Sanity Challenge: Path One (Ship an Agent That Queries Real Content)](https://dev.to/challenges/sanity-2026-09-16)*

---

## 🎯 The Core Problem: Why Traditional Keyword Search & RAG Fail

In enterprise cloud security, **authoritative rulebooks frequently contradict each other**:

1. **Vendor Architecture Guides & Terraform Specs** permit and recommend patterns for operational scale (e.g., S3 public bucket policies for CloudFront CDN origins, `hostNetwork: true` for Kubernetes CNI Daemons, or whitelisted direct public RDS endpoints for BI tools).
2. **Regulatory & Hardening Frameworks** (CIS Benchmarks, PCI-DSS v4.0, NSA Hardening) flatly prohibit these same patterns as **CRITICAL security failures**.

### The RAG Failure Mode
When an engineering team asks a standard vector RAG agent: *"Can my S3 bucket have public read permissions for CloudFront?"*
- Standard text search retrieves snippets from both sides, **conflating vendor defaults with regulatory audits**.
- The AI either hallucinates a false pass (violating compliance) or raises false alarms (breaking production deployments).

---

## 💡 The Solution: Because It's Modeled as a Graph

ClashGuard solves this because the domain knowledge is **not a blob of text — it is an interconnected Graph in Sanity Content Lake**.

```
    ┌──────────────────────────┐             ┌──────────────────────────┐
    │  Authority Source A      │             │  Authority Source B      │
    │  (AWS Well-Architected)  │             │  (CIS AWS Benchmark)     │
    └─────────────┬────────────┘             └─────────────┬────────────┘
                  │                                        │
                  ▼                                        ▼
    ┌──────────────────────────┐   conflictsWith     ┌──────────────────────────┐
    │ Compliance Rule A        │◄───────────────────►│ Compliance Rule B        │
    │ (AWS-ARCH-S3-004)        │                     │ (CIS-AWS-2.1.5)          │
    │ STANCE: RECOMMENDED      │                     │ STANCE: STRICT_FORBIDDEN │
    └─────────────┬────────────┘                     └─────────────┬────────────┘
                  │                                        │
                  └──────────────────┬─────────────────────┘
                                     │ resource
                                     ▼
                       ┌───────────────────────────┐
                       │ Cloud Resource Target     │
                       │ (aws_s3_bucket)           │
                       └───────────────────────────┘
```

Using **GROQ graph dereferencing (`->`)**, ClashGuard traverses bidirectional conflict edges and surfaces **both claims side-by-side with verbatim evidence quotes and reconciliation advice**.

---

## 🗄️ Sanity Project Details

As required by the Sanity Challenge rules:
- **Sanity Project ID:** `1rqqy3g5`
- **Dataset:** `production` (Public)
- **Public API Query Endpoint:**
  ```text
  https://1rqqy3g5.api.sanity.io/v2024-10-01/data/query/production?query=*[_type=="complianceRule"]
  ```

---

## 🚀 Quickstart

```bash
# 1. Clone the repository
git clone https://github.com/Hao610/clashguard-sanity.git
cd clashguard-sanity

# 2. Install lightweight dependencies
pip install streamlit

# 3. Launch the agent dashboard
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 📜 License

Distributed under the Apache 2.0 Open Source License. See [`LICENSE`](LICENSE) for details.
