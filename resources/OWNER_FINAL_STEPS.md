# Repository Owner — Final Publishing Steps

All source-controlled participant material is prepared in GitHub.

Two actions require repository-admin / Release-upload access that the connected GitHub integration does not expose.

## 1. Make the repository public

GitHub:

**Settings → General → Danger Zone → Change repository visibility → Public**

Repository:

`Decoding-Data-Science/enec2026`

Only do this if you are comfortable making the synthetic training material publicly accessible.

## 2. Publish the two companion ZIP files

Open:

**Releases → Draft a new release**

Recommended:

- Tag: `enec-2026-final`
- Title: **ENEC 2026 Training Materials — Final**

Attach:

1. `ENEC_2026_V2_2_Data_and_PDF_Corpus.zip`
2. `ENEC_2026_Slides_and_Trainer_Materials.zip`

Suggested Release description:

> Final companion resources for the ENEC 2026 AI for Coders & Software Engineers programme.
>
> **Participant data pack:** V2.2 synthetic SQLite database + original nine A-001 RAG PDFs.
>
> **Trainer pack:** slide decks, trainer runbook and Databricks setup material.
>
> All data and documents are synthetic and for training only.

After publishing, participants can use the repository code and the Release downloads from one GitHub location.

## Verification

Compare the uploaded ZIP checksums with:

`data/SHA256SUMS.txt`

Then open the repository in a logged-out/incognito browser to verify public access.
