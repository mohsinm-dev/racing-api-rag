from app.core.scheduler import ingestion_job
from app.core.logging import logger

if __name__ == "__main__":
    logger.info("Manually triggering ingestion job...")
    ingestion_job()
    logger.info("Ingestion job completed.")
