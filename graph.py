

import re
import networkx as nx
import requests
import random

from itertools import combinations, islice, chain
from clint.textui import progress



class Text:


    @classmethod
    def from_url(cls, url):

        """
        Create a text from a URL.

        Args:
            url (str)
        """

        return cls(requests.get(url).text)


    def __init__(self, text):

        """
        Set the text string, tokenize.

        Args:
            text (str)
        """

        self.text = text

        self.tokenize()


    def tokenize(self):

        """
        Split the text into a list of tokens.
        """

        self.tokens = []

        # Match sequences of letters.
        tokens = re.finditer('[a-z]{2,}', self.text.lower())

        for match in tokens:
            token = match.group(0)
            self.tokens.append(token)



class Graph:


    def __init__(self, text):

        """
        Set the text instance.

        Args:
            text (Text)
        """

        self.text = text

        self.graph = nx.Graph()


    def build(self, num_samples=500, sample_size=10):

        """
        Index term co-occurrence edges.

        Args:
            n (int): Window width.
        """

        for i in range(num_samples):

            # Get a random starting offset.
            start = random.randint(0, len(self.text.tokens)-sample_size)

            # Take N tokens after the offset.
            sample = self.text.tokens[start:start+sample_size]

            for t1, t2 in combinations(sample, 2):

                # If the edge exists, increment the weight.

                if self.graph.has_edge(t1, t2):
                    self.graph[t1][t2]['weight'] += 1

                # Otherwise, initialize the edge.

                else:
                    self.graph.add_edge(t1, t2, weight=1)


    def write_gml(self, path):

        """
        Serialize the graph as GML.

        Args:
            path (str)
        """

        nx.write_gml(self.graph, path)
