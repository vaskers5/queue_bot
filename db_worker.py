from tinydb import TinyDB, Query


class DBWorker:
    def __init__(self) -> None:
        self.local_db = TinyDB('local_db.json')
    
    