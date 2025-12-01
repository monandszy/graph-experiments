# graph-experiments

Small pipeline to parse English into AMR, convert AMR to RDF/Turtle, optionally enhance graphs with an LLM, and upload to a GraphDB triplestore.

## Purpose

- Parse English sentences into AMR graphs using `amrlib`.
- Convert AMR (Penman) graphs into RDF (Turtle) using `rdflib`.
- Optionally call a Google GenAI model to enhance AMR graphs.
- Upload Turtle to a GraphDB HTTP endpoint.