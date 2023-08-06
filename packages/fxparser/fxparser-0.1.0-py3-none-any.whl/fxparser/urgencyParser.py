import spacy
import json
from baseParser import nlp
from spacy.matcher import PhraseMatcher

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(name) for name in ["now", "instant"]]

matcher.add("Urgency", None, *patterns)

def parse_text(text):
    doc = nlp(text)
    matches = matcher(doc)
    for match_id, start, end in matches:
        string_id = nlp.vocab.strings[match_id]  # Get string representation
        span = doc[start:end]  # The matched span
        print(match_id, string_id, start, end, span.text)
    return matches


def test() :
    filename2 = "/home/test/dev/scripts/docs/emvip/emvip-8.txt"

    infile = open(filename2, 'r')
    text = infile.read()
    infile.close()
    parse_text(text)
    