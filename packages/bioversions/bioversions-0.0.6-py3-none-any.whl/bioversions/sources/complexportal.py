# -*- coding: utf-8 -*-

"""A getter for Complex Portal."""

from bioversions.utils import Getter, _get_ftp_date_version

__all__ = [
    'ComplexPortalGetter',
]


class ComplexPortalGetter(Getter):
    """A getter for Complex Portal."""

    name = 'Complex Portal'
    homepage_fmt = 'ftp://ftp.ebi.ac.uk/pub/databases/intact/complex/{version}/'

    def get(self):
        """Get the latest ComplexPortal version number."""
        return _get_ftp_date_version('ftp.ebi.ac.uk', 'pub/databases/intact/complex/')


if __name__ == '__main__':
    ComplexPortalGetter.print()
