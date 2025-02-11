from app.core.logging import logger
from app.models.racing import RaceCard
from app.core.database import SessionLocal
from app.services.racing_api_client import RacingAPIClient

def ingest_racecards(db):
    client = RacingAPIClient()
    logger.info("Fetching racecards data...")
    data = client.racecards_standard({"day": "today"})
    RaceCard.upsert_from_api(db, data)

def ingest_courses(db):
    client = RacingAPIClient()
    logger.info("Fetching courses data...")
    from app.models.course import Course
    data = client.list_courses()
    Course.upsert_from_api(db, data)

def ingest_horses(db):
    client = RacingAPIClient()
    logger.info("Fetching horses data...")
    from app.models.horse import Horse
    horse_names = ["Constitution Hill", "Another Horse"]
    for name in horse_names:
        data = client.search_horses(name)
        Horse.upsert_from_api(db, data)

def ingest_jockeys(db):
    client = RacingAPIClient()
    logger.info("Fetching jockeys data...")
    from app.models.jockey import Jockey
    jockey_names = ["Jockey One", "Jockey Two"]
    for name in jockey_names:
        data = client.search_jockeys(name)
        Jockey.upsert_from_api(db, data)

def ingest_trainers(db):
    client = RacingAPIClient()
    logger.info("Fetching trainers data...")
    from app.models.trainer import Trainer
    trainer_names = ["Trainer One", "Trainer Two"]
    for name in trainer_names:
        data = client.search_trainers(name)
        Trainer.upsert_from_api(db, data)

def ingest_owners(db):
    client = RacingAPIClient()
    logger.info("Fetching owners data...")
    from app.models.owner import Owner
    owner_names = ["Owner One", "Owner Two"]
    for name in owner_names:
        data = client.search_owners(name)
        Owner.upsert_from_api(db, data)

def full_ingestion_job():
    logger.info("Starting full ingestion job...")
    db = SessionLocal()
    try:
        ingest_racecards(db)
        ingest_courses(db)
        ingest_horses(db)
        ingest_jockeys(db)
        ingest_trainers(db)
        ingest_owners(db)
        logger.info("Full ingestion job completed successfully.")
    except Exception as e:
        logger.error("Error during full ingestion job: %s", e)
        db.rollback()
    finally:
        db.close()
