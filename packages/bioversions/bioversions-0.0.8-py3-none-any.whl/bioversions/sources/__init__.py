# -*- coding: utf-8 -*-

"""Sources for Bioversions."""

from typing import Iterable, List, Mapping, Type

from .biofacquim import BiofacquimGetter
from .biogrid import BioGRIDGetter
from .chembl import ChEMBLGetter
from .complexportal import ComplexPortalGetter
from .daily import NCBIGeneGetter
from .drugbank import DrugBankGetter
from .drugcentral import DrugCentralGetter
from .expasy import ExPASyGetter
from .intact import IntActGetter
from .interpro import InterProGetter
from .kegg import KEGGGetter
from .mirbase import MirbaseGetter
from .msigdb import MSigDBGetter
from .npass import NPASSGetter
from .obo import (
    ChebiGetter, ClGetter, DoidGetter, GoGetter, HpGetter, PatoGetter, PoGetter, PrGetter, XaoGetter, ZfaGetter,
)
from .pathbank import PathBankGetter
from .pfam import PfamGetter
from .reactome import ReactomeGetter
from .rfam import RfamGetter
from .uniprot import UniProtGetter
from .wikipathways import WikiPathwaysGetter
from ..utils import Bioversion, Getter, norm, refresh_daily

__all__ = [
    'getters',
    'getter_dict',
    'resolve',
    'get_rows',
    'get_version',
]

# TODO replace with entrypoint lookup
getters = [
    BioGRIDGetter,
    ChEMBLGetter,
    ComplexPortalGetter,
    DrugBankGetter,
    DrugCentralGetter,
    ExPASyGetter,
    HpGetter,
    IntActGetter,
    InterProGetter,
    ReactomeGetter,
    RfamGetter,
    ChebiGetter,
    PrGetter,
    DoidGetter,
    GoGetter,
    XaoGetter,
    WikiPathwaysGetter,
    MirbaseGetter,
    MSigDBGetter,
    PatoGetter,
    PoGetter,
    PfamGetter,
    ClGetter,
    ZfaGetter,
    UniProtGetter,
    KEGGGetter,
    PathBankGetter,
    NCBIGeneGetter,
    NPASSGetter,
    BiofacquimGetter,
]
getters = sorted(getters, key=lambda cls: cls.__name__.lower())

getter_dict: Mapping[str, Type[Getter]] = {
    norm(getter.name): getter
    for getter in getters
}


def resolve(name: str, use_cache: bool = True) -> Bioversion:
    """Resolve the database name to a :class:`Bioversion` instance."""
    if use_cache:
        return _resolve_helper_cached(name)
    else:
        return _resolve_helper(name)


@refresh_daily
def _resolve_helper_cached(name: str) -> Bioversion:
    return _resolve_helper(name)


def _resolve_helper(name: str) -> Bioversion:
    norm_name = norm(name)
    getter: Type[Getter] = getter_dict[norm_name]
    return getter.resolve()


def get_version(name: str) -> str:
    """Resolve a database name to its version string."""
    return resolve(name).version


def get_rows() -> List[Bioversion]:
    """Get the rows, refreshing once per day."""
    return list(_iter_versions())


def _iter_versions() -> Iterable[Bioversion]:
    for name in getter_dict:
        yield resolve(name)
