# -*- coding:utf-8 -*-
"""Search handler module"""
from typing import List, Optional, Text
from tabulate import tabulate

from pypisearch import constants as const
from pypisearch.result_item import ResultItem
from security import safe_requests


class Search:
    """Main search process instance."""

    pypi_search_url = "https://pypi.org/search/?q={query}&page={page}"

    def __init__(
        self,
        query: str,
        page_from: str = "0",
        page_to: Optional[str] = None,
    ):
        page_from, page_to = int(page_from), int(page_to) if page_to else None
        self.result = []

        if page_to is None:
            self.result = self.download_data(query=query, page=page_from)
        else:
            for page in range(page_from, page_to + 1):
                result = self.download_data(query=query, page=page)

                if not result:
                    break

                self.result.extend(result)

    def download_data(self, *, query: Text, page: int) -> List[ResultItem]:
        """

        :param query:
        :param page:
        :return:
        """
        url = self.pypi_search_url.format(query=query, page=page)
        page_data = safe_requests.get(url=url).text
        items = const.ITEM_RE.split(page_data)
        result = list(
            filter(
                lambda result_item:
                not result_item.is_empty,
                map(
                    lambda plain_item:
                    ResultItem(plain_text=plain_item),
                    items,
                ),
            )
        )

        return result

    @property
    def tabulated_result(self) -> str:
        """Returns tabulated list of results."""

        return tabulate(
            [
                [
                    f"{item.name} ({item.version})",
                    f"{item.installed_description}{item.description}",
                    f'{item.pypi_url}'
                ]
                for item in self.result
            ],
            tablefmt="plain",
        )
