class User:
    def __init__(self, id: int, tg_id: str) -> None:
        self.id = id
        self.tg_id = tg_id
    
    def __repr__(self) -> str:
        return f'User(id={self.id}, tg_id={self.tg_id})'
    