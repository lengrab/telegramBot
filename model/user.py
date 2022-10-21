from states.state import State


class User:
    def __init__(self, id, city, state: State):
        self.id = id
        self.city = city
        self.state = state.name
        self.cached_message = None