<!-- README.md: Explains local-only financial data placement and the public sample-data boundary. -->
# Data Directory

`samples/` contains synthetic public onboarding records only.

Place team-controlled source material under these ignored directories:

```text
data/raw/          # Original PDF, DOCX, XLSX, PPTX
data/processed/    # OCR and normalized section records
data/indexes/      # Embeddings and local vector indexes
```

Do not commit financial documents merely because they are available locally. Confirm license, confidentiality, provenance, effective date, and redaction before publishing any derived dataset.
