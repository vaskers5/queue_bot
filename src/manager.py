from tinydb import TinyDB, Query

from typing import Optional

from .entities.trainer import Trainer
from .entities.place import Place
from .entities.user import User
from .entities.slot import Slot


class BotManager:
    def __init__(self):
        self.local_db = TinyDB('local_db.json')
        self.trainers_table = self.local_db.table('trainers')
        self.users_table = self.local_db.table('users')
        self.user_trainer_table = self.local_db.table('user_trainer')
        self.trainer_places_table = self.local_db.table('trainer_places')
        self.user_states_table = self.local_db.table('user_states')
        self.slots_table = self.local_db.table('slots')

    def add_new_trainer(self, trainer_tg_nick: str) -> bool:
        # Check if the trainer already exists
        trainer = self.trainers_table.get(Query().tg_id == trainer_tg_nick)
        if trainer:
            return False
        trainer_id = self.trainers_table._next_id
        self.trainers_table.insert({"id": trainer_id, "tg_id": trainer_tg_nick})
        return True

    
    def add_new_slot(self, user_id: int, start_time: str, end_time: str,
                     place_id: int, place_name: str, trainer_nickname: str,
                     slot_type: str="free", user_nickname: Optional[str]=None) -> Slot:
        last_id = self.slots_table._next_id
        slot_data = {"id": last_id, "user_id": user_nickname, "start_time": start_time,
                     "end_time": end_time, "place_id": place_id, "place_name": place_name,
                     "slot_type": slot_type, "user_nickname": user_nickname,
                     "trainer_nickname": trainer_nickname,
                     "trainer_id": user_id, "slot_type": slot_type} 
        slot = Slot(**slot_data)
        self.slots_table.insert(slot_data)
        return slot
    
    def get_user_slots(self, trainer_nick: str) -> list[Slot]:
        slots = self.slots_table.search(Query().trainer_nickname == trainer_nick)
        return [Slot(**slot) for slot in slots]
    
    def get_trainer_places(self, user_id: int) -> list[Place]:
        user_places = self.trainer_places_table.search(Query().user_id == user_id)
        places = [Place(place["place_id"], place["place_name"]) for place in user_places]
        return places
    
    def add_trainer_place(self, user_id: int, place_name: str) -> None:
        last_id = self.trainer_places_table._next_id
        if last_id is None:
            last_id = 1
        self.trainer_places_table.insert({"place_id":last_id, "user_id": user_id, "place_name":place_name})
        
    def get_user_trainer(self, user_nick: str) -> list[str]:
        user_trainers = self.user_trainer_table.search(Query().user_nick == user_nick)
        trainers = [trainer["trainer_nick"] for trainer in user_trainers]
        return trainers
    
    def add_user_trainer(self, user_nick: str, trainer_nick: str) -> str:
        trainer_id = self.trainers_table.get(Query().tg_id == trainer_nick)
        if not trainer_id:
            return "Такого тренера нет в базе данных!"
        else:
            # check if user already has the same trainer. User can have more then one trainer
            user_trainers = self.user_trainer_table.search(Query().user_id == user_nick)
            if trainer_id in user_trainers:
                return "Вы уже привязаны к этому тренеру!"
            else:
                self.user_trainer_table.insert({"user_nick": user_nick, "trainer_nick": trainer_nick})
                return "Тренер успешно добавлен!"
    
    def delete_user_trainer(self, user_nick: str, trainer_nick: str) -> str:
        trainer_id = self.trainers_table.get(Query().tg_id == trainer_nick)
        if not trainer_id:
            return "Такого тренера нет в базе данных!"
        else:
            # check if user already has the same trainer. User can have more then one trainer
            user_trainers = self.user_trainer_table.search(Query().user_nick == user_nick)
            if trainer_id in user_trainers:
                self.user_trainer_table.remove(Query().user_nick == user_nick and Query().trainer_nick == trainer_nick)
                return "Тренер успешно удален!"
            else:
                return "Вы не записаны к этому тренеру"


    def get_trainer_clients(self, trainer_nick: str) -> list[str]:
        trainer_id = self.trainers_table.get(Query().tg_id == trainer_nick)
        if trainer_id:
            user_trainers = self.user_trainer_table.search(Query().trainer_nick == trainer_nick)
            clients = [user["user_nick"] for user in user_trainers]
            return clients
        else:
            return []

        
    def add_new_user(self, user_id: int, user_tg_nick: str) -> User:
        user = User(user_id, user_tg_nick)
        self.users_table.insert({"user_id": user_id, "tg_nick": user_tg_nick})
        return user
        
    def delete_user_place(self, user_id: int, place_id: int) -> None:
        self.trainer_places_table.remove(Query().user_id == user_id and Query().place_id == place_id)
    
    def change_current_user_state(self, chat_id: int, state: str, state_info: dict =None):
        # must change last user state
        self.user_states_table.remove(Query().chat_id == chat_id)
        self.user_states_table.insert({"chat_id": chat_id, "state":state, "state_info":state_info})
        
    def get_current_user_state(self, chat_id: int) -> dict[str, object]:
        user_state = self.user_states_table.get(Query().chat_id == chat_id)
        return user_state
    
    def get_trainer_slots(self, trainer_nick: str) -> list[Slot]:
        slots = self.slots_table.search(Query().trainer_nickname == trainer_nick)
        slots = list(filter(lambda slot: slot["slot_type"] == "free", slots))
        return [Slot(**slot) for slot in slots]


    def check_trainer(self, trainer_nick: str, user_nick: str) -> bool:
        user_trainer = self.user_trainer_table.get(Query().user_nick == user_nick and Query().trainer_nick == trainer_nick)
        if user_trainer:
            return True
        else:
            return False
    
    def add_user_to_slot(self, user_tg: str, slot: dict[str, str]) -> None:
    # Check if the user has a trainer
        user_trainer = self.user_trainer_table.get(Query().user_nick == user_tg)
        if not user_trainer:
            raise ValueError("User has no trainer yet.")

        # Check if the slot is free
        if slot["slot_type"] != "free":
            raise ValueError("The slot is not free.")
        print(slot)
        # Update the slot's status
        self.slots_table.update({"slot_type": "reserved"}, Query().id == slot["id"])

        # Add the user to the slot
        self.slots_table.update({"user_nickname": user_tg}, Query().id == slot["id"])


    def get_user_booked_slots(self, user_tg: str) -> list[dict[str, str]]:
        # Get the user's booked slots
        slots = self.slots_table.search(Query().user_nickname == user_tg and Query().slot_type == "reserved")
        # Return a list of Slot objects
        return slots

    def cancel_booking(self, slot_data):
        # Update the slot's status
        self.slots_table.update({"slot_type": "free"}, Query().user_nickname == slot_data["user_nickname"] and Query().start_time == slot_data["start_time"] and  Query().trainer_nickname == slot_data["trainer_nickname"])

    def find_trainer_nick_for_user(self, user_nick: str) -> Optional[str]:
        trainer_entry = self.user_trainer_table.get(Query().user_nick == user_nick)
        if trainer_entry:
            return trainer_entry.get('trainer_nick')
        return None
