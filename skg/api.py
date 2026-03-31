"""
Created on 2026-03-31

@author: wf
"""

from typing import Optional

from fastapi import Request
from fastapi.responses import JSONResponse, PlainTextResponse

from skg.crossref import Crossref
from skg.doi import DOI

VALID_FORMATS = ("scite", "bibtex")


def register_routes(app):
    """
    Register REST API routes on the given FastAPI/NiceGUI app instance.

    Args:
        app: the FastAPI application instance (nicegui.app)
    """

    @app.get(
        "/api/v1/markup",
        tags=["markup"],
        summary="Get citation markup for a DOI",
        response_description="Citation markup in the requested format",
    )
    async def get_markup(
        request: Request,
        doi: str,
        format: Optional[str] = "scite",
    ):
        """
        Return citation markup for the given DOI.

        Supported formats:
        - **scite** (default): Semantic Cite `{{#scite:...}}` markup for use in
          Semantic MediaWiki (SemanticCite extension)
        - **bibtex**: BibTeX entry via Crossref content negotiation

        Content negotiation:
        - Default response: `application/json` with `{doi, format, markup}`
        - Pass `Accept: text/plain` to receive the raw markup string directly
        """
        # Validate DOI
        if not doi:
            return JSONResponse(
                status_code=400,
                content={"error": "Missing required parameter: doi"},
            )
        if not DOI.isDOI(doi):
            return JSONResponse(
                status_code=400,
                content={"error": f"Not a valid DOI: {doi}"},
            )

        # Normalize format
        fmt = (format or "scite").lower()
        if fmt not in VALID_FORMATS:
            fmt = "scite"

        # Generate markup
        try:
            markup = _get_markup(doi, fmt)
        except Exception as ex:
            return JSONResponse(
                status_code=500,
                content={"error": f"Markup generation failed: {str(ex)}"},
            )

        # Content negotiation
        accept = request.headers.get("accept", "")
        if "text/plain" in accept:
            return PlainTextResponse(content=markup)

        return JSONResponse(
            content={
                "doi": doi,
                "format": fmt,
                "markup": markup,
            }
        )


def _get_markup(doi: str, fmt: str) -> str:
    """
    Generate citation markup for a DOI in the requested format.

    Args:
        doi(str): the DOI string
        fmt(str): output format — 'scite' or 'bibtex'

    Returns:
        str: the markup string
    """
    if fmt == "scite":
        doi_obj = DOI(doi)
        return doi_obj.asScite()
    elif fmt == "bibtex":
        crossref = Crossref()
        return crossref.doiBibEntry([doi])
    else:
        raise ValueError(f"Unsupported format: {fmt}")
