# Data Guide — Catalyst Discovery Agent (Stream 4)

---

## Primary Source: Catalysis-Hub

- **Portal:** https://www.catalysis-hub.org/  
- **GraphQL API:** http://api.catalysis-hub.org/graphql  
- **Scale:** ~**158k** reactions (community-contributed DFT adsorption / reaction energies)  
- **Formats:** JSON via GraphQL (cache locally as JSON or CSV)  
- **Account:** **No account required** for read queries

### Typical fields

| Field | Meaning |
|---|---|
| `chemicalComposition` | Surface / adsorbate stoichiometry |
| `reactants` / `products` | Adsorption / desorption species |
| `reactionEnergy` | Reaction or adsorption energy (eV) |
| `facet` | Miller indices when available |
| `pubId` / `doi` | Literature provenance |

Exact schema evolves — introspect via GraphQL or inspect returned documents.

---

## Setup

### 1. No account required

Public GraphQL endpoint — no API key for read access.

### 2. Example query (curl)

```bash
curl -X POST http://api.catalysis-hub.org/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ reactions(first: 5, reactants: \"H\") { totalCount edges { node { chemicalComposition reactionEnergy facet pubId } } } }"}'
```

### 3. Example query (Python)

```python
import json
import requests

query = """
{
  reactions(first: 100, reactants: "H") {
    totalCount
    edges {
      node {
        chemicalComposition
        reactionEnergy
        facet
        pubId
      }
    }
  }
}
"""

resp = requests.post(
    "http://api.catalysis-hub.org/graphql",
    json={"query": query},
    timeout=30,
)
resp.raise_for_status()
data = resp.json()

# Cache locally
import pathlib
out = pathlib.Path("data/raw/catalysis-hub/her_h_adsorption.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(data, indent=2))
print("cached", out)
```

### 4. Convert to CSV (optional)

Flatten `edges[].node` into a pandas DataFrame for offline agent runs.

---

## Suggested Local Layout

```
data/
├── README.md
└── raw/
    └── catalysis-hub/
        ├── her_h_adsorption.json
        └── catalyst_shortlist.csv   # optional processed cache
```

---

## Offline Hackathon Fallback

If the API is slow or unavailable during the event, cache a few hundred rows on Saturday morning. The starter agent **generates** a synthetic adsorption-energy table on first run if no cache is present (written under `data/raw/`, which is gitignored).

---

## License & Redistribution

> **LICENSE NOTE:** Catalysis-Hub aggregates contributions from many research groups. **Default to research-only use.** Before bulk redistribution, check each entry's `pubId` / DOI via the portal and honor the original publication's terms. Cite Catalysis-Hub and the underlying DFT studies referenced by each entry. Do not commit large bulk dumps to Git.

### Citation

Acknowledge Catalysis-Hub and the underlying DFT studies referenced by each entry.
