import json
from itertools import starmap
from typing import Any, Dict, Iterator

import rdflib
from boltons.iterutils import remap
from pyld import jsonld

from octadocs.octiron.context import merge
from octadocs.octiron.types import LOCAL, Context, Triple

MetaData = Dict[str, Any]   # type: ignore


def _convert(term: Any) -> Any:  # type: ignore
    """Convert $statement to @statement."""
    if isinstance(term, str) and term.startswith('$'):
        return '@' + term[1:]  # noqa: WPS336

    return term


def convert_dollar_signs(
    meta_data: MetaData,
) -> MetaData:
    """
    Convert $ character to @ in keys.

    We use $ by convention to avoid writing quotes.
    """
    return remap(
        meta_data,
        lambda path, key, value: (  # noqa: WPS110
            _convert(key),
            _convert(value),
        ),
    )


def as_triple_stream(
    raw_data: MetaData,
    context: Context,
    local_iri: str,
) -> Iterator[Triple]:
    """Convert YAML dict to a stream of triples."""
    meta_data = convert_dollar_signs(raw_data)

    local_context = meta_data.pop('@context', None)
    if local_context is not None:
        context = merge(
            first=context,
            second=local_context,
        )

    if meta_data.get('@id') is not None:
        # The author specified an IRI the document tells us about. Let us
        # link this IRI to the local document IRI.
        meta_data['octa:subjectOf'] = local_iri

    else:
        # The document author did not tell us about what their document is.
        # In this case, we assume that the local_iri of the document file
        # is the subject of the document description.
        meta_data['@id'] = local_iri

    # Reason: https://github.com/RDFLib/rdflib-jsonld/issues/97
    # If we don't expand with an explicit @base, import will fail silently.
    meta_data = jsonld.expand(
        meta_data,
        options={
            'base': str(LOCAL),
            'expandContext': context,
        },
    )

    # Reason: https://github.com/RDFLib/rdflib-jsonld/issues/98
    # If we don't flatten, @included sections will not be imported.
    meta_data = jsonld.flatten(meta_data)

    serialized_meta_data = json.dumps(meta_data, indent=4)

    graph = rdflib.Graph()

    graph.parse(
        data=serialized_meta_data,
        format='json-ld',
    )

    yield from starmap(Triple, iter(graph))
