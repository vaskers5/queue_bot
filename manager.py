from tinydb import TinyDB, Query

from trainer import Trainer
from place import Place
from user import User


class BotManager:
    def __init__(self):
        self.local_db = TinyDB('local_db.json')
        self.trainers_table = self.local_db.table('trainers')
        self.users_table = self.local_db.table('users')
        self.places_table = self.local_db.table('places')
        self.trainer_places_table = self.local_db.table('trainer_places')

    def add_new_trainer(self, trainer_tg_nick: str) -> Trainer:
        trainer_id = self.trainers_table._next_id
        trainer = Trainer(trainer_tg_nick)
        self.local_db.insert(id=trainer_id, tg_id=trainer_tg_nick)
        return trainer
    
    def get_trainer_by_tg_nick(self, tg_nick: str) -> Trainer:
        trainer_entity = self.trainers_table.get(Query().tg_id == tg_nick)
        places = self.find_trainer_places(trainer)
        trainer = Trainer(trainer_entity["id"], trainer_entity["tg_id"], places)
        return trainer
    
    def find_trainer_places(self, trainer_id) -> list[Place]:
        trainer_places = self.trainer_places_table.search(Query().trainer_id == trainer_id)
        places = [Place(place["id"], place["name"], place["latitude"], place["longitude"]) for place in trainer_places]
        return places
    
    