

import re
import networkx as nx
import requests
import random

from itertools import combinations, islice, chain
from collections import OrderedDict
from stop_words import get_stop_words



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

        # Get English stopwords.
        stopwords = get_stop_words('en')

        for match in tokens:

            token = match.group(0)

            if token not in stopwords:
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


    def build(self, n=10, keep=0.01):

        """
        Index term co-occurrence edges.

        Args:
            n (int): Window width.
        """

        for w in window(self.text.tokens, n):

            if random.random() > keep:
                continue

            for t1, t2 in combinations(w, 2):

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


def window(seq, n=2):

    """
    Yield a sliding window over an iterable.

    Args:
        seq (iter): The sequence.
        n (int): The window width.

    Yields:
        tuple: The next window.
    """

    for i in range(len(seq)-n):
        yield seq[i:i+n]
