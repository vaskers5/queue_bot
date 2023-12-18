from datetime import datetime

from src.entities.place import Place


class Slot:
    def __init__(self,
                 id: int,
                 start_time: datetime,
                 end_time: datetime,
                 user_id: int,
                 trainer_id: int,
                 slot_type: str,
                 place_name: str,
                 place_id: int):
        self.id = id
        self.start_time = str(start_time)
        self.end_time = str(end_time)
        self.user_id = user_id
        self.place_name = place_name
        self.place_id = place_id
        self.slot_type = slot_type
        self.trainer_id = trainer_id
    
    def __dict__(self):
        return {"start_time": self.start_time, "end_time": self.end_time,
                "user_id": self.user_id, "place_id": self.place_id,
                "place_name": self.place_name, "slot_type": self.slot_type, 
                "trainer_id": self.trainer_id}
        
    def __str__(self) -> str:
        return f"{self.place_name} {self.start_time} {self.end_time}"
