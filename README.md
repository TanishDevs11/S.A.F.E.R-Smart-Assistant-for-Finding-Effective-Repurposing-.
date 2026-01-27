S.A.F.E.R

Safety-Aware Framework for Drug Repurposing

S.A.F.E.R is a modular, safety-aware drug repurposing pipeline built on live Open Targets Platform data.
It identifies biologically plausible new disease indications for existing drugs and explicitly penalizes unsafe candidates using real-world adverse event data.

Not just “what might work”, but “what might work safely”.

Key Features:

1. ChEMBL-centric drug identity resolution
2. Mechanism- and target-driven disease prioritization
3. Automatic exclusion of known indications
4. Real pharmacovigilance (FAERS) safety signals
5. Safety-aware re-scoring (SAFER score)
6. Live queries to Open Targets (no static datasets)
7. Fully modular, extensible architecture

Pipeline:

ChEMBL Drug ID
      ↓
Drug Identity Validation (Stage 1)
      ↓
Mechanism of Action & Targets (Stage 2)
      ↓
Target → Disease Associations (Stage 3)
      ↓
Known Indication Filtering
      ↓
Safety Signal Analysis (Stage 4)
      ↓
Safety-Aware Disease Re-scoring

Project Structure:
S.A.F.E.R/
│
├── app.py                  # Pipeline orchestrator
│
├── chembl/                 # Stage 1 – Drug identity
│   ├── validator.py
│   ├── resolver.py
│   └── parser.py
│
├── mechanism/              # Stage 2 – Mechanism & targets
│   └── fetcher.py
│
├── stage3/                 # Stage 3 – Disease prioritization
│   ├── fetcher.py
│   ├── aggregator.py
│   ├── filter.py
│   ├── ranker.py
│   └── prioritizer.py
│
├── safety/                 # Stage 4 – Safety layer
│   ├── fetcher.py
│   ├── normalizer.py
│   └── scorer.py
│
├── requirements.txt
└── README.md

Installation & Setup
Clone the repository
git clone <your-repo-url>
cd S.A.F.E.R

Create & activate virtual environment
python -m venv venv


Windows

.\venv\Scripts\Activate.ps1


Linux / macOS

source venv/bin/activate

Install dependencies
pip install -r requirements.txt

Running SAFER

Run the full pipeline using a ChEMBL ID:

python app.py

Example (CHEMBL25 – Aspirin)
{
  "drug": {...},
  "safety_summary": {...},
  "results": [
    {
      "disease_name": "gout",
      "association_score": 0.6159,
      "safer_score": 0.308,
      "safety_risk": "HIGH"
    },
    ...
  ]
}

SAFER Scoring Logic
Risk Level	Penalty Factor
LOW	1.0
MEDIUM	0.75
HIGH	0.5
SAFER Score = Association Score × Safety Penalty


This ensures biological plausibility is preserved while unsafe drugs are deprioritized.

Data Sources

Open Targets Platform (GraphQL API)

Drug–target–disease associations

Mechanisms of action

Pharmacovigilance (FAERS)

No datasets are downloaded or stored locally.

Design Philosophy

Interpretable (no black-box ML)

Modular & extensible

Reproducible & deterministic

No UI / No database (logic-first MVP)



Disclaimer:

S.A.F.E.R is a research and decision-support tool.
It does not make clinical recommendations.

Acknowledgements:

Built using publicly available data from the Open Targets Platform.
