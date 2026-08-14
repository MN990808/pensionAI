<!-- DATA_GOVERNANCE.md: Defines how pension documents are classified, versioned, transformed, and kept out of public Git. -->
# Data Governance v1

## Repository Policy

Raw PDF, DOCX, XLSX, PPTX, OCR output, embeddings, indexes, account exports, and credentials remain outside Git. The public repository stores schemas, synthetic samples, ingestion code, and manifests without proprietary content.

## Knowledge Layers

| Layer | Examples | Retrieval behavior |
|---|---|---|
| Law/regulation | Statute and official guidance | Highest authority; effective-date filter |
| Institutional operations | Approved manuals and forms | Scope to institution and process date |
| Explanatory FAQ | Curated customer explanations | Use when consistent with higher authority |
| Product documents | Investment prospectuses | Key by product code and latest effective version |
| Synthetic sample | Repository examples | Never support production financial claims |

## Required Metadata

- `document_id`
- `title`
- `source_type`
- `authority_level`
- `published_at`
- `effective_from` and optional `effective_to`
- `product_code` when applicable
- `page_or_section`
- `source_uri` or controlled local locator
- `content_hash`
- `supersedes` and `superseded_by`

## Ingestion Rules

- OCR and extracted text must retain page boundaries.
- Chunk by semantic section before applying token limits.
- Tables are normalized separately from prose.
- Duplicate versions are detected by hash and product/date keys.
- Conflicts are recorded rather than silently overwritten.
- An ingestion run produces an auditable manifest and validation report.
