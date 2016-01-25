

import requests
import re


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
            self.tokens.append(match.group(0))
