class ObjectIDNotFoundException(Exception):
    def __init__(self, id: int) -> None:
        self.id = id
        super().__init__(f'Объекта с id {id} не найдено.')
