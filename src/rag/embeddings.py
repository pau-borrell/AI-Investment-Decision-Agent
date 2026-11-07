
MODEL_NAME = "BAAI/bge-base-en"

_model = None


def load_embedding_model():
    global _model

    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(MODEL_NAME)

    return _model


def embed_texts(texts: list[str]):
    model = load_embedding_model()
    return model.encode(texts, convert_to_numpy=True).tolist()

def embed_chunks(chunks: list[dict], model=None):
    if model is None:
        model = load_embedding_model()

    texts = [chunk["text"] for chunk in chunks]
    return model.encode(texts, convert_to_numpy=True).tolist()