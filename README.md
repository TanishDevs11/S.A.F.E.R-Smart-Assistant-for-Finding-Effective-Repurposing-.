S.A.F.E.R

Safety-Aware Framework for Drug Repurposing

Overview

S.A.F.E.R is a modular, safety-aware drug repurposing pipeline built entirely on live Open Targets Platform data.
It identifies biologically plausible new disease indications for existing drugs and explicitly penalizes unsafe candidates using real-world pharmacovigilance signals.

Rather than answering only “what might work”, S.A.F.E.R is designed to answer:

“What might work safely?”

The framework is logic-first, interpretable, reproducible, and designed as a decision-support tool for exploratory research.

Key Features:

1. ChEMBL-centric drug identity resolution

2. Mechanism- and target-driven disease prioritization

3. Automatic exclusion of known indications

4. Integration of real pharmacovigilance (FAERS) safety signals

5. Safety-aware disease re-scoring (SAFER score)

6. Live queries to the Open Targets GraphQL API (no static datasets)

Fully modular and extensible architecture:
```
Pipeline Architecture:

ChEMBL Drug ID
      ↓
Drug Identity Validation (Stage 1)
      ↓
Mechanism of Action & Target Mapping (Stage 2)
      ↓
Target → Disease Associations (Stage 3)
      ↓
Known Indication Filtering
      ↓
Safety Signal Analysis (Stage 4)
      ↓
Safety-Aware Disease Re-scoring

```
Project Structure
S.A.F.E.R/
├── app.py                      # Pipeline orchestrator (main entry point)
├── chembl/                     # STAGE 1: Drug identity
│   ├── validator.py            # Validates ChEMBL IDs
│   ├── resolver.py             # Resolves drug metadata
│   └── parser.py               # Normalizes raw API responses
├── mechanism/                  # STAGE 2: Mechanism & targets
│   ├── fetcher.py              # Fetches mechanisms of action
│   └── normalizer.py           # Normalizes mechanism data
├── stage3/                     # STAGE 3: Disease prioritization
│   ├── fetcher.py              # Retrieves target–disease associations
│   ├── aggregator.py           # Aggregates association evidence
│   ├── filter.py               # Removes known indications
│   ├── ranker.py               # Scores disease relevance
│   └── prioritizer.py          # Final disease ranking logic
├── safety/                     # STAGE 4: Safety layer
│   ├── fetcher.py              # Fetches pharmacovigilance signals
│   ├── normalizer.py           # Normalizes ADR signals
│   └── scorer.py               # Applies safety penalties
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```
Installation & Setup: 
Clone the Repository
git clone <your-repo-url>
cd S.A.F.E.R
```
```
Create and Activate a Virtual Environment
python -m venv venv
```
```
Windows

.\venv\Scripts\Activate.ps1
```
```
Linux / macOS

source venv/bin/activate
```
```
Install Dependencies
pip install -r requirements.txt
```

Running S.A.F.E.R

Run the full pipeline using a ChEMBL ID:
```
python app.py
```

You will be prompted to enter a ChEMBL identifier.

Example
```
Input : CHEMBL25

Output: (simplified)

{
  "drug": {
    "chembl_id": "CHEMBL25",
    "drug_name": "ASPIRIN",
    "drug_type": "Small molecule",
    "clinical_status": "4"
  },
  "safety_summary": {
    "risk_level": "HIGH",
    "mean_signal": 1150.43,
    "max_signal": 5511.95
  },
  "results": [
    {
      "disease_name": "gout",
      "association_score": 0.6159,
      "safer_score": 0.308,
      "safety_risk": "HIGH"
    }
  ]
}
```

SAFER Scoring Logic
Risk Level	Penalty Factor
LOW	      1.00
MEDIUM	0.75
HIGH	      0.50

SAFER Score is calculated as:
```
SAFER Score = Association Score × Safety Penalty
```

This ensures that strong biological associations are preserved while unsafe candidates are deprioritized.

Data Sources:
```
All data are fetched live at runtime.

1. Open Targets Platform (GraphQL API)

2. Drug–target–disease associations

3. Mechanisms of action

4. Clinical evidence scores

5. Pharmacovigilance (FAERS)

6. Adverse drug reaction signals

7. Log likelihood ratios (logLR)

```

No datasets are downloaded or stored locally.

Design Philosophy:

```
Interpretable (No black-box machine learning)
      ↓
Modular and Extensible
      ↓
Deterministic and Reproducible
      ↓
Logic-First MVP
      ↓
No Database or Persistent Storage
      ↓
Frontend Optional and Decoupled

```

Disclaimer:

S.A.F.E.R is a research and decision-support tool.
It does not provide clinical recommendations and must not be used for medical decision-making.

Acknowledgements:

This project is built using publicly available data from the Open Targets Platform.
