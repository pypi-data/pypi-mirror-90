import itertools
import operator
from typing import List

import editdistance
import networkx as nx
import nltk

from desker.nlp import utils


class TextRank:
    """Implements the TextRank algorithm

    see. https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf
    """

    def __init__(self):
        pass

    @staticmethod
    def build_graph(tokens: List[str]):
        graph = nx.Graph()
        graph.add_nodes_from(tokens)
        pairs = list(itertools.combinations(tokens, 2))
        for pair in pairs:
            distance = editdistance.eval(pair[0], pair[1])
            graph.add_edge(pair[0], pair[1], weight=distance)
        return graph

    @staticmethod
    def _compute_text_rank(tokens: List[str], keyphrases: List[str]):
        res = []
        seen = []
        i = 1
        while i < len(tokens):
            a = tokens[i - 1]
            b = tokens[i]
            if a in keyphrases and b in keyphrases:
                keyphrase = " ".join([a, b])
                res.append(keyphrase)
                seen.extend([a, b])
            elif a in keyphrases and a not in seen:
                res.append(a)
            i = i + 1
        return set(res)

    @staticmethod
    def _compute_scores(candidates, page_rank):
        scores = []
        for candidate in candidates:
            score = 0
            words = utils.tokenize(candidate)
            for word in words:
                if word in page_rank:
                    score = score + page_rank[word]
            scores.append((candidate, score / len(words)))
        return sorted(scores, key=operator.itemgetter(1), reverse=True)

    def fit(self, text: str, max_words=5):
        # text = utils.stem_sentence(text)
        raw_tokens = utils.tokenize(text)
        raw_tokens = utils.remove_stopwords(raw_tokens)
        tokens_pos = nltk.pos_tag(raw_tokens)

        def _filter_tags(items):
            filtered_out = [
                "NN",  # Noun, singular or mass
                "NNS",  # Noun, plural
                "JJ",  # Adjective
                "NNP",  # Proper noun, singular
                "NNPS",  # Proper noun, plural
            ]
            return list({item[0] for item in items if item[1] in filtered_out})

        tokens = _filter_tags(tokens_pos)

        graph = self.build_graph(tokens)

        page_rank = nx.pagerank(graph, weight="weight")
        keywords = sorted(page_rank, key=page_rank.get, reverse=True)
        keyphrases = keywords[0: len(tokens) // 3 + 1]

        candidates = self._compute_text_rank(raw_tokens, keyphrases)
        candidates_scores = self._compute_scores(candidates, page_rank)

        return [c for c in candidates_scores if len(c[0].split()) <= max_words]
