class BreedNotFoundException(Exception):
    def __init__(self, breed_name: str) -> None:
        self.id = id
        super().__init__(f'Породы с названием {breed_name} не найдено.')
