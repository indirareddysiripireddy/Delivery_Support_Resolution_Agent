# Policy Evidence

This starter uses deterministic intent-to-document selection and returns the selected Markdown file, heading, and text excerpt as source evidence. It fails closed if the file is absent. This is intentionally not described as semantic or hybrid RAG.

A production ingestion path should validate and parse approved PDF, DOCX, text, Markdown, CSV, JSON, and HTML uploads; attach tenant/access metadata; chunk with source positions; embed; store vectors in pgvector; combine metadata-filtered dense and keyword retrieval; rerank; and validate citations against retrieved chunk IDs. Retrieved content remains untrusted and must never override system policy or authorization.