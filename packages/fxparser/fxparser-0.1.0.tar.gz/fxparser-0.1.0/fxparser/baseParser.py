from spacy.lang.en import English
import re
from spacy.tokenizer import Tokenizer


class BaseParser:
    def __init__(self):
        self.debug = False
        self.nlp = English()
        self.matches = []
        self.doc = None

        self.prefix_re = re.compile(r'''^[\[("']''')
        self.suffix_re = re.compile(r'''[\])"']$''')
        self.infix_re = re.compile(r'''[-~@:]''')

        def custom_tokenizer(self):
            return Tokenizer(self.nlp.vocab,
                             prefix_search=self.prefix_re.search,
                             suffix_search=self.suffix_re.search,
                             infix_finditer=self.infix_re.finditer)
        self.nlp.tokenizer = custom_tokenizer(self)

    def parse_text(self):
        raise Exception("parse_text is not implemented")

    def print_result(self):
        for match_id, start, end in self.matches:
            # Get string representation
            string_id = self.nlp.vocab.strings[match_id]
            span = self.doc[start:end]  # The matched span
            print(match_id, string_id, start, end, span.text)
