import spacy
import json
from baseParser import nlp
from spacy.matcher import Matcher

matcher = Matcher(nlp.vocab)
# Add match ID "HelloWorld" with no callback and one pattern
pattern = [{"LOWER": {"IN": ["tp", "t/p"]}},
           {"ORTH": {"IN": [":", " ", "@"]}, "OP": "*"}, {"LIKE_NUM": True}]
pattern2 = [{"LOWER": "take"}, {"LOWER": "profit"},
            {"ORTH": {"IN": [":", " ", "@"]}, "OP": "*"}, {"LIKE_NUM": True}]
matcher.add("TP", None, pattern)
matcher.add("TP", None, pattern2)


def parse_text(text):
    doc = nlp(text)
    matches = matcher(doc)
    # explain(text)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        print(match_id, string_id, start, end, span.text)
        print(span[-1])
    return matches


def test():
    filename2 = "/home/test/dev/scripts/docs/emvip/emvip-8.txt"

    infile = open(filename2, 'r')
    text = infile.read()
    infile.close()
    parse_text(text)


def explain(text):
    tok_exp = nlp.tokenizer.explain(text)
    for t in tok_exp:
        print(t[1], "\t", t[0])


# test()
