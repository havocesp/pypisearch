# -*- coding:utf-8 -*-
"""Custom pip-search utility by pypi search line."""
import argparse
import re

from pypisearch.search import Search


def main() -> None:
    """Main program entrypoint."""

    # Get command arguments
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "q", nargs='+', help="Query for search"
    )
    ap.add_argument(
        "-p",
        "--page",
        default="1",
        metavar="page",
        type=str,
        help="Starting page (default 1, could be range of pages like 1-5)",
    )
    args = ap.parse_args()

    if '-' in f'{args.page}':
        # noinspection RegExpAnonymousGroup
        page_range = re.search(r'^(\d+)-(\d+)$', args.page)
        page_from, page_to = page_range.groups()
        if page_from < page_to:
            raise ValueError("Page from shouldn't be greater then page to.")
    elif args.page.isnumeric():
        page_from = args.page
        page_to = None
    else:
        raise ValueError('Invalid page range or supplied page is not a integer,')

    # noinspection RegExpAnonymousGroup
    query = re.sub(r'[\t ]{2,}', ' ', ''.join(args.q).strip())
    # Parse search url and print result table
    search = Search(query=query, page_from=page_from, page_to=page_to)
    print(search.tabulated_result or "No results")


if __name__ == "__main__":
    main()
