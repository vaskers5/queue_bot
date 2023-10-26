from tinydb import TinyDB, Query

from entities.trainer import Trainer
from entities.place import Place
from entities.user import User


class BotManager:
    def __init__(self):
        self.local_db = TinyDB('local_db.json')
        self.trainers_table = self.local_db.table('trainers')
        self.users_table = self.local_db.table('users')
        self.trainer_places_table = self.local_db.table('trainer_places')
        self.user_states_table = self.local_db.table('user_states')
        self.slots_table = self.local_db.table('slots')

    def add_new_trainer(self, trainer_tg_nick: str) -> Trainer:
        trainer_id = self.trainers_table._next_id
        trainer = Trainer(trainer_tg_nick)
        self.local_db.insert(id=trainer_id, tg_id=trainer_tg_nick)
        return trainer
    
    def add_new_slot(self, trainer_id: int, place_id: int, start_time: datetime, end_time: datetime) -> Slot:
        pass
    
    def get_trainer_by_tg_nick(self, tg_nick: str) -> Trainer:
        trainer_entity = self.trainers_table.get(Query().tg_id == tg_nick)
        places = self.find_trainer_places(trainer)
        trainer = Trainer(trainer_entity["id"], trainer_entity["tg_id"], places)
        return trainer
    
    def find_trainer_places(self, trainer_id) -> list[Place]:
        trainer_places = self.trainer_places_table.search(Query().trainer_id == trainer_id)
        places = [Place(place["id"], place["name"], place["latitude"], place["longitude"]) for place in trainer_places]
        return places
    
    def add_trainer_place(self, trainer_id: int, place: Place) -> None:
        self.trainer_places_table.insert(trainer_id=trainer_id, place_id=place.id, place_name=place.name)
    
    def change_current_user_state(self, chat_id: int, state: str, state_info: dict =None):
        # must change last user state
        self.user_states_table.remove(Query().chat_id == chat_id)
        self.user_states_table.insert(chat_id=chat_id, state=state, state_info=state_info)
        
    def get_current_user_state(self, chat_id: int) -> dict[str, object]:
        user_state = self.user_states_table.get(Query().chat_id == chat_id)
        return user_state
