from abc import abstractmethod
from abc import ABC
from typing import Iterator
from typing import List
import random

from desker.nlp.pipotron.bow import BagOfWords


class BaseSelector(ABC):
    @property
    def key(self):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def select(items: List[str]) -> Iterator[str]:
        pass


class OneSelector(BaseSelector):
    """Select a random element whithin a given list.

    Example:
        >> ONE().select(["a", "b", "c"])
        >> "b"
    """

    key = "ONE"

    @staticmethod
    def select(items):

        yield random.choice(items)


class AllOfSelector(BaseSelector):
    """Select all elements whithin a bag of word

    Example:
        >> ALL_OF().select("countries")
        >> ["korea", "france", "spain", ...]
    """

    key = "ALL_OF"
    _bow = BagOfWords()

    @staticmethod
    def select(items):
        if isinstance(items, List):
            raise ValueError("AllOF selectors requires a single category as parameter.")
        yield from AllOfSelector._bow.get(items)


class OneOfSelector(BaseSelector):
    """Select a random element whithin a bag of word

    Example:
        >> ONE_OF().select("countries")
        >> "korea"
    """

    key = "ONE_OF"
    _bow = BagOfWords()

    @staticmethod
    def select(items):
        if isinstance(items, List):
            raise ValueError("OneOF selectors requires a single category as parameter.")
        yield random.choice(OneOfSelector._bow.get(items))


class AllSelector(BaseSelector):
    """Select all elements from a list

    Example:
        >> ALL().select(["a", "b", "c"])
        >> ["a", "b", "c"]
    """

    key = "ALL"

    @staticmethod
    def select(items):
        yield from items


selectors = [OneSelector, AllSelector, OneOfSelector, AllOfSelector]
