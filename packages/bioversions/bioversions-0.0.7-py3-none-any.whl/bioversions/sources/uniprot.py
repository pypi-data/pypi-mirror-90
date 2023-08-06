# -*- coding: utf-8 -*-

"""A getter for UniProt."""

from xml.etree import ElementTree  # noqa:S405

import requests
import requests_ftp

from bioversions.utils import Getter

__all__ = [
    'UniProtGetter',
]

requests_ftp.monkeypatch_session()


class UniProtGetter(Getter):
    """A getter for UniProt."""

    name = 'UniProt'
    homepage_fmt = 'ftp://ftp.uniprot.org/pub/databases/uniprot/previous_releases/release-{version}/'
    date_version_fmt = '%Y_%m'

    def get(self):
        """Get the latest UniProt version number."""
        session = requests.Session()
        f = session.get('ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/RELEASE.metalink')
        tree = ElementTree.fromstring(f.text)  # noqa:S314
        version_tag = tree.find('{http://www.metalinker.org/}version')
        return version_tag.text


if __name__ == '__main__':
    UniProtGetter.print()
