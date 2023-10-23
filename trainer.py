from .place import Place


class Trainer:
    def __init__(self, id: int, tg_id: str, trainer_places: list[Place]) -> None:
        self.id = id
        self.tg_id = tg_id
        self.trainer_places = trainer_places
        
    def __repr__(self) -> str:
        return f'Trainer(id={self.id}, tg_id={self.tg_id}, trainer_places={self.trainer_places})'