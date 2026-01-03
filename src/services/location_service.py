from sqlalchemy.orm import Session
from src.data.dao.location_dao import LocationDAO
from src.data.models import Location


class LocationService:
    def __init__(self, db: Session):
        self.dao = LocationDAO(db)

    def create_location(
        self,
        *,
        name: str,
        address: str | None = None,
        location_type: str = "none",
    ) -> Location:
        """
        Create a new Location.

        :param name: Name of the location (required)
        :param address: Optional address
        :param location_type: Type of location ("crossfit", "gym", "none")
        :return: persisted Location object
        """
        if not name:
            raise ValueError("Location name is required")

        location = Location(
            name=name,
            address=address,
            location_type=location_type,
        )
        return self.dao.create(location)

    def get_location(self, location_id: int) -> Location | None:
        """
        Retrieve a Location by ID.
        """
        return self.dao.get_by_id(location_id)

    def list_locations(self) -> list[Location]:
        """
        Return all Locations.
        """
        return self.dao.list()

    def delete_location(self, location_id: int) -> None:
        """
        Delete a location by ID. Raises ValueError if not found.
        """
        location = self.dao.get_by_id(location_id)
        if not location:
            raise ValueError("Location not found")
        self.dao.delete(location)
