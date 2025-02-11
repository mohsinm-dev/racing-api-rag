from app.core.database import SessionLocal
from app.models.racing import RaceCard
from app.models.embedding import RaceCardEmbedding
from app.utils.embedding import generate_embedding
from app.core.logging import logger

def vectorize_new_racecards():
    """
    Query all RaceCard records and, for each record that does not have an embedding in
    the RaceCardEmbedding table, generate an embedding and insert it.
    """
    logger.info("Starting vectorization job using pgvector...")
    db = SessionLocal()
    try:
        racecards = db.query(RaceCard).all()
        count = 0
        for rc in racecards:
            # Check if an embedding already exists for this racecard
            existing = db.query(RaceCardEmbedding).filter(RaceCardEmbedding.race_id == rc.race_id).first()
            if existing:
                continue

            # Create a summary text (adjust as needed)
            text = f"{rc.race_name} at {rc.course}"
            embedding = generate_embedding(text)
            if embedding:
                new_embedding = RaceCardEmbedding(
                    race_id=rc.race_id,
                    embedding=embedding
                )
                db.add(new_embedding)
                count += 1
        db.commit()
        logger.info("Vectorization job completed. Vectorized %d new racecards.", count)
    except Exception as e:
        logger.error("Error during vectorization job: %s", e)
        db.rollback()
    finally:
        db.close()
