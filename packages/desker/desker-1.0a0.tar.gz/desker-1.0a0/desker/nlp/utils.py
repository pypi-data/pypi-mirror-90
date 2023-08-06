import re
from typing import List

from nltk.stem.snowball import SnowballStemmer
from nltk.tag.stanford import StanfordPOSTagger

from desker.nlp.corpus import (pos_file, stanford_tagger_jar, stopwords)

SENTENCE_DELIMITERS = re.compile(
    r'[\.…⋯‹«›»,;:¡!¿\?\\"“”\[\]\(\)⟨⟩}{&]'  # punctuation signs
    r"|\s[-–~]+\s"  # dash between spaces
)


def remove_stopwords(tokens: List[str]) -> List[str]:
    return [t for t in tokens if t.lower() not in stopwords]


def stem_sentence(sentence: str, lang: str = "french") -> str:
    # TODO: multilang
    stemmer = SnowballStemmer(lang)
    word_stems = [stemmer.stem(word) for word in sentence.split()]
    return " ".join(word_stems)


def tag_tokens(sentence: str) -> str:
    # TODO: multilang
    tagger = StanfordPOSTagger(pos_file, stanford_tagger_jar, encoding="utf8")
    return tagger.tag(sentence)


def tokenize(text: str, lower=False) -> List[str]:
    """Convert a text to a list of words.
    """
    word_regex = re.compile(r"(?u)\W+")
    words = []
    for word in word_regex.split(text):
        words.append(word.strip())
    if lower:
        words = [w.lower() for w in words]
    return list(filter(None, words))


def split_text_by_delimiters(text: str) -> List[str]:
    """Split a given text using delimiters.
    """
    sentences = SENTENCE_DELIMITERS.split(text)
    return [s for s in sentences if s]


def split_text_by_stopwords(text: str, lang: str = "fr") -> List[str]:
    """Split a given text using stopwords.
    """
    # TODO: multilang
    sentences = []
    sentence = []
    for word in tokenize(text):
        if word in stopwords:
            if sentence:
                sentences.append(" ".join(sentence))
            sentence = []
        else:
            sentence.append(word)
    if sentence:
        sentences.append(" ".join(sentence))
    return sentences
