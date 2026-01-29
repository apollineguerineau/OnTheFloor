from src.core.database import new_engine
from src.services.spe_services.session_service import SessionService
from src.services.spe_services.block_service import BlockService
from src.services.spe_services.exercise_service import ExerciseService
from src.services.spe_services.user_service import UserService
from src.services.spe_services.location_service import LocationService
from src.services.domain_services.ownership_service import OwnershipService

from src.data.dao.block_dao import BlockDAO
from src.data.dao.exercise_dao import ExerciseDAO
from src.data.dao.session_dao import SessionDAO
from src.data.dao.location_dao import LocationDAO
from src.data.dao.user_dao import UserDAO

class Injector:
    def __init__(self) -> None:
        """Init injector for depedencies initialization"""
        self.engine = new_engine()

    def ownership_service(self) -> OwnershipService :
        return OwnershipService(session_dao=SessionDAO(self.engine), block_dao=BlockDAO(self.engine), exercise_dao=ExerciseDAO(self.engine))
    
    def location_service(self) -> LocationService:
        return LocationService(location_dao=LocationDAO(self.engine))
    
    def session_service(self) -> SessionService :
        return SessionService(session_dao=SessionDAO(self.engine), ownership_service=self.ownership_service(), location_service=self.location_service())
    
    def exercise_service(self) -> ExerciseService :
        return ExerciseService(exercise_dao=ExerciseDAO(self.engine), block_dao=BlockDAO(self.engine),ownership_service=self.ownership_service())
    
    def block_service(self) -> BlockService :
        return BlockService(block_dao=BlockDAO(self.engine), ownership_service=self.ownership_service())
    
    def user_service(self)-> UserService:
        return UserService(user_dao = UserDAO(self.engine))
    
injector = Injector()