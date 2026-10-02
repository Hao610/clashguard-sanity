"""
ClashGuard GROQ Graph Query Client
Executes graph-traversal queries across Sanity Content Lake
to surface rule conflicts, verbatim evidence, and reconciliation paths.
"""

import json
import urllib.request
import urllib.parse
from typing import List, Dict, Any

PROJECT_ID = "1rqqy3g5"
DATASET = "production"
API_VERSION = "v2024-10-01"

# GROQ Graph Query:
# 1. Fetch compliance rules matching resource kind
# 2. Dereference the authority source (->)
# 3. Dereference conflicting rules (->) AND their respective authority sources (->)
CONFLICT_GRAPH_QUERY = """
*[_type == "complianceRule" && defined(conflictsWith)] {
  ruleId,
  title,
  verdictStance,
  verbatimRequirement,
  enforcementLevel,
  reconciliationAdvice,
  "resource": resource-> {
    name,
    resourceKind,
    provider,
    riskSurface
  },
  "source": source-> {
    name,
    shortCode,
    authorityType,
    strictnessScore,
    homepage,
    coreTenet
  },
  "conflicts": conflictsWith[]-> {
    ruleId,
    title,
    verdictStance,
    verbatimRequirement,
    enforcementLevel,
    reconciliationAdvice,
    "source": source-> {
      name,
      shortCode,
      authorityType,
      strictnessScore,
      homepage,
      coreTenet
    }
  }
}
"""

def query_sanity_graph() -> List[Dict[str, Any]]:
    """Queries the live Sanity Content Lake using GROQ."""
    encoded_query = urllib.parse.quote(CONFLICT_GRAPH_QUERY)
    url = f"https://{PROJECT_ID}.api.sanity.io/{API_VERSION}/data/query/{DATASET}?query={encoded_query}"
    
    req = urllib.request.Request(url, headers={"User-Agent": "ClashGuard-Agent/1.0"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data.get("result", [])

if __name__ == "__main__":
    results = query_sanity_graph()
    print(f"[+] Retrieved {len(results)} active conflict graph chains from Sanity:")
    for item in results:
        res = item.get("resource", {})
        src = item.get("source", {})
        print(f"\n[RESOURCE] {res.get('name')} ({res.get('resourceKind')})")
        print(f"   PRIMARY CLAIM: [{src.get('shortCode')}] {item.get('ruleId')} -- {item.get('title')}")
        print(f"   STANCE: {item.get('verdictStance')}")
        for conf in item.get("conflicts", []):
            c_src = conf.get("source", {})
            print(f"   [!] DIRECT CLASH WITH: [{c_src.get('shortCode')}] {conf.get('ruleId')} -- {conf.get('title')}")
            print(f"      OPPOSING STANCE: {conf.get('verdictStance')} ({conf.get('enforcementLevel')})")
