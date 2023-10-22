# -*- coding:utf-8 -*-
"""Model classes module."""
from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version as pkg_version
from typing import Text

import pyshorteners

from pypisearch.constants import DESCRIPTION_RE, NAME_RE, VERSION_RE


class ResultItem:
    """Result item instance of search."""

    def __init__(self, plain_text: Text):
        self.plain_text = plain_text

    @property
    def is_empty(self) -> bool:
        """Check is current instance empty."""
        return not all([self.name, self.version])

    @property
    def name(self) -> Text:
        """Returns item name."""
        name = NAME_RE.findall(self.plain_text)
        return name[0] if name else ""

    @property
    def version(self) -> Text:
        """Returns item version."""
        version = VERSION_RE.findall(self.plain_text)
        return version[0] if version else ""

    @property
    def description(self) -> Text:
        """Description attribute.

        :return: package description attribute.
        """
        description = DESCRIPTION_RE.findall(self.plain_text)
        return description[0] if description else ""

    @property
    def is_installed(self) -> bool:
        """Check if current package is installed or not.

        :return: True if package is installed, False otherwise.
        """
        try:
            pkg_version(self.name)
        except PackageNotFoundError:
            return False
        else:
            return True

    @property
    def get_installed_version(self) -> Text:
        """Installed version attribute.

        :return: a str instance with the current version installed.
        """
        return pkg_version(self.name) if self.is_installed else ""

    @property
    def installed_description(self) -> Text:
        """Installed version description attribute.

        :return: a str instance with the current version installed.
        """
        return (
            f"[installed {self.get_installed_version}] "
            if self.is_installed
            else ""
        )

    @property
    def pypi_url(self) -> Text:
        """URL pointing to package project attribute.

        :return: a str instance URL pointing to package project attribute.
        """
        return f'https://pypi.org/project/{self.name}/'

    @property
    def short_pypi_url(self) -> Text:
        """A Tiny version of URL package project."""
        url_shorter = pyshorteners.Shortener()
        tinyurl = url_shorter.tinyurl
        return tinyurl.short(f'https://pypi.org/project/{self.name}/')

    def __str__(self):
        return f'{self.name}<{self.version}>'

    def __repr__(self):
        return f'Pkg<{self.name}|{self.version}>'
