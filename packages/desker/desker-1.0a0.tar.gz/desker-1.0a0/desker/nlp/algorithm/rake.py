import operator
from collections import defaultdict
from typing import Dict, List

from desker.nlp import utils
from desker.nlp.corpus import stopwords


class Rake:
    """Implements the Rapid Automatic Keyword Extraction

    see. https://www.researchgate.net/publication/227988510_Automatic_Keyword_Extraction_from_Individual_Documents
    """

    def __init__(self, max_words=3, min_characters=2, lang=None):
        # TODO: multilang
        self.lang = "fr"
        self.max_words = max_words
        self.min_characters = min_characters
        self.stop_words = stopwords

    def _generate_keywords(self, text: str) -> List[str]:
        sentences = utils.split_text_by_delimiters(text)
        keywords = []
        for sentence in sentences:
            keywords.extend(utils.split_text_by_stopwords(sentence))

        def _filter(keyword):
            if len(keyword) < self.min_characters:
                return False
            if len(utils.tokenize(keyword)) > self.max_words:
                return False
            return True

        return list(filter(_filter, keywords))

    @staticmethod
    def _calculate_word_score(keywords: List[str]):
        word_frequency = defaultdict(int)
        word_degree = defaultdict(int)
        word_score = defaultdict(int)

        for keyword in keywords:
            words = utils.tokenize(keyword)
            words_degree = len(words) - 1

            for word in words:
                word_frequency[word] += 1
                word_degree[word] += words_degree

        for word in word_frequency:
            word_degree[word] = word_degree[word] + word_frequency[word]

        for word in word_frequency:
            word_score[word] = word_degree[word] / word_frequency[word]

        return word_score

    @staticmethod
    def _calculate_keyword_score(candidates: List[str], scores: Dict[str, int]):
        candidate_keywords = {}
        for candidate in candidates:
            words = utils.tokenize(candidate)
            candidate_score = 0
            for word in words:
                candidate_score += scores[word]
            candidate_keywords[candidate] = candidate_score
        return candidate_keywords

    def fit(self, text: str) -> Dict[str, int]:
        candidates = self._generate_keywords(text)
        words_score = self._calculate_word_score(candidates)
        keywords = self._calculate_keyword_score(candidates, words_score)
        return dict(sorted(keywords.items(), key=operator.itemgetter(1), reverse=True))
