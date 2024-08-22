"""
Created on 2022-11-16

@author: wf
"""

import webbrowser

from skg.crossref import Crossref
from skg.doi import DOI
from skg.graph import Node
from skg.kg import SKG_Def
from skg.orcid import ORCID
from skg.paper import Paper
from skg.search import SearchOptions, SearchResult
from skg.smw import SemWiki
from skg.wdsearch import WikidataSearch
from skg.wikidata import Wikidata


class SotSog:
    """
    Standing on the shoulders of giants
    """
    instance=None

    def __init__(self,debug:bool=False):
        """
        constructor

        """
        SotSog.instance=self
        self.debug=debug
        Node.debug = self.debug
        self.wikipedia_url = (
            "https://en.wikipedia.org/wiki/Standing_on_the_shoulders_of_giants"
        )
        self.skg_def = SKG_Def()
        self.scholar_concept = self.skg_def.concepts["Scholar"]

    def getMarkups(self, item, options: SearchOptions) -> dict:
        """
        get the markups for the given item and search options

        Args:
            item(Node): the item to get the markup for
            options(SearchOptions): the search options to apply
        """
        markups = {}
        do_markup = len(options.markup_names) > 0
        if do_markup:
            if item.concept.name == "Paper":
                doi = getattr(item, "doi", None)
                if doi is not None:
                    crossref = Crossref()
                    if "bibtex" in options.markup_names:
                        bibentry = crossref.doiBibEntry([doi])
                        markups["bibtex"] = bibentry
                    if "scite" in options.markup_names:
                        # meta_data=crossref.doiMetaData([doi])
                        # scite_entry=crossref.asScite(meta_data)
                        if not hasattr(item, "doi_obj"):
                            item.fromDOI(doi)
                        scite_entry = item.doi_obj.asScite()
                        markups["scite"] = scite_entry
            if item.concept.name == "Scholar":
                if "smw" in options.markup_names:
                    markups["smw"] = SemWiki.asMarkup(item)
        return markups

    def wd_search(self, wd: Wikidata, search_term: str, options) -> list:
        """
        do a wikidata search
        """
        items = []
        wds = WikidataSearch(language=options.lang, debug=self.debug)
        search_options = wds.searchOptions(search_term, limit=options.limit)
        qids = []
        for qid, itemLabel, desc in search_options:
            qids.append(qid)
        class_map = wd.getClassQids(qids)
        for qid, itemLabel, desc in search_options:
            if qid in class_map:
                class_rows = class_map[qid]
                for class_row in class_rows:
                    class_qid = class_row["class_qid"]
                    concept = self.skg_def.conceptForQid(class_qid)
                    if concept is not None:
                        wd_items = concept.cls.from_wikidata_via_id(
                            concept, "wikiDataId", qid, lang=options.lang
                        )
                        if len(wd_items) > 0:
                            item = wd_items[0]
                            items.append(item)
                            self.handleItem(item, qid, itemLabel, desc, options)
        return items

    def handleItem(self, item, item_id, itemLabel, desc, options):
        """
        handle the given item as a search result
        """
        if options.show:
            print(f"{itemLabel}({item_id}):{desc}✅")
            print(item)
        item.markups = self.getMarkups(item, options)
        if options.show:
            for markup_name, markup in item.markups.items():
                print(f"{markup_name} markup:")
                print(markup)
            pass
        if options.open_browser:
            browser_url = item.browser_url()
            if browser_url is not None:
                print(f"opening {browser_url} in browser")
                webbrowser.open(browser_url)

    def handleItems(self, items, options):
        """
        handle the given items
        """
        for item in items:
            item_id = item.wikiDataId
            itemLabel = item.label
            desc = "?"
            self.handleItem(item, item_id, itemLabel, desc, options)

    def handleDoiItem(self, item, options: SearchOptions):
        item_id = item.doi
        itemLabel = item.title
        desc = item.title
        self.handleItem(item, item_id, itemLabel, desc, options)

    def search(self, search_list, options: SearchOptions) -> SearchResult:
        """
        search with the given search list

        Args:
            search_list(list): a list of search terms
            options(SearchOptions): the search options to apply
        """
        search_result = SearchResult(search_list, options)
        search_term = " ".join(search_list)
        for prefix in ["https://doi.org"]:
            if search_term.startswith(prefix):
                search_term = search_term.replace(prefix, "")
        wd = Wikidata(debug=self.debug)
        if ORCID.isORCID(search_term):
            scholar_concept = self.skg_def.concepts["Scholar"]
            items = Node.from_wikidata_via_id(
                scholar_concept, "orcid", search_term, options.lang
            )
            self.handleItems(items, options)
        elif DOI.isDOI(search_term):
            # DOI may not be referencing paper but something else
            paper_concept = self.skg_def.concepts["Paper"]
            items = Paper.from_wikidata_via_id(
                paper_concept, "doi", search_term, options.lang
            )
            self.handleItems(items, options)
            dblp_items = Paper.from_dblp_via_id(
                paper_concept, "doi", search_term.lower()
            )
            if len(dblp_items) == 0:
                paper = Paper()
                paper.concept = paper_concept
                paper.fromDOI(search_term)
                paper.provenance = "doi"
                dblp_items = [paper]
            for item in dblp_items:
                self.handleDoiItem(item, options)
            items.extend(dblp_items)
        else:
            items = self.wd_search(wd, search_term, options)
        search_result.items = items
        return search_result
