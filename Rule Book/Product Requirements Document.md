\# 📄 Product Requirements Document (PRD)



\*\*Project Name\*\*

S.A.F.E.R (Safety-Aware Framework for Drug Repurposing)



\*\*Stage\*\*: Foundation Build (ChEMBL-first)



---



\### Executive Summary \& Business Context



Drug repurposing accelerates therapeutic discovery by identifying new disease indications for existing drugs. While platforms like Open Targets provide rich datasets, there is no streamlined, safety-aware workflow that begins from a validated drug entity and progressively builds repurposing insight.



S.A.F.E.R aims to fill this gap by creating a modular, interpretable, and safety-aware drug repurposing tool. This PRD defines Stage 1, which establishes the drug identity layer using ChEMBL IDs as the canonical entry point. This foundation is critical: every downstream biological inference depends on correct drug identity resolution.



---



\### Problem Statement



Current repurposing workflows suffer from:



\* Ambiguous drug naming (synonyms, formulations)

\* Inconsistent identifiers across datasets

\* Lack of validation before downstream analysis

\* High risk of propagating early errors into biological conclusions



Without a validated drug object, repurposing analysis becomes unreliable and difficult to defend in scientific or platform contexts.



---



\### Objectives



\*\*Primary Objective\*\*



\* Build a robust ChEMBL-based drug identity resolver using the Open Targets Model Context Protocol (MCP) as the foundation for the S.A.F.E.R pipeline.



\*\*Secondary Objectives\*\*



\* Ensure native compatibility with Open Targets Platform datasets through MCP integration.

\* Enable modular expansion in later stages (MoA, targets, diseases, safety).

\* Maintain interpretability and reproducibility.



---



\### In-Scope vs Out-of-Scope



\*\*✅ In Scope (Stage 1)\*\*



\* \*\*Input\*\*: ChEMBL ID validation using regex `CHEMBL\[0-9]+`.

\* \*\*Data Sourcing\*\*: Use of Open Targets MCP for real-time drug identity resolution.

\* \*\*Metadata Retrieval\*\*: Fetching core drug metadata (name, type, status).

\* \*\*Standardized Output\*\*: Deterministic JSON output.

\* \*\*Error Handling\*\*: Explicit messaging for invalid formats or non-existent IDs.



\*\*❌ Out of Scope (Explicit)\*\*



\* Drug name search, target identification, or mechanism of action analysis.

\* Disease prioritization or safety scoring.

\* Frontend UI or Machine Learning models.



---



\### Stakeholders



\*\*Primary Stakeholders\*\*



\* Computational biology developers

\* Bioinformatics researchers

\* Hackathon evaluators



\*\*Secondary Stakeholders\*\*



\* Open Targets platform contributors

\* Drug discovery researchers



---



\### User Personas



\*\*Persona 1: Researcher\*\*



\* Familiar with ChEMBL IDs and needs reliable programmatic drug validation.



\*\*Persona 2: Hackathon Judge\*\*



\* Evaluates scientific rigor and looks for clean scope boundaries and modularity.



---



\### User Stories \& Acceptance Criteria



\*\*User Story 1\*\*

As a user, I want to input a ChEMBL ID and receive a validated drug profile via the Open Targets MCP so that I can confidently use it for downstream analysis.



\*\*Acceptance Criteria\*\*



\* Given a valid ChEMBL ID, the system returns structured drug metadata.

\* Given an invalid ChEMBL ID, the system returns a clear error.

\* System successfully connects to and queries the Open Targets MCP server.



---



\### Functional Requirements



\* \*\*FR-1: Input Validation\*\*: Accept ChEMBL IDs in the format `CHEMBL\[0-9]+` and reject malformed inputs.

\* \*\*FR-2: Drug Resolution\*\*: Query the Open Targets MCP to confirm drug existence and resolve entity details.

\* \*\*FR-3: Metadata Extraction\*\*: Retrieve ChEMBL ID, drug name, drug type, and clinical/approval status.

\* \*\*FR-4: Output Format\*\*: Return data in a deterministic JSON structure with no UI dependency.



---



\### Non-Functional Requirements



\* \*\*Lightweight\*\*: No persistent storage or databases.

\* \*\*API-First\*\*: Designed for programmatic access and "vibe coding" workflows.

\* \*\*Modular Architecture\*\*: Clear separation between validation, resolution, and parsing logic.

\* \*\*Context-Aware\*\*: Leverages MCP for native understanding of the Open Targets data schema.



---



\### Technical Specifications



\*\*Architecture\*\*



\* Standalone Python-based backend module.

\* Integration with \*\*Open Targets Model Context Protocol (MCP)\*\* for data fetching.



\*\*Data Model (Stage 1)\*\*



```json

{

&nbsp; "chembl\_id": "string",

&nbsp; "drug\_name": "string",

&nbsp; "drug\_type": "string",

&nbsp; "clinical\_status": "string | null"

}



```



\*\*External Dependencies\*\*



\* Open Targets MCP Server (`mcp.platform.opentargets.org/mcp`)

\* Python libraries: `requests` or `mcp-sdk`.



---



\### Edge Cases \& Error Handling



\* \*\*Invalid Format\*\*: Immediate rejection with a descriptive message.

\* \*\*ID Not Found\*\*: Explicit "not found" response from MCP.

\* \*\*MCP/API Failure\*\*: Graceful handling of timeouts or service unavailability.



---



\### Success Metrics \& KPIs



\* 100% valid ChEMBL IDs resolve correctly via MCP.

\* Zero hardcoded drug records within the repository.

\* Clean extensibility into Stage 2 (Drug → Target).



---



\### Risks \& Mitigation



\* \*\*Risk\*\*: MCP connectivity issues. \*\*Mitigation\*\*: Implement robust error handling and status checks.

\* \*\*Risk\*\*: Scope creep. \*\*Mitigation\*\*: Strict adherence to "vibe coding" rules in `todo.md`.



---



\### Implementation Timeline (Stage 1)



\* \*\*Day 1\*\*: PRD update + Cursor MCP configuration.

\* \*\*Day 2\*\*: Implementation of `validator.py` and MCP-based `resolver.py`.

\* \*\*Day 3\*\*: Response parsing and unified `app.py` orchestration.

\* \*\*Day 4\*\*: Manual verification and Stage 1 completion.



---



\### Future Roadmap



\* \*\*Stage 2\*\*: Drug → Mechanism → Target (via MCP)

\* \*\*Stage 3\*\*: Target → Disease prioritization

\* \*\*Stage 4\*\*: Safety-aware scoring

\* \*\*Stage 5\*\*: UI integration



---



\### Summary



S.A.F.E.R Stage 1 establishes a validated, MCP-integrated ChEMBL drug identity layer, forming the essential foundation for a modular, safety-aware drug repurposing platform.



---



\*\*Would you like me to generate the Cursor configuration JSON so you can connect the Open Targets MCP and start coding?\*\*

