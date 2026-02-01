import os
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar
from typing import Literal

import requests

from libs.cache import Cache
from .response import HitModel

current_dir_path = os.path.dirname(os.path.realpath(__file__))


class HackerNewsTag(str, Enum):
    STORY = "story"
    COMMENT = "comment"
    POLL = "poll"
    # noinspection SpellCheckingInspection
    POLLOPT = "pollopt"
    SHOW_HN = "show_hn"
    ASK_HN = "ask_hn"
    FRONT_PAGE = "front_page"
    AUTHOR_ID = "author_:{username}"
    STORY_ID = "story_:{id}"


class HackerNewsNumericFiltersKey(str, Enum):
    CREATED_AT_I = "created_at_i"
    POINTS = "points"
    NUM_COMMENTS = "num_comments"


@dataclass
class HackerNewsNumericFilter:
    key: HackerNewsNumericFiltersKey
    condition: Literal["<", "<=", "=", ">", ">="]
    value: int

    def to_param(self) -> str:
        return f"{self.key.value}{self.condition}{self.value}"


@dataclass
class HackerNews:
    """Hacker News API"""

    cache = Cache(directory=f"{current_dir_path}/cache")

    BASE_DOMAIN: ClassVar[str] = "hn.algolia.com"
    SEARCH_BY_DATE: ClassVar[str] = "/api/v1/search_by_date"
    TIME_OUT: ClassVar[int] = 1000

    def create_search_by_date_url(
        self,
        tags: HackerNewsTag | list[HackerNewsTag] | None = None,
        numeric_filters: list[HackerNewsNumericFilter] | None = None,
    ) -> str:
        """Create url for search by date
        :param tags: story, comment, poll, pollopt, show_hn, ask_hn, front_page
        :param numeric_filters: created_at_i, points, num_comments, objectID
        """
        url = f"https://{self.BASE_DOMAIN}{self.SEARCH_BY_DATE}"

        if tags:
            if isinstance(tags, list):
                tags_query = f"({','.join(map(lambda tag: tag.value, tags))})"
            else:
                tags_query = tags.value
            url += f"?tags={tags_query}"
        if numeric_filters:
            url += "&numericFilters=" f"{','.join(map(lambda filter_: filter_.to_param(), numeric_filters))}"
        return url

    def search_by_date(
        self,
        tags: HackerNewsTag | list[HackerNewsTag] | None = None,
        numeric_filters: list[HackerNewsNumericFilter] | None = None,
        bypass_cache: bool = False,
        cache_expire_sec: int | None = None,
    ) -> HitModel:
        """Search by date
        :param tags: story, comment, poll, pollopt, show_hn, ask_hn, front_page
        :param numeric_filters: created_at_i, points, num_comments, objectID
        :param bypass_cache: if True, fetch from API without cache
        :param cache_expire_sec: if bypass_cache is False, cache expire time
        """
        result = None

        if not bypass_cache:
            result = self.cache.load_latest_json(expire_sec=cache_expire_sec)

        if result is None:
            print("Fetching from API.")
            response_ = requests.get(
                self.create_search_by_date_url(tags, numeric_filters),
                timeout=self.TIME_OUT,
            )
            if response_.status_code < 200 or 300 <= response_.status_code:
                raise ValueError(f"Failed to fetch search_by_date. Code: {response_.status_code}")
            result = response_.json()
            if not bypass_cache:
                self.cache.save_json(data=result)

        return HitModel.model_validate(obj=result)
