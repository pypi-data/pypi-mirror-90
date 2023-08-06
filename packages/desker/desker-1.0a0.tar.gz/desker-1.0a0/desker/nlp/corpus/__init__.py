import nltk
import re
import os


def build_stopwords():
    stopwords = nltk.corpus.stopwords.words("french")
    stopwords_file = (
        f"{ os.path.dirname(os.path.abspath(__file__))}/stopwords/french.txt"
    )
    with open(stopwords_file) as f:
        lines = f.readlines()
        stopwords.extend([l.rstrip().lower() for l in lines])
        stopwords = list(set(stopwords))
    return stopwords


def build_stopwords_regex():
    _regex_list = [r"\b" + word + r"(?![\w-])" for word in stopwords]
    return re.compile("(?u)" + "|".join(_regex_list), re.IGNORECASE)


stopwords = build_stopwords()
stopwords_regex = build_stopwords_regex()

pos_file = f"{ os.path.dirname(os.path.abspath(__file__))}/pos/french.tagger"
stanford_tagger_jar = (
    f"{ os.path.dirname(os.path.abspath(__file__))}/pos/stanford-postagger.jar"
)
__all__ = ["stopwords"]
