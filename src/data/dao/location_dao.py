from sqlalchemy.orm import Session
from src.data.models import Location


class LocationDAO:
    def __init__(self, db: Session):
        self.db = db

    def create(self, location: Location) -> Location:
        """
        Persist a new Location in the database.
        """
        self.db.add(location)
        self.db.commit()
        self.db.refresh(location)
        return location

    def get_by_id(self, location_id: int) -> Location | None:
        """
        Retrieve a Location by its primary key.
        """
        return self.db.query(Location).filter(Location.id == location_id).first()

    def list(self) -> list[Location]:
        """
        List all Locations in the database.
        """
        return self.db.query(Location).all()
    
    def delete(self, location: Location) -> None:
        """
        Delete a Location from the database.
        """
        self.db.delete(location)
        self.db.commit()
