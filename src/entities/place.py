""""Place where trainer can train"""
class Place:
    """"Place where trainer can train"""
    def __init__(self, place_id: int, name: str) -> None:
        self.place_id = place_id
        self.name = name    

    def __str__(self) -> str:
        return f"{self.place_id}, name={self.name}"
