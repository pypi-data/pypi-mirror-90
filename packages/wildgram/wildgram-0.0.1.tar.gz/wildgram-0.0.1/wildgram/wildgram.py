import regex as re
import string
import os

def wildgram(text):
    # corner case for inappropriate input
    if not isinstance(text, str):
        raise Exception("What you just gave wildgram isn't a string, mate.")
    # if its just whitespace
    if text.isspace():
        return [], []

    with open(os.path.join(os.path.dirname(__file__), 'stopwords.txt')) as stopwordsfile:
        stopwords = stopwordsfile.read().split("\n")[:-1]

    punc = [x for x in string.punctuation]
    regex = '('+"|".join(["(\s|^)"+stop+"(\s|$)" for stop in stopwords])+'|\n|[\s' + "|\\".join(punc)+ ']{'+ str(2)+',})'
    prog = re.compile(regex)

    prev = 0
    count = 0
    ranges = []
    for match in prog.finditer(text.lower(),overlapped=True):
        if match.start() > prev:
            ranges.append((prev, match.start()))
        prev = match.end()
    if len(text) > prev:
        ranges.append((prev, len(text)))

    tokens = []
    for snippet in ranges:
        tokens.append(text[snippet[0]:snippet[1]])

    return tokens, ranges
