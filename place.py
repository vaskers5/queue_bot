import geopy



class Place:
    def __init__(self, id: int, name: str, latitude: float, longitude: float) -> None:
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.location: object = geopy.Point(latitude, longitude)
    
    def __repr__(self) -> str:
        return f'Place(id={self.id}, name={self.name}, latitude={self.latitude}, longitude={self.longitude})'
    
    def get_location(self) -> geopy.Point:
        return self.location
