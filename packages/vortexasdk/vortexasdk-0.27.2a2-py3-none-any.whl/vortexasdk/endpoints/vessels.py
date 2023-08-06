"""Vessels Endpoint."""
from typing import Dict, List, Union

from vortexasdk.api.id import ID
from vortexasdk.endpoints.endpoints import VESSELS_REFERENCE
from vortexasdk.endpoints.vessels_result import VesselsResult
from vortexasdk.operations import Reference, Search
from vortexasdk.utils import convert_to_list


class Vessels(Reference, Search):
    """Vessels endpoint."""

    def __init__(self):
        """Instantiate endpoint using reference endpoint."""
        Reference.__init__(self, VESSELS_REFERENCE)
        Search.__init__(self, VESSELS_REFERENCE)

    def load_all(self) -> VesselsResult:
        """Load all vessels."""
        return self.search()

    def search(
        self,
        term: Union[str, List[str]] = None,
        ids: Union[str, List[str]] = None,
        vessel_classes: Union[str, List[str]] = None,
        vessel_product_types: Union[ID, List[ID]] = None,
        vessel_scrubbers: str = "disabled",
        exact_term_match: bool = False,
    ) -> VesselsResult:
        """
        Find all vessels matching given search arguments. Search arguments are combined in an AND manner.

        # Arguments
            term: The name(s) (or partial name(s)) of a vessel we'd like to search

            ids: ID or IDs of vessels we'd like to search

            vessel_classes: vessel_class (or list of vessel classes) we'd like to search. Each vessel class must be one of `"tiny_tanker" , "general_purpose" , "handysize" , "handymax" , "panamax", "aframax" , "suezmax" , "vlcc_plus" , "sgc" , "mgc" , "lgc" , "vlgc"`. Refer to [VortexaAPI Vessel Entities](https://docs.vortexa.com/reference/intro-vessel-entities) for the most up-to-date list of vessel classes.

            vessel_product_types: A product ID, or list of product IDs to filter on, searching vessels _currently_ carrying these products.

            vessel_scrubbers: An optional filter to filter on vessels with or without scrubbers.
             To disable the filter (the default behaviour), enter 'disabled'.
             To only include vessels with scrubbers, enter 'inc'.
             To exclude vessels with scrubbers, enter 'exc'.

             exact_term_match: Search on only exact term matches, or allow similar matches.
                 e.g. When searching for "Ocean" with `exact_term_match=False`, then the SDK will yield vessels named
                ['Ocean', 'Ocean Wisdom', ...] etc. When `exact_term_match=True`,
                the SDK will only yield the vessel named `Ocean`.


        # Returns
        List of vessels matching the search arguments.


        # Examples

        - Let's find all the VLCCs with 'ocean' in their name, or related names.

        ```python
        >>> from vortexasdk import Vessels
        >>> vessels_df = Vessels().search(vessel_classes='vlcc', term='ocean').to_df(columns=['name', 'imo', 'mmsi', 'related_names'])

        ```
        |    | name         |     imo |      mmsi | related_names             |
        |---:|:-------------|--------:|----------:|:--------------------------|
        |  0 | OCEANIS      | 9532757 | 241089000 | ['OCEANIS']               |
        |  1 | AEGEAN       | 9732553 | 205761000 | ['GENER8 OCEANUS']        |
        |  2 | OCEANIA      | 9246633 | 205753000 | ['OCEANIA'| 'TI OCEANIA'] |
        |  3 | ENEOS OCEAN  | 9662875 | 432986000 | ['ENEOS OCEAN']           |
        |  4 | OCEAN LILY   | 9284960 | 477178100 | ['OCEAN LILY']            |
        |  5 | SHINYO OCEAN | 9197868 | 636019316 | ['SHINYO OCEAN']          |
        |  6 | NASHA        | 9079107 | 370497000 | ['OCEANIC']               |
        |  7 | HUMANITY     | 9180281 | 422204700 | ['OCEAN NYMPH']           |

        Note the `term` search also looks for vessels with matching `related_names`


        - Let's find all the vessels currently carrying Crude.

        ```python
        >>> from vortexasdk import Vessels, Products
        >>> crude = [p.id for p in Products().search(term="crude").to_list() if 'group' in p.layer]
        >>> vessels_df = Vessels().search(vessel_product_types=crude).to_df()

        ```

        # Further Documentation

        [VortexaAPI Vessel Reference](https://docs.vortexa.com/reference/POST/reference/vessels)

        """
        api_params = {
            "term": [str(e) for e in convert_to_list(term)],
            "ids": convert_to_list(ids),
            "vessel_product_types": convert_to_list(vessel_product_types),
            "vessel_classes": [
                v.lower() for v in convert_to_list(vessel_classes)
            ],
            "vessel_scrubbers": vessel_scrubbers,
        }

        return VesselsResult(
            super().search(exact_term_match=exact_term_match, **api_params)
        )

    def reference(self, id: ID) -> Dict:
        """
        Perform a vessel lookup.

        # Arguments
            id: Vessel ID to lookup

        # Returns
        Vessel record matching the ID

        # Further Documentation:
        [VortexaAPI Vessel Reference](https://docs.vortexa.com/reference/GET/reference/vessels/%7Bid%7D)

        """
        return super().reference(id)


AVAILABLE_VESSEL_CLASSES = [
    "tiny_tanker",
    "general_purpose",
    "handysize",
    "handymax",
    "panamax",
    "aframax",
    "suezmax",
    "vlcc_plus",
    "vlcc",
    "sgc",
    "mgc",
    "lgc",
    "vlgc",
]
