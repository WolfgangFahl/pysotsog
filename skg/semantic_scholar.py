"""
Created on 2022-11-22

@author: __wf__
"""

import os

from semanticscholar import SemanticScholar as SemScholar


class SemanticScholar:
    """
    wrapper for Semantic Scholar API
    """

    def __init__(self, timeout: float = 5.0, retry: bool = False, api_key: str = None):
        """
        constructor

        Args:
            timeout: request timeout in seconds
            retry: whether to retry failed requests
            api_key: Semantic Scholar API key (reads from SEMANTIC_SCHOLAR_API_KEY env var if not provided)
        """
        self.timeout = timeout
        self.api_key = api_key or os.getenv("SEMANTIC_SCHOLAR_API_KEY")
        self.sch = SemScholar(timeout=timeout, retry=retry, api_key=self.api_key)

    def get_paper(self, doi: str):
        """
        get the paper with the given DOI identifier

        Args:
            doi: Digital Object Identifier

        Returns:
            paper object
        """
        paper = self.sch.get_paper(doi)
        return paper

    def search_paper(self, query: str):
        """
        search for papers by query

        Args:
            query: search query string

        Returns:
            search results
        """
        results = self.sch.search_paper(query)
        return results
