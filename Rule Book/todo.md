SAFER — Stage 1 (ChEMBL ID Drug Identity Layer)

Goal: Build a minimal, robust drug identity resolver using ChEMBL IDs as the canonical input, leveraging the Open Targets Model Context Protocol (MCP) for data sourcing.



🧱 Phase 0 — Project Setup

\[ ] Create project root folder



\[ ] Initialize Git repository



\[ ] Create Python virtual environment



\[ ] Add .gitignore



\[ ] Create requirements.txt (Include mcp SDK)



📁 Phase 1 — Repo Structure

\[ ] Create base folder structure:



Plaintext

safer/

├── chembl/

│   ├── \_\_init\_\_.py

│   ├── validator.py

│   ├── resolver.py

│   └── parser.py

├── app.py

├── PRD.md

├── DESIGN.md

├── TECH\_RULES.md

└── todo.md

🔍 Phase 2 — Input Validation

\[ ] Implement ChEMBL ID format validation using regex CHEMBL\[0-9]+



\[ ] Reject malformed inputs immediately



\[ ] Return clear JSON error for invalid format



File: chembl/validator.py



🌐 Phase 3 — Drug Resolution (Core Logic)

\[ ] Configure Cursor/AI environment to connect to Open Targets MCP



\[ ] Implement function to query Open Targets via MCP server



\[ ] Resolve drug entity using ChEMBL ID



\[ ] Handle:



\[ ] Valid ID



\[ ] Non-existent ID (MCP "not found" state)



\[ ] MCP connection failure / timeout



File: chembl/resolver.py



🧩 Phase 4 — Response Parsing \& Normalization

\[ ] Extract required fields from MCP response:



\[ ] ChEMBL ID



\[ ] Drug name



\[ ] Drug type



\[ ] Clinical / approval status



\[ ] Normalize response into stable JSON schema



\[ ] Fill missing fields with null



File: chembl/parser.py



🔗 Phase 5 — Application Orchestration

\[ ] Wire validator → resolver → parser



\[ ] Implement main execution flow



\[ ] Ensure single entry point



File: app.py



⚠️ Phase 6 — Error Handling

\[ ] Handle invalid ChEMBL ID format



\[ ] Handle drug not found in Open Targets



\[ ] Handle MCP service/API failure



\[ ] Ensure all errors return JSON format (no stack traces)



🧪 Phase 7 — Manual Testing

\[ ] Test with a known valid ChEMBL ID (e.g., CHEMBL25)



\[ ] Test with invalid format (e.g., chembl\_25)



\[ ] Test with non-existent ID



\[ ] Verify deterministic JSON output



Note: No test framework required (Stage 1 rule).



📘 Phase 8 — Documentation Check

\[ ] Confirm PRD reflects actual MCP behavior



\[ ] Confirm Design Doc matches implementation



\[ ] Confirm Tech Rules are strictly respected



\[ ] Update README (optional, brief)



✅ Definition of Done (Stage 1)

Valid ChEMBL ID returns correct drug metadata via MCP



Invalid input fails gracefully with JSON error



Output is clean, stable JSON



No hardcoded drug data in the source code



Code is modular and ready for Stage 2 (Target Mapping)



🚫 Explicit Non-Tasks (Do NOT do)

❌ No drug name search



❌ No target mapping



❌ No disease associations



❌ No safety scoring



❌ No UI / frontend



🧠 Vibe Coding Rule (Read This Before Coding)

Complete tasks top-to-bottom.



Do not skip phases.



If a task isn’t in this file, it doesn’t get coded.



Would you like me to help you initialize the project by providing the .gitignore and requirements.txt contents?

