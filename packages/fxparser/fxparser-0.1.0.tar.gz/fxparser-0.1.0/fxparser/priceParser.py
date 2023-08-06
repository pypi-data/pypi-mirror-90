import spacy
import json
from baseParser import nlp
from spacy.matcher import Matcher

matcher = Matcher(nlp.vocab)
# Add match ID "HelloWorld" with no callback and one pattern
pattern = [{"LIKE_NUM": True}]

matcher.add("Price", None, pattern)


def parse_text(text, tps, sl):
    doc = nlp(text)
    matches = matcher(doc)
    prices = []
    # explain(text)
    for _, start, end in matches:
        span = doc[start:end]  # The matched span
        prices.append(span.text)
    for price in tps:
        if price in prices: prices.remove(price) 
    if sl in prices: prices.remove(sl)
    print(prices)
    return matches


def test():
    filename2 = "/home/test/dev/scripts/docs/emvip/emvip-8.txt"

    infile = open(filename2, 'r')
    text = infile.read()
    infile.close()
    parse_text(text, ['1.2279', '1.2305'], '1.2342')


def explain(text):
    tok_exp = nlp.tokenizer.explain(text)
    for t in tok_exp:
        print(t[1], "\t", t[0])


test()
