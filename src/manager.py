from tinydb import TinyDB, Query

from .entities.trainer import Trainer
from .entities.place import Place
from .entities.user import User
from .entities.slot import Slot


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
    
    def add_new_slot(self, user_id: int, start_time: str, end_time: str, place_id: int, place_name: str) -> Slot:
        last_id = self.slots_table._next_id
        slot_data = {"id": last_id, "user_id": user_id, "start_time": start_time,
                     "end_time": end_time, "place_id": place_id, "place_name": place_name}
        slot = Slot(**slot_data)
        self.slots_table.insert(slot_data)
        return slot
    
    def get_user_slots(self, user_id: int) -> list[Slot]:
        slots = self.slots_table.search(Query().user_id == user_id)
        return [Slot(**slot) for slot in slots]
    
    def get_user_places(self, user_id: int) -> list[Place]:
        user_places = self.trainer_places_table.search(Query().user_id == user_id)
        places = [Place(place["place_id"], place["place_name"]) for place in user_places]
        return places
    
    def add_user_place(self, user_id: int, place_name: str) -> Place:
        last_id = self.trainer_places_table._next_id
        self.trainer_places_table.insert({"place_id":last_id, "user_id": user_id, "place_name":place_name})
        
    def delete_user_place(self, user_id: int, place_id: int) -> None:
        self.trainer_places_table.remove(Query().user_id == user_id and Query().id == place_id)
    
    def change_current_user_state(self, chat_id: int, state: str, state_info: dict =None):
        # must change last user state
        self.user_states_table.remove(Query().chat_id == chat_id)
        self.user_states_table.insert({"chat_id": chat_id, "state":state, "state_info":state_info})
        
    def get_current_user_state(self, chat_id: int) -> dict[str, object]:
        user_state = self.user_states_table.get(Query().chat_id == chat_id)
        return user_state
