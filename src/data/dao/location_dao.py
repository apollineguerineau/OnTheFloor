from sqlalchemy.engine import Engine
import uuid

from src.data.models import Location
from src.core.database import new_session
from src.core.entities import LocationEntity



class LocationDAO:
    def __init__(self, engine: Engine):
        self.engine = engine

    def create(self, location_entity: LocationEntity) -> uuid.UUID:
        with new_session(self.engine) as session:
            model = Location(
                name=location_entity.name,
                address=location_entity.address,
                location_type=location_entity.location_type,
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            return model.id

    def get_by_id(self, location_id: uuid.UUID) -> LocationEntity | None:
        with new_session(self.engine) as session:
            model = session.get(Location, location_id)
            return model.to_entity() if model else None

    def list(self) -> list[LocationEntity]:
        with new_session(self.engine) as session:
            models = session.query(Location).all()
            return [m.to_entity() for m in models]

    def delete(self, location_id: uuid.UUID) -> None:
        with new_session(self.engine) as session:
            model = session.get(Location, location_id)
            if model:
                session.delete(model)
                session.commit()
