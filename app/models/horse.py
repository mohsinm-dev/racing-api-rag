from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Horse(Base):
    __tablename__ = "horses"
    
    id = Column(Integer, primary_key=True, index=True)
    horse_id = Column(String, unique=True, index=True)
    name = Column(String)
    sire = Column(String)
    dam = Column(String)
    raw_data = Column(JSON)

    @classmethod
    def upsert_from_api(cls, db, data: dict):
        for item in data.get("search_results", []):
            horse_id = item.get("id")
            if not horse_id:
                continue
            instance = db.query(cls).filter(cls.horse_id == horse_id).first()
            if not instance:
                instance = cls(horse_id=horse_id)
            instance.name = item.get("name")
            instance.sire = item.get("sire")
            instance.dam = item.get("dam")
            instance.raw_data = item
            db.merge(instance)
        db.commit()
