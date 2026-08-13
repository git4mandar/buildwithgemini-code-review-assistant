import vertexai
from vertexai.preview import rag
from vertexai.preview.rag.utils import resources as rr

PROJECT_ID = "qwiklabs-gcp-04-71f8c49abd0b"
LOCATION = "us-central1"
GCS_PATH = "gs://code-review-assistant-assets-qwiklabs-gcp-04-71f8c49abd0b/rag/code_review_pr_guidelines.md"

PARSING_PROMPT = (
    "Extract all code review principles, pull request rules, style guides, and security guidelines. "
    "Output clean, self-contained prose."
)

def create_rag_corpus():
    print(f"Initializing Vertex AI RAG Engine for project={PROJECT_ID}, location={LOCATION}...")
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    cfg = f"projects/{PROJECT_ID}/locations/{LOCATION}/ragEngineConfig"
    rag.update_rag_engine_config(
        rag_engine_config=rag.RagEngineConfig(
            name=cfg,
            rag_managed_db_config=rag.RagManagedDbConfig(mode=rr.Serverless()),
        )
    )

    print("Creating serverless RAG corpus...")
    corpus = rag.create_corpus(
        display_name="code-review-pr-guidelines-corpus",
        embedding_model_config=rag.EmbeddingModelConfig(
            publisher_model="publishers/google/models/text-embedding-005"
        ),
    )
    print(f"RAG Corpus Created! Name: {corpus.name}")

    print(f"Importing files from {GCS_PATH}...")
    resp = rag.import_files(
        corpus_name=corpus.name,
        paths=[GCS_PATH],
        transformation_config=rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(chunk_size=512, chunk_overlap=100)
        ),
        llm_parser=rag.LlmParserConfig(
            model_name="gemini-2.5-flash",
            custom_parsing_prompt=PARSING_PROMPT,
        ),
    )
    print(f"Import complete! Imported files count: {resp.imported_rag_files_count}")
    return corpus.name

if __name__ == "__main__":
    corpus_name = create_rag_corpus()
    print("Corpus Resource Name:", corpus_name)
