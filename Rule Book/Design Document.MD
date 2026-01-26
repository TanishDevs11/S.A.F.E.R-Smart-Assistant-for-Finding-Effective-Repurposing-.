Design Document
Project S.A.F.E.R (Stage 1) Drug Identity Resolution via ChEMBL ID

1. Design Philosophy
Stage 1 of S.A.F.E.R prioritizes correctness, clarity, and extensibility over visual complexity. This stage is API-first and logic-first, leveraging the Open Targets Model Context Protocol (MCP) to ensure high-fidelity data resolution without UI overhead.

The design is intentionally minimal to:

Reduce cognitive load.

Avoid premature UI decisions.

Support rapid iteration via "vibe coding".

Allow clean expansion in later stages.

Design Principle: If a component does not improve drug identity validation, it does not belong in Stage 1.

2. Scope of Design (Stage 1)
✅ Included

Input handling for ChEMBL ID.

Backend data flow via Open Targets MCP.

Output structure (JSON).

Error states and messaging.

Internal module boundaries.

❌ Excluded

Visual UI styling and frontend frameworks.

Charts, dashboards, and user authentication.

Persistent storage (SQL/NoSQL).

3. High-Level System Design
3.1 Component Overview
Code snippet
graph TD
    A[User / CLI / API Call] --> B(ChEMBL ID Input)
    B --> C{Input Validation Layer}
    C -->|Valid| D[Drug Resolver Module]
    C -->|Invalid| E[Error JSON]
    D --> F[Open Targets MCP Server]
    F --> G[Response Parser]
    G --> H[JSON Output]
4. User Interaction Design
4.1 Interaction Model (Stage 1)
Interaction Type: Command-line script invocation or API-style function call.

Example Interaction:

Input: CHEMBL25

Output: JSON drug profile

5. Input Design
5.1 Input Format
Type: String.

Format Constraint: CHEMBL[0-9]+ (Strict regex).

Valid Example: CHEMBL25.

Invalid Examples: imatinib, chembl_25, CHEMBLXYZ.

6. Output Design
6.1 Output Format
Format: JSON only.

Structure: Deterministic and schema-stable.

Schema:

JSON
{
  "chembl_id": "string",
  "drug_name": "string",
  "drug_type": "string",
  "clinical_status": "string | null"
}
7. Error State Design
Error handling is a first-class design element, not an afterthought.

Output Format: { "error": "Descriptive error message" }.

Scenarios:

Invalid ID format: Reject immediately.

ID not found: Return clear "not found" error via MCP.

API/MCP unavailable: Return service error.

Partial data: Return available fields with null for missing keys.

8. Internal Module Design
8.1 Module Responsibilities (chembl/ folder)
validator.py: Validates ChEMBL ID format using regex.

resolver.py: Handles authentication and queries to the Open Targets MCP.

parser.py: Normalizes the complex MCP/API response into the simplified S.A.F.E.R JSON schema.

9. Extensibility by Design
Stage 1 is designed to allow future stages to “plug in” without refactoring.

Planned Extensions: Drug → Mechanism of Action, Drug → Target mapping, and Safety-aware scoring.

Design Decision: All future stages will consume the Stage 1 drug object as their primary input.

10. Design Constraints
No database or UI dependencies.

No hardcoded drug data.

Must align strictly with the Open Targets data model via MCP.

11. Design Success Criteria
The design is successful if:

The system accepts only valid ChEMBL IDs.

Outputs are predictable, clean, and MCP-verified.

Code modules are reusable for Stage 2 expansion.

12. Summary
The updated Stage 1 design of S.A.F.E.R establishes a clean, minimal, and MCP-integrated foundation focused exclusively on drug identity resolution.