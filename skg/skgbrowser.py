"""
Created on 2022-11-18

@author: wf
"""

import os
from urllib import parse

from ngwidgets.input_webserver import InputWebserver, InputWebSolution
from ngwidgets.webserver import WebserverConfig
from ngwidgets.widgets import Lang, Link
from nicegui import Client, run, ui
from wikibot3rd.wikiuser import WikiUser

from skg.graph import Node
from skg.orcid import ORCID
from skg.scholargrid import ScholarGrid
from skg.sotsog import SotSog
from skg.version import Version
from skg.wikidata import Wikidata


class SkgBrowser(InputWebserver):
    """
    scholary knowledge graph browser
    """

    @classmethod
    def get_config(cls) -> WebserverConfig:
        copy_right = "(c)2022-2025 Wolfgang Fahl"
        config = WebserverConfig(
            copy_right=copy_right,
            version=Version(),
            default_port=8765,
            short_name="sotsog",
        )
        server_config = WebserverConfig.get(config)
        server_config.solution_class = SkgSolution
        return server_config

    def __init__(self):
        """Constructs all the necessary attributes for the WebServer object."""
        config = SkgBrowser.get_config()
        InputWebserver.__init__(self, config=config)

        @ui.page("/scholars")
        async def scholars(client: Client):
            return await self.page(client, SkgSolution.scholars)

    def configure_run(self):
        # wiki users
        self.wikiUsers = WikiUser.getWikiUsers()
        self.wikiId = self.args.wikiId
        wikidata = Wikidata()
        self.sparql = wikidata.sparql
        if hasattr(self.args, "root_path"):
            self.root_path = self.args.root_path
        else:
            self.root_path = SkgBrowser.examples_path()

    @classmethod
    def examples_path(cls) -> str:
        # the root directory (default: examples)
        path = os.path.join(os.path.dirname(__file__), "../sotsog_examples")
        path = os.path.abspath(path)
        return path


class SkgSolution(InputWebSolution):
    """
    the scholarly knowledge graph solution
    """

    def __init__(self, webserver: SkgBrowser, client: Client):
        """
        Initialize the solution

        Calls the constructor of the base solution
        Args:
            webserver (SkgBrowser): The webserver instance associated with this context.
            client (Client): The client instance this context is associated with.
        """
        super().__init__(webserver, client)  # Call to the superclass constructor
        self.language = "en"
        self.wikiId = "cr"
        self.markup_names = ["-", "bibtex", "scite", "smw"]
        self.markup_name = self.markup_names[1]
        self.scholia_base = "https://qlever.scholia.wiki"
        self.sotsog = SotSog.instance
        self.sotsog.options.open_browser = False
        Node.scholia_base = self.scholia_base

    def configure_menu(self):
        """
        configure additional non-standard menu entries
        """
        # self.link_button(name='Scholars',icon_name='account-school',target='/scholars')
        pass

    def configure_settings(self):
        """
        configure settings for the scholarly knowledge graph
        """
        super().configure_settings()

        def update_scholia_base(e):
            Node.scholia_base = e.value

        scholia_select = self.add_select(
            "scholia", ["https://qlever.scholia.wiki", "https://scholia.toolforge.org"]
        )
        scholia_select.bind_value(self, "scholia_base")
        scholia_select.on_value_change(update_scholia_base)

    def createItemLink(self, item, term: str, index: int) -> str:
        """
        create a link for the given item

        Args:
            item(Node): the item to create a link for
            term(str): the
        """
        if index > 0:
            style = "color:grey"
            text = f"{term}<sub>{index + 1}</sub>"
            delim = "&nbsp"
        else:
            style = ""
            text = term
            delim = ""
        link = Link.create(
            item.browser_url(), text, tooltip=item.label, target="_blank", style=style
        )
        if item.concept.name == "Scholar":
            if hasattr(item, "orcid"):
                orcid = ORCID(item.orcid)
                link += orcid.asHtml()
        markup = delim + link
        return markup

    async def onSearchButton(self, _msg):
        """
        handle button to search for terms
        """
        await run.io_bound(self.do_search)

    def do_search(self):
        """
        perform a search with the given search terms
        """
        try:
            self.results.content = ""
            self.markup.content = ""
            terms = self.searchTerms.value.split("\n")
            self.messages.content = "Searching"
            delim = ""
            for term in terms:
                if term:
                    msg = f"... {term}\n"
                    self.messages.content += msg
                    if self.markup_name == "-":
                        self.sotsog.options.markup_names = []
                    else:
                        self.sotsog.options.markup_names = [self.markup_name]
                    search_result = self.sotsog.search([term], self.sotsog.options)
                    items = search_result.items
                    rmarkup = ""
                    if len(items) == 0:
                        # TODO check google search
                        # https://pypi.org/project/googlesearch-python/
                        params = parse.urlencode({"q": term})
                        search_url = f"https://www.google.com/search?{params}"
                        rmarkup = Link.create(
                            search_url,
                            term,
                            "not found",
                            target="_blank",
                            style="color:red",
                        )
                    else:
                        for i, item in enumerate(items):
                            rmarkup += self.createItemLink(item, term, i)
                            if len(item.markups) > 0:
                                markups = ""
                                for _markup_name, markup in item.markups.items():
                                    markups += markup
                                    self.markup.content += f"<pre>{markups}</pre>"
                                    # break
                    self.results.content += delim + rmarkup
                    delim = "<br>"
            # handle errors
            for entry in self.sotsog.log.entries:
                markup = entry.as_html()
                self.markup.content += delim + markup
                delim = "<br>"

        except BaseException as ex:
            self.handle_exception(ex)

    def addLanguageSelect(self):
        """
        add a language selector
        """
        lang_dict = Lang.get_language_dict()
        self.add_select("language:", lang_dict).bind_value(self, "language")

    def addWikiUserSelect(self):
        """
        add a wiki user selector
        """
        if len(self.wikiUsers) > 0:
            wu_dict = {}
            for wikiUser in sorted(self.wikiUsers):
                wu_dict[wikiUser] = wikiUser
            self.add_select("wiki:", wu_dict).bind_value(self, "wikiId")

    async def scholars(self):
        """
        scholar display

        """
        self.setup_menu()
        with ui.element("div").classes("w-full h-full"):
            try:
                self.scholarsGrid = ScholarGrid(
                    self, self.wikiUsers, self.wikiId, sparql=self.sparql
                )
                # @TODO refactor the two setup calls to one to hide wdgrid details
                # self.scholarsGrid.setup(a=self.rowB, header=self.rowA)
                # self.scholarsGrid.wdgrid.setup(a=self.rowC)
            except BaseException as ex:
                self.handle_exception(ex)
        await self.setup_footer()

    def setup_content(self):
        with ui.splitter() as self.splitter:
            with self.splitter.before:
                self.add_select("markup", self.markup_names).bind_value(
                    self, "markup_name"
                )
                self.searchTerms = ui.textarea(placeholder="enter search terms")
                self.searchButton = ui.button("search", on_click=self.onSearchButton)
            with self.splitter.after:
                self.markup = ui.html()
        self.messages = ui.html()
        self.results = ui.html()

    async def home(self):
        """
        provide the main content page

        """

        await self.setup_content_div(self.setup_content)
