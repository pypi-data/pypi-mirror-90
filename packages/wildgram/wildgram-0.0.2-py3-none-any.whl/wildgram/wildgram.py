import regex as re
import string
import os

STOPWORDS = [
"no",
"with",
"and",
"or",
"on",
"due to",
"secondary to",
"s/p",
"as well as",
"was",
"from",
"when",
"for",
"vs",
"without",
"ruled out",
"in",
"came back",
"who",
"had",
"at",
"but",
"though",
"verses",
"to",
"the",
"could",
"w/o",
"c/b",
"complicated by",
"experience",
"become",
"becomes",
"if",
"including",
"indicate",
"since",
"towards",
"toward",
"out",
"you",
"your",
"by",
"developed",
"develop",
"described",
"describe",
"denies",
"denied",
"suggests",
"suggest",
"suggested",
"is",
"status",
"are",
"represented",
"represent",
"that",
"in the",
"been",
"be",
"a"
]

def wildgram(text):
    # corner case for inappropriate input
    if not isinstance(text, str):
        raise Exception("What you just gave wildgram isn't a string, mate.")
    # if its just whitespace
    if text.isspace():
        return [], []

    punc = [x for x in string.punctuation]
    regex = '('+"|".join(["(\s|^)"+stop+"(\s|$)" for stop in STOPWORDS])+'|\n|[\s' + "|\\".join(punc)+ ']{'+ str(2)+',})'
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
