#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pathlib
import os
from typing import Iterator
import re

from desker.nlp.pipotron import selector
from desker.nlp.pipotron.exceptions import InvalidTemplate
from desker.nlp.pipotron.bow import BagOfWords
from desker.nlp.pipotron.yaml_reader import YAMLReader


class Template:
    def __init__(self, file_name: str):
        self._text = None
        self._bow = BagOfWords()
        actual_path = pathlib.Path(__file__).parent.absolute()
        template_abs_path = os.path.join(actual_path, "templates/", file_name)
        if not os.path.isfile(template_abs_path):
            raise InvalidTemplate(f"Template file {template_abs_path} does not exists")
        with YAMLReader(template_abs_path) as content:
            self._template = content

    @staticmethod
    def parse_text(text) -> Iterator[str]:
        selectors = {s.key: s for s in selector.selectors}

        def parse_blob(blob, selectors):
            for key, value in blob.items():
                if key not in selectors:
                    raise InvalidTemplate(f"Selector {key} not implemented yet !")
                for text in selectors[key].select(value):
                    yield str(text)

        for blob in text:
            if isinstance(blob, str):
                yield str(blob)
                continue
            yield from parse_blob(blob, selectors)

    def replace_statements(self):
        stmts_re = re.compile(r"(?s)(?<=\{\{).*?(?=\}\})")
        selectors = {s.key: s for s in selector.selectors}
        sentences = []

        for sentence in self._text:
            stmts = stmts_re.findall(sentence)
            for stmt in stmts:
                calls = stmt.strip().split()
                if len(calls) < 2:
                    raise InvalidTemplate(f"Statement `{stmt}` is invalid")
                fn = calls.pop(0)
                if fn not in selectors:
                    raise InvalidTemplate(
                        f"Statement `{stmt}`, selector {fn} is not implemented"
                    )
                replaced_by = " ".join(list(selectors[fn].select(*calls)))
                sentence = sentence.replace(stmt, replaced_by)
            sentence = sentence.replace("{", "")
            sentence = sentence.replace("}", "")
            sentences.append(sentence)
        self._text = sentences

    def render(self):
        if not "text" in self._template:
            raise InvalidTemplate("Template should contain a `text` key.")

        text = self._template.pop("text")
        # First, we extract the bag of words
        self._bow.add_dict(self._template)
        # Then, we extract the text templates
        self._text = list(self.parse_text(text))
        # Finally, replace the statements (between brackets)
        self.replace_statements()
        return " ".join(self._text).strip()


if __name__ == "__main__":
    excuse = Template("excuses.yml")
    enarque = Template("ena.yml")
    l = Template("laboralphy.yml")
    email = Template("email.yml")
    BagOfWords().add("destinataire", "ljk")
    BagOfWords().set("destinataire", "ljk")

    print(f"===========\nENA:\n{ enarque.render() }")
    print(f"===========\nEXCUSE MOI:\n{ excuse.render() }")
    print(f"===========\nLABARALPHY:\n{ l.render() }")
    print(f"===========\nEMAIL:\n{ email.render() }")
