import uuid

class IdGenerator:
    def make_id(self) -> int:
        return uuid.uuid4().int