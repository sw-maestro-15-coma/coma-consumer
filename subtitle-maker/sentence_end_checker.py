from abc import abstractmethod


class SentenceEndChecker:
    def __init__(self):
        pass

    @abstractmethod
    def is_sentence_ended(self, sentence):
        pass
