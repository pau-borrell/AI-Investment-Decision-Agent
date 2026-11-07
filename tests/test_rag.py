from types import SimpleNamespace
from unittest.mock import Mock, patch
import pytest
from src.rag.retrieval import retrieve_relevant_chunks
from src.rag import slm


def test_retrieval_caps_to_collection_size_without_model_download():
    collection = Mock()
    collection.count.return_value = 1
    collection.query.return_value = {
        "ids": [["id"]], "documents": [["text"]],
        "metadatas": [[{"source": "doc"}]], "distances": [[.1]],
    }
    with patch("src.rag.retrieval.get_collection", return_value=collection),          patch("src.rag.retrieval.embed_texts", return_value=[[.1, .2]]):
        result = retrieve_relevant_chunks("risk", top_k=5)
    assert len(result) == 1
    assert collection.query.call_args.kwargs["n_results"] == 1


def test_empty_collection_avoids_embedding_download():
    collection = Mock()
    collection.count.return_value = 0
    with patch("src.rag.retrieval.get_collection", return_value=collection),          patch("src.rag.retrieval.embed_texts") as embed:
        assert retrieve_relevant_chunks("risk") == []
        embed.assert_not_called()


def test_ollama_empty_response_rejected():
    response = Mock()
    response.json.return_value = {"response": ""}
    with patch("src.rag.slm.requests.post", return_value=response):
        with pytest.raises(RuntimeError, match="malformed"):
            slm._generate_answer_ollama("Question")


def test_unsupported_backend_fails_explicitly():
    with patch.object(slm, "SLM_BACKEND", "typo"):
        with pytest.raises(ValueError, match="SLM_BACKEND"):
            slm.generate_answer("Question")
