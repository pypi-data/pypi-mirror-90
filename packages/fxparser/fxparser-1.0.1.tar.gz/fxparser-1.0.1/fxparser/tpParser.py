import spacy
import json
from .baseParser import BaseParser
from spacy.matcher import Matcher


class TPParser(BaseParser):
    def __init__(self):
        super().__init__()
        self.matcher = Matcher(self.nlp.vocab)
        pattern = [{"LOWER": {"IN": ["tp", "t/p"]}},
                   {"ORTH": {"IN": [":", " ", "@"]}, "OP": "*"}, {"LIKE_NUM": True}]
        pattern2 = [{"LOWER": "take"}, {"LOWER": "profit"},
                    {"ORTH": {"IN": [":", " ", "@"]}, "OP": "*"}, {"LIKE_NUM": True}]
        self.matcher.add("TP", None, pattern)
        self.matcher.add("TP", None, pattern2)

    def parse_text(self,text):
        self.doc = self.nlp(text)
        self.matches = self.matcher(self.doc)
        if self.debug:
            self.print_result()
        tps = []
        for _, start, end in self.matches:
            span = self.doc[start:end]  # The matched span
            tps.append(span[-1].text)
        return tps
