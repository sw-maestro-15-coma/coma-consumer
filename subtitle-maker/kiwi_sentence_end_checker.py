from sentence_end_checker import SentenceEndChecker

from kiwipiepy import Kiwi


SENTENCE_END_TAG = ['SF', 'EF']


class KiwiSentenceEndChecker(SentenceEndChecker):
    kiwi = Kiwi()

    def is_sentence_ended(self, sentence):
        tokens = self.kiwi.tokenize(sentence)
        return tokens[-1].tag in SENTENCE_END_TAG


sentence_end_checker: SentenceEndChecker = KiwiSentenceEndChecker()
