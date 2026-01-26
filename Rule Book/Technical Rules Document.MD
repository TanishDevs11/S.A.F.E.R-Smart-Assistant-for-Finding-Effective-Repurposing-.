Technical Rules Document

Project: S.A.F.E.R (Stage 1) Drug Identity Resolution via ChEMBL ID



1\. Purpose of This Document

This document defines the technical boundaries, standards, and constraints for developing S.A.F.E.R. Its goals are to:



Prevent overengineering



Maintain consistency during vibe coding



Enable clean expansion in later stages



Ensure hackathon- and platform-ready quality



If a decision is unclear during development, this document is the final authority.



2\. Tech Stack (Stage 1 – Locked)

2.1 Language: Python 3.10+



2.2 Libraries: mcp (Model Context Protocol SDK), requests (for fallback), and standard Python libraries only.



2.3 APIs \& Data Sources: Open Targets Model Context Protocol (MCP) server.



2.4 Explicitly Prohibited: Databases (SQL/NoSQL), Frontend frameworks, ORMs, ML models, and cloud/auth layers.



3\. Architecture Rules

3.1 Architecture Style: Modular, API-first, backend-only, and stateless.



3.2 Responsibility Separation: One file per responsibility (e.g., validator.py for input, resolver.py for MCP calls, parser.py for normalization).



No “god files”: Logic must be decoupled.



4\. Input Rules

Strict Validation: Only ChEMBL IDs are accepted.



Regex Format: Must strictly match CHEMBL\[0-9]+.



No Fallbacks: No drug name search, fuzzy matching, or silent corrections.



Fail Fast: Reject malformed inputs immediately.



5\. Output Rules

Format: JSON only.



Deterministic: Keys must remain stable across runs.



Schema: Missing fields must return as null, not omitted.



JSON

{

&nbsp; "chembl\_id": "CHEMBL25",

&nbsp; "drug\_name": "Imatinib",

&nbsp; "drug\_type": "Small molecule",

&nbsp; "clinical\_status": null

}

6\. Error Handling Rules

Errors are first-class outputs, not exceptions hidden in logs.



6.1 Format: { "error": "Human-readable explanation" }



6.2 Required Cases: Invalid format, ID not found in MCP, API timeout, and unexpected response structure.



Security: No stack traces exposed to users.



7\. Coding Standards

7.1 Code Style: Use clear function names, type hints, and no magic numbers or hardcoded drug data.



7.2 Functions Over Scripts: Core logic must live inside functions; if \_\_name\_\_ == "\_\_main\_\_": is for execution only.



8\. Version Control Rules

Git must be initialized before coding.



Small, meaningful commits with intent-based messages (e.g., feat: resolve drug via Open Targets MCP).



No large “dump commits”.



9\. Testing Rules (Lightweight)

Manual testing is mandatory for:



Valid ChEMBL ID → success JSON



Invalid format → error JSON



Non-existent ID → error JSON



No test framework is required for Stage 1, but logic must be testable.



10\. Performance \& Extensibility

Scalability: Single MCP/API call per resolution where possible; no caching.



Extensibility: All future stages must consume the Stage-1 drug object and extend (not modify) outputs.



Contracts: Breaking Stage-1 contracts is strictly prohibited.



11\. What NOT to Build (Guardrails)

❌ Drug name search



❌ Multi-input workflows



❌ UI dashboards, scoring logic, or repurposing claims.



12\. Definition of Technical Success

Stage 1 is successful if the system resolves valid IDs reliably via the Open Targets MCP, errors are explicit, and code is modular enough to move to Stage 2 without refactoring.



Summary (One-Line Rule): If it does not directly support ChEMBL-based drug identity resolution, it does not belong in Stage 1.

