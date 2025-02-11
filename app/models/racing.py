# app/models/racing.py
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class RaceCard(Base):
    __tablename__ = "racecards"
    
    id = Column(Integer, primary_key=True, index=True)
    race_id = Column(String, unique=True, index=True)
    course = Column(String, index=True)
    date = Column(DateTime)
    off_time = Column(String)
    race_name = Column(String)
    distance = Column(String)
    odds = Column(JSON) 
    going = Column(String)
    raw_data = Column(JSON)  

    @classmethod
    def upsert_from_api(cls, db, data: dict):
        """Parse API data and upsert racecards into the database."""
        for item in data.get("racecards", []):
            race_id = item.get("race_id")
            if not race_id:
                continue  # Skip if no race_id
            instance = db.query(cls).filter(cls.race_id == race_id).first()
            if not instance:
                instance = cls(race_id=race_id)
            instance.course = item.get("course")
            # Convert date string to datetime (assuming ISO format)
            date_str = item.get("date")
            try:
                instance.date = datetime.fromisoformat(date_str)
            except Exception:
                instance.date = datetime.utcnow()  # Fallback if parsing fails
            instance.off_time = item.get("off_time")
            instance.race_name = item.get("race_name")
            instance.distance = item.get("distance")
            instance.odds = item.get("runners")
            instance.going = item.get("going")
            instance.raw_data = item
            db.merge(instance)
        db.commit()
