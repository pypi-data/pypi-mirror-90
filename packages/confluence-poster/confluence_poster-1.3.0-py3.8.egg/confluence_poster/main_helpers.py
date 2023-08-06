from atlassian import Confluence
from dataclasses import dataclass
from confluence_poster.poster_config import Page
from typing import Union

"""File that contains procedures used inside main.py's functions"""


def check_last_updated_by(
    page_id: int, username_to_check: str, confluence_instance: Confluence
) -> (bool, str):
    """Checks which user last updated `page_id`. If it's not `username_to_check` — return False
    :param page_id: ID of the page to check
    :param username_to_check: compare this username against the one that last updated the page
    :param confluence_instance: instance of Confluence to run the check
    """
    page_last_updated_by = confluence_instance.get_page_by_id(
        page_id, expand="version"
    )["version"]["by"]
    if confluence_instance.api_version == "cloud":
        page_last_updated_by = page_last_updated_by["email"]  # pragma: no cover
    else:
        page_last_updated_by = page_last_updated_by["username"]

    return page_last_updated_by == username_to_check, page_last_updated_by


@dataclass
class PostedPage(Page):
    """Merges independently set fields with the runtime-set fields"""

    version_comment: Union[str, None] = None
