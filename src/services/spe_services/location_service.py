from src.data.dao.location_dao import LocationDAO
from src.data.models import Location
from src.api.schemas.location import LocationCreate
import uuid

class LocationService:
    def __init__(self, location_dao : LocationDAO):
        self.location_dao = location_dao

    def create_location(
        self,
        location_create : LocationCreate
    ) -> Location:
        """
        Create a new Location.
        """
        if not location_create.name:
            raise ValueError("Location name is required")

        location = Location(
            name=location_create.name,
            address=location_create.address,
            location_type=location_create.location_type,
        )
        return self.location_dao.create(location)

    def get_location(self, location_id: uuid.UUID) -> Location | None:
        """
        Retrieve a Location by ID.
        """
        return self.location_dao.get_by_id(location_id)

    def list_locations(self) -> list[Location]:
        """
        Return all Locations.
        """
        return self.location_dao.list()

    def delete_location(self, location_id: uuid.UUID) -> None:
        """
        Delete a location by ID. Raises ValueError if not found.
        """
        location = self.location_dao.get_by_id(location_id)
        if not location:
            raise ValueError("Location not found")
        self.location_dao.delete(location)
