from ai_project_health_monitor.rag.embeddings.base import EmbeddingModel


class FakeEmbeddingModel(EmbeddingModel):
    """Deterministic embedding model for unit tests."""

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[float(index), 1.0] for index, _ in enumerate(texts)]


def test_embedding_model_returns_one_vector_per_text() -> None:
    model = FakeEmbeddingModel()

    embeddings = model.embed(
        [
            "Payment API integration is blocked.",
            "Backend development is delayed.",
        ]
    )

    assert len(embeddings) == 2
    assert embeddings[0] == [0.0, 1.0]
    assert embeddings[1] == [1.0, 1.0]


def test_embedding_model_returns_empty_list_for_no_texts() -> None:
    model = FakeEmbeddingModel()

    assert model.embed([]) == []