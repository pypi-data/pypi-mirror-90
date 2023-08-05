"""
    .. autofunction:: setup
    .. autofunction:: init_foot_bibliography_id
"""

import docutils.nodes

from typing import Any, Dict

from sphinx.application import Sphinx

from .domain import BibtexDomain
from .nodes import bibliography
from .roles import CiteRole
from .directives import BibliographyDirective
from .transforms import BibliographyTransform
from .foot_nodes import footbibliography
from .foot_roles import FootCiteRole
from .foot_directives import FootBibliographyDirective
from .foot_directives import new_foot_bibliography_id
from .foot_transforms import FootBibliographyTransform


def init_foot_bibliography_id(app: Sphinx, docname: docutils.nodes.document,
                              source: str) -> None:
    """Initialize current footbibliography id for *docname*."""
    new_foot_bibliography_id(app.env)


def setup(app: Sphinx) -> Dict[str, Any]:
    """Set up the bibtex extension:

    * register config values
    * register directives
    * register nodes
    * register roles
    * register transforms
    * connect events to functions
    """

    app.add_config_value("bibtex_default_style", "alpha", "html")
    app.add_config_value("bibtex_bibfiles", None, "html")
    app.add_config_value("bibtex_encoding", "utf-8-sig", "html")
    app.add_config_value("bibtex_bibliography_header", "", "html")
    app.add_config_value("bibtex_footbibliography_header", "", "html")
    app.add_domain(BibtexDomain)
    app.connect("source-read", init_foot_bibliography_id)
    app.add_directive("bibliography", BibliographyDirective)
    app.add_role("cite", CiteRole())
    app.add_node(bibliography, override=True)
    app.add_post_transform(BibliographyTransform)
    app.add_directive("footbibliography", FootBibliographyDirective)
    app.add_role("footcite", FootCiteRole())
    app.add_node(footbibliography, override=True)
    app.add_transform(FootBibliographyTransform)

    return {
        'env_version': 6,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        }
