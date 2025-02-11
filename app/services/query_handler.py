from sqlalchemy import text
from app.utils.embedding import generate_embedding
from app.utils.helpers import cosine_similarity
from app.core.logging import logger

def retrieve_context_from_pgvector(query: str, db, top_k: int = 5):
    """
    Generate an embedding for the query and run a SQL query against the
    racecard_embeddings table (using pgvector) to return the top_k closest matches.
    """
    query_embedding = generate_embedding(query)
    if not query_embedding:
        logger.error("Failed to generate embedding for the query.")
        return []

    # Use the pgvector operator (<=>) to compute the distance between vectors.
    sql = text("""
        SELECT race_id, (embedding <=> :query_embedding) AS distance
        FROM racecard_embeddings
        ORDER BY embedding <=> :query_embedding
        LIMIT :top_k
    """)
    result = db.execute(sql, {"query_embedding": query_embedding, "top_k": top_k})
    rows = result.fetchall()
    return rows

def process_query(query: str, chat_history: str, db) -> str:
    """
    Process the query by determining if we need to retrieve additional context.
    Uses the pgvector-enabled database to retrieve context and merges it with chat history.
    """
    # If no chat history, we always want to retrieve context.
    if not chat_history.strip():
        use_retrieval = True
    else:
        query_embedding = generate_embedding(query)
        history_embedding = generate_embedding(chat_history)
        similarity = cosine_similarity(query_embedding, history_embedding)
        logger.info("Cosine similarity between query and chat history: %.3f", similarity)
        use_retrieval = similarity < 0.5

    if use_retrieval:
        retrieved = retrieve_context_from_pgvector(query, db, top_k=5)
        retrieved_str = "\n".join(
            [f"Race ID: {row.race_id}, Distance: {row.distance:.3f}" for row in retrieved]
        )
        context = f"{chat_history}\nRetrieved Context:\n{retrieved_str}"
        logger.info("Using retrieval-based context.")
    else:
        context = chat_history
        logger.info("Using chat history only.")
    return context
