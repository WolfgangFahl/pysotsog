"""
Created on 2026-03-31

@author: wf
"""

import unittest

from basemkit.basetest import Basetest

from skg.api import _get_markup
from skg.doi import DOI


class TestAPI(Basetest):
    """
    Test the REST API markup generation pipeline.

    Network tests are skipped in public CI since they require
    outbound access to doi.org and api.crossref.org.
    """

    # The paper from the user's example
    ARXIV_DOI = "10.48550/arXiv.2202.12837"
    ARXIV_DOI_UPPER = "10.48550/ARXIV.2202.12837"

    def test_doi_validation(self):
        """
        DOI.isDOI should accept the arXiv DOI and reject junk input
        """
        self.assertTrue(DOI.isDOI(self.ARXIV_DOI))
        self.assertTrue(DOI.isDOI("10.1007/978-3-031-21595-7_17"))
        self.assertFalse(DOI.isDOI("not-a-doi"))
        self.assertFalse(DOI.isDOI(""))
        self.assertFalse(DOI.isDOI(None))

    @unittest.skipIf(Basetest.inPublicCI(), "requires network access to doi.org")
    def test_scite_markup(self):
        """
        _get_markup for the arXiv paper should produce valid #scite markup
        containing the expected title, CiteRef, and doi field.
        """
        debug = self.debug
        markup = _get_markup(self.ARXIV_DOI, "scite")
        if debug:
            print(markup)
        # Title line
        self.assertIn("Rethinking the Role of Demonstrations", markup)
        # CiteRef link
        self.assertIn("[[CiteRef::", markup)
        # scite template
        self.assertIn("{{#scite:", markup)
        # doi field (doi.org normalises to uppercase for arXiv DOIs)
        self.assertTrue(
            f"|doi={self.ARXIV_DOI}" in markup
            or f"|doi={self.ARXIV_DOI_UPPER}" in markup,
            f"Expected doi field in markup:\n{markup}",
        )
        # authors should include first author
        self.assertIn("Sewon Min", markup)
        # year
        self.assertIn("|year=2022", markup)

    @unittest.skipIf(
        Basetest.inPublicCI(), "requires network access to api.crossref.org"
    )
    def test_bibtex_markup(self):
        """
        _get_markup for bibtex format should return a BibTeX entry starting with '@'
        """
        debug = self.debug
        markup = _get_markup(self.ARXIV_DOI, "bibtex")
        if debug:
            print(markup)
        self.assertTrue(
            markup.strip().startswith("@"),
            f"Expected BibTeX entry starting with '@', got:\n{markup[:200]}",
        )

    def test_invalid_format_falls_back(self):
        """
        _get_markup with an unknown format should raise ValueError
        (the API layer normalises to scite before calling this, but the
        function itself should be explicit about unsupported formats)
        """
        with self.assertRaises(ValueError):
            _get_markup(self.ARXIV_DOI, "unknown_format")
