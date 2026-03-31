# pysotsog Architecture

> **Standing on the shoulders of giants** — scholarly knowledge graph browser and citation tool.
>
> Version 0.4.1 · Apache 2.0 · [GitHub](https://github.com/WolfgangFahl/pysotsog)

---
see also AGENTS.md
## 1. Overview

`pysotsog` resolves scholarly identifiers (DOIs, ORCIDs, free-text queries) against multiple
knowledge graph sources and produces citation markup in formats understood by
[Semantic MediaWiki](https://www.semantic-mediawiki.org/) and BibTeX toolchains.

It is deployed as a **NiceGUI web application** at `https://sotsog2.bitplan.com/` and exposes a
**FastAPI REST endpoint** at `/api/v1/markup` documented via Swagger UI at `/docs`.

---

## 2. Package structure

```
pysotsog/
├── skg/                        # Main package ("Standing on the Shoulders of Giants")
│   ├── __init__.py             # version = "0.4.1"
│   ├── version.py              # Version dataclass (name, date, urls)
│   │
│   ├── sotsog_cmd.py           # CLI entry point  (SotSogCmd → WebserverCmd)
│   ├── sotsog.py               # Core orchestrator (SotSog.search / getMarkups)
│   ├── skgbrowser.py           # NiceGUI web UI   (SkgBrowser / SkgSolution)
│   ├── api.py                  # REST API routes  (register_routes → FastAPI app)
│   │
│   ├── search.py               # SearchOptions, SearchResult data classes
│   ├── graph.py                # Node, Concept, Property — SPARQL-backed graph nodes
│   ├── kg.py                   # SKG_Def: concept definitions + Wikidata/DBLP mappings
│   │
│   ├── paper.py                # Paper(Node)
│   ├── scholar.py              # Scholar(Node), Institution(Node)
│   ├── event.py                # Event(Node), EventSeries(Node), Proceedings(Node)
│   ├── location.py             # Country(Node)
│   │
│   ├── doi.py                  # DOI: validation, bibtex, citeproc JSON, DataCite, scite
│   ├── citeproc.py             # Citeproc.asScite(): metadata dict → SMW #scite markup
│   ├── crossref.py             # Crossref: habanero wrapper → bibtex + citeproc metadata
│   ├── orcid.py                # ORCID: validation, pub.orcid.org REST API, HTML badge
│   ├── ris.py                  # RIS_Entry: Research Information Systems format
│   ├── smw.py                  # SemWiki: Semantic MediaWiki access + markup generation
│   │
│   ├── wikidata.py             # Wikidata: SPARQL endpoint wrapper
│   ├── wdsearch.py             # WikidataSearch: wbsearchentities API
│   ├── dblp.py                 # Dblp: QLever SPARQL endpoint for DBLP
│   ├── dblp2wikidata.py        # Dblp2Wikidata: DBLP → Wikidata sync
│   ├── scholargrid.py          # ScholarGrid, ScholarQuery, SmwGrid
│   ├── semantic_scholar.py     # SemanticScholar: semanticscholar library wrapper
│   ├── searchengine.py         # InternetSearch: Google/Bing/Yahoo/DDG/Scholar
│   ├── owl.py                  # Owl(Schema): RDFLib OWL ontology loader
│   ├── schema.py               # Schema base class + PlantUML generator
│   └── profiler.py             # Simple timing profiler
│
├── tests/                      # unittest test suite
│   ├── base_skg_test.py        # BaseSkgTest(Basetest) + check_id_examples helper
│   ├── test_api.py             # REST API pipeline tests (network-skipped in CI)
│   ├── test_sotsog.py          # SotSog.search() end-to-end
│   ├── test_doi.py             # DOI validation, bibtex, citeproc, DataCite, scite
│   ├── test_crossref.py        # Crossref bibtex + metadata
│   └── ...                     # further test modules per source
│
├── sotsog_examples/            # Placeholder package for example scripts/data
│   └── __init__.py
│
├── scripts/                    # Shell helpers
│   ├── test                    # unittest discover / green / tox
│   ├── blackisort              # black + isort formatter
│   ├── install                 # pip install . -U
│   └── ...
│
├── pyproject.toml              # hatchling build, dependencies, entry point
├── mkdocs.yml                  # MkDocs documentation config
└── architecture.md             # this file
```

---

## 3. Web server layer

```
CLI invocation
  sotsog --server
        │
        ▼
SotSogCmd(WebserverCmd)          sotsog_cmd.py
        │  extends ngwidgets.WebserverCmd
        │  adds: --search, --bibtex, --scite, --smw, --wikiId, --dblp2wikidata
        │
        ▼
SkgBrowser(InputWebserver)       skgbrowser.py
        │  NiceGUI web application, default port 8765
        │  short_name = "sotsog"
        │  configures WikiUser, Wikidata SPARQL at startup
        │
        ├── @ui.page("/")        → SkgSolution.home()
        ├── @ui.page("/scholars")→ SkgSolution.scholars()
        └── register_routes(app) → /api/v1/markup  (FastAPI REST endpoint)

SkgSolution(InputWebSolution)    skgbrowser.py
        │  per-client NiceGUI state
        │  markup selector, textarea, search button, HTML result panels
        └── do_search() → SotSog.search() → item.markups → displayed inline
```

`NiceGUI`'s `app` object inherits from `fastapi.FastAPI`, so `@app.get(...)` routes
registered via `register_routes(app)` appear in the Swagger UI at `/docs` alongside
the NiceGUI internal routes.

---

## 4. REST API

### `GET /api/v1/markup`

Documented at `https://sotsog2.bitplan.com/docs`.

| Parameter | Type   | Required | Default | Description |
|-----------|--------|----------|---------|-------------|
| `doi`     | string | yes      | —       | DOI, e.g. `10.48550/arXiv.2202.12837` |
| `format`  | string | no       | `scite` | Output format: `scite` or `bibtex` |

**Content negotiation**

| `Accept` header | Response type | Body |
|-----------------|--------------|------|
| *(default)*     | `application/json` | `{"doi": "...", "format": "...", "markup": "..."}` |
| `text/plain`    | `text/plain`       | raw markup string |

**Error responses**

| HTTP status | Condition |
|-------------|-----------|
| 400 | Missing `doi` or not a valid DOI string |
| 500 | Upstream lookup failure (doi.org / crossref) |

**Example — scite (default)**

```
GET /api/v1/markup?doi=10.48550/arXiv.2202.12837
```

```json
{
  "doi": "10.48550/arXiv.2202.12837",
  "format": "scite",
  "markup": "Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?\n[[CiteRef::min2022re]]\n{{#scite:\n|reference=min2022re\n|type=journal-article\n|title=Rethinking the Role of Demonstrations: What Makes In-Context Learning Work?\n|authors=Sewon Min;Xinxi Lyu;Ari Holtzman;Mikel Artetxe;Mike Lewis;Hannaneh Hajishirzi;Luke Zettlemoyer\n|publisher=arXiv\n|doi=10.48550/ARXIV.2202.12837\n|year=2022\n|retrieved-from=https://doi.org/\n|retrieved-on=2026-03-31\n}}"
}
```

**Example — bibtex**

```
GET /api/v1/markup?doi=10.48550/arXiv.2202.12837&format=bibtex
```

```json
{
  "doi": "10.48550/arXiv.2202.12837",
  "format": "bibtex",
  "markup": "@misc{Min_2022,\n  title={Rethinking the Role of Demonstrations ...},\n  ...}"
}
```

---

## 5. Citation / markup pipeline

```
Input: DOI string  (e.g. "10.48550/arXiv.2202.12837")
        │
        ▼
DOI.isDOI()                      doi.py     regex validation
        │
        ├─── format=scite ───────────────────────────────────────────────────┐
        │    DOI.doi2Citeproc()   doi.py     GET doi.org  Accept: csl+json   │
        │           │                                                         │
        │    Citeproc.asScite()   citeproc.py                                │
        │           │  extracts: title, authors (given+family), year,        │
        │           │            publisher, DOI, ISSN, journal, volume,      │
        │           │            pages, subject                               │
        │           │  builds reference key: {family_lower}{year}{title[:2]} │
        │           ▼                                                         │
        │    full_markup:                                                     │
        │      {title}                                                        │
        │      [[CiteRef::{reference}]]                                      │
        │      {{#scite:                                                      │
        │      |reference={reference}                                        │
        │      |type=journal-article                                          │
        │      |title=...                                                     │
        │      |authors=First Last;First Last;...                            │
        │      |publisher=...                                                 │
        │      |doi=...                                                       │
        │      |year=...                                                      │
        │      |retrieved-from=https://doi.org/                              │
        │      |retrieved-on={YYYY-MM-DD}                                    │
        │      }}                                              ◄──────────────┘
        │
        └─── format=bibtex ──────────────────────────────────────────────────┐
             Crossref.doiBibEntry([doi])   crossref.py                       │
                    │  habanero.cn.content_negotiation()                     │
                    │  GET doi.org  Accept: application/x-bibtex            │
                    ▼                                                         │
             @article{key,                                                   │
               title = {...},                                                │
               author = {...},                                               │
               ...                                                           │
             }                                                ◄──────────────┘
```

---

## 6. Search pipeline

```
Input: search term(s)
        │
        ├── ORCID string?  ─────► Node.from_wikidata_via_id(Scholar, "orcid", ...)
        │                                      │
        ├── DOI string?    ─────► Paper.from_wikidata_via_id(Paper, "doi", ...)
        │                         Paper.from_dblp_via_id(Paper, "doi", ...)
        │                         (fallback: Paper.fromDOI → DOI metadata)
        │                                      │
        └── free text      ─────► WikidataSearch.searchOptions()  (wbsearchentities)
                                   Wikidata.getClassQids()         (SPARQL)
                                   concept.cls.from_wikidata_via_id(...)
                                              │
                                   SotSog.handleItem()
                                   SotSog.getMarkups()  ──► bibtex / scite / smw
```

---

## 7. Knowledge graph concepts

Defined in `kg.py` (`SKG_Def`). Each concept maps a Python class to Wikidata Q-IDs,
SPARQL property paths, DBLP RDF properties, and SMW template properties.

| Concept | Python class | Wikidata Q-ID example |
|---------|-------------|----------------------|
| Scholar | `Scholar` | Q937 (Albert Einstein) |
| Institution | `Institution` | Q273263 (RWTH Aachen) |
| Paper | `Paper` | Q55693406 |
| Event | `Event` | Q112055391 |
| EventSeries | `EventSeries` | Q105695678 |
| Proceedings | `Proceedings` | — |
| Country | `Country` | — |

---

## 8. External services

| Service | Module | Protocol | Purpose |
|---------|--------|----------|---------|
| doi.org | `doi.py` | HTTPS content negotiation | bibtex, citeproc JSON |
| DataCite API | `doi.py` | REST JSON | metadata for DataCite DOIs |
| Crossref API | `crossref.py` | habanero library | bibtex, metadata |
| Wikidata SPARQL | `wikidata.py`, `graph.py` | SPARQL (`query.wikidata.org`) | entity lookup |
| Wikidata Search | `wdsearch.py` | REST (`wbsearchentities`) | free-text search |
| DBLP SPARQL | `dblp.py` | SPARQL (`qlever.dev/api/dblp`) | paper lookup |
| ORCID Public API | `orcid.py` | REST JSON (`pub.orcid.org/v3.0`) | scholar works |
| Semantic Scholar | `semantic_scholar.py` | `semanticscholar` library | paper/author search |
| Semantic MediaWiki | `smw.py` | SMW ASK API (`wikibot3rd`) | scholar/paper markup |
| Internet Search | `searchengine.py` | `search-engine-parser` | Google/Bing/DDG |

---

## 9. Dependencies

| Package | Role |
|---------|------|
| `nicegui` | NiceGUI SPA framework (FastAPI/Starlette under the hood) |
| `ngwidgets >= 0.30.0` | NiceGUI widget extensions, `WebserverCmd`, `InputWebserver` base classes |
| `fastapi` | REST API (via NiceGUI's embedded FastAPI instance) |
| `habanero ~= 1.2.2` | Crossref API client |
| `pyLodStorage >= 0.18.7` | SPARQL endpoint, list-of-dicts storage, query manager |
| `pybasemkit >= 0.1.6` | Base utilities: YAML/JSON I/O, logging, CLI, shell execution |
| `py-3rdparty-mediawiki >= 0.18.1` | MediaWiki / SMW client (`wikibot3rd`) |
| `semanticscholar >= 0.11.0` | Semantic Scholar API client |
| `python-stdnum >= 1.18` | ORCID checksum validation (ISO 7064 MOD 11-2) |
| `py_ez_wikidata >= 0.3.2` | Wikidata item creation / property mapping |
| `wdgrid >= 0.2.1` | Wikidata grid/sync widgets |
| `search-engine-parser >= 0.6.8` | Multi-engine web search |
| `fake-useragent >= 0.1.11` | Rotating user-agent strings |
| `rispy >= 0.9.0` | RIS file format parser |
