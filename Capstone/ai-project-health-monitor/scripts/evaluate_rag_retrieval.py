import json
from pathlib import Path

from qdrant_client import QdrantClient

from ai_project_health_monitor.evaluation.models.retrieval import (
    RetrievalEvaluationCase,
)
from ai_project_health_monitor.evaluation.retrieval import RetrievalEvaluator
from ai_project_health_monitor.ingestion.connectors.synthetic_document import (
    SyntheticDocumentConnector,
)
from ai_project_health_monitor.ingestion.connectors.synthetic_email import (
    SyntheticEmailConnector,
)
from ai_project_health_monitor.ingestion.connectors.synthetic_jira import (
    SyntheticJiraConnector,
)
from ai_project_health_monitor.ingestion.service import IngestionService
from ai_project_health_monitor.rag.chunking import FixedSizeChunker
from ai_project_health_monitor.rag.embeddings.bge import BGEEmbeddingModel
from ai_project_health_monitor.rag.indexing import RAGIndexer
from ai_project_health_monitor.rag.pipeline import RAGPipeline
from ai_project_health_monitor.rag.retrieval import RetrievalService
from ai_project_health_monitor.rag.vector_store.qdrant import QdrantVectorStore

PROJECT_ROOT = Path(__file__).resolve().parents[1]

JIRA_DATA = PROJECT_ROOT / "data/synthetic/jira/events.json"
EMAIL_DATA = PROJECT_ROOT / "data/synthetic/emails/events.json"
DOCUMENT_DATA = PROJECT_ROOT / "data/synthetic/documents"
GOLDEN_DATA = PROJECT_ROOT / "data/evaluation/retrieval_golden.json"

VECTOR_SIZE = 384
TOP_K = 3


def load_evaluation_cases() -> list[RetrievalEvaluationCase]:
    """Load retrieval evaluation cases from the golden dataset."""
    with GOLDEN_DATA.open(encoding="utf-8") as file:
        raw_cases = json.load(file)

    if not isinstance(raw_cases, list):
        raise ValueError("retrieval golden dataset must contain a JSON array")

    return [
        RetrievalEvaluationCase.model_validate(case)
        for case in raw_cases
    ]


def build_pipeline() -> RAGPipeline:
    """Build the real baseline RAG pipeline using in-memory Qdrant."""
    ingestion_service = IngestionService(
        connectors=[
            SyntheticJiraConnector(JIRA_DATA),
            SyntheticEmailConnector(EMAIL_DATA),
            SyntheticDocumentConnector(DOCUMENT_DATA),
        ]
    )

    embedding_model = BGEEmbeddingModel()

    vector_store = QdrantVectorStore(
        client=QdrantClient(":memory:"),
        vector_size=VECTOR_SIZE,
    )

    indexer = RAGIndexer(
        chunker=FixedSizeChunker(
            chunk_size=500,
            overlap=50,
        ),
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    retrieval_service = RetrievalService(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    return RAGPipeline(
        ingestion_service=ingestion_service,
        indexer=indexer,
        retrieval_service=retrieval_service,
    )


def main() -> None:
    """Run the baseline retrieval evaluation."""
    pipeline = build_pipeline()
    cases = load_evaluation_cases()

    project_ids = sorted(
        {case.project_id for case in cases}
    )

    indexed_chunks = 0

    for project_id in project_ids:
        indexed_chunks += pipeline.index_project(project_id)

    evaluator = RetrievalEvaluator(
        lambda query, project_id, limit: pipeline.retrieve(
            query=query,
            project_id=project_id,
            limit=limit,
        )
    )

    summary = evaluator.evaluate(
        cases=cases,
        k=TOP_K,
    )

    print("=" * 60)
    print("RAG RETRIEVAL BASELINE")
    print("=" * 60)
    print(f"Indexed chunks              : {indexed_chunks}")
    print(f"Evaluation cases            : {summary.total_cases}")
    print(f"Top K                       : {TOP_K}")
    print()
    print("POSITIVE RETRIEVAL")
    print(f"Hit Rate                    : {summary.hit_rate:.4f}")
    print(f"Mean Precision@{TOP_K}       : {summary.mean_precision_at_k:.4f}")
    print(f"Mean Recall@{TOP_K}          : {summary.mean_recall_at_k:.4f}")
    print()
    print("NEGATIVE RETRIEVAL")
    print(f"Negative cases              : {summary.negative_cases}")
    print(
        f"Negative false-positive cases: "
        f"{summary.negative_false_positive_cases}"
    )
    print()
    print("ISOLATION")
    print(f"Cross-project result count  : {summary.cross_project_result_count}")
    print("=" * 60)

    if summary.cross_project_result_count > 0:
        raise RuntimeError(
            "retrieval evaluation detected cross-project leakage"
        )


if __name__ == "__main__":
    main()