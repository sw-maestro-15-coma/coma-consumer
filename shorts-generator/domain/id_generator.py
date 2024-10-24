import uuid

class IdGenerator:
    @staticmethod
    def make_id() -> int:
        return uuid.uuid4().int