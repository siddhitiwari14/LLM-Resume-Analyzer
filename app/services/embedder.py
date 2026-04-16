import numpy as np
import faiss
from app.core.llm import generate_embeddings


def _normalize(vec: np.ndarray) -> np.ndarray:
    """L2-normalize a vector so inner product == cosine similarity."""
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return vec / norm


def compute_similarity(resume_text: str, jd_text: str) -> float:
    """
    Compute semantic similarity between resume and job description
    using FAISS inner-product index (cosine similarity after L2 normalization).

    Returns a score in [0, 100].
    """
    resume_emb = generate_embeddings(resume_text)
    jd_emb = generate_embeddings(jd_text)

    if not resume_emb or not jd_emb:
        return 0.0

    resume_vec = _normalize(np.array(resume_emb, dtype=np.float32))
    jd_vec = _normalize(np.array(jd_emb, dtype=np.float32))

    dim = len(resume_vec)

    # Build a FAISS flat inner-product index and add the JD vector
    index = faiss.IndexFlatIP(dim)
    index.add(jd_vec.reshape(1, dim))

    # Search for the closest match to the resume vector
    distances, _ = index.search(resume_vec.reshape(1, dim), k=1)
    cosine_score = float(distances[0][0])

    # Clamp to [0, 1] then scale to [0, 100]
    cosine_score = max(0.0, min(1.0, cosine_score))
    return round(cosine_score * 100, 2)
