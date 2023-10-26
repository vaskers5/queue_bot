""""Place where trainer can train"""
class Place:
    """"Place where trainer can train"""
    def __init__(self, place_id: int, name: str) -> None:
        self.place_id = place_id
        self.name = name    

    def __repr__(self) -> str:
        return f'Place(id={self.place_id}, name={self.name}'
