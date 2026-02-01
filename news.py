import os
from time import time
from dataclasses import dataclass


from hacker_news import HackerNews
from hacker_news import HackerNewsNumericFilter
from hacker_news import HackerNewsNumericFiltersKey
from hacker_news import HackerNewsTag
from hacker_news import HitModel


@dataclass
class News:
    hacker_news = HackerNews()

    cache_expire_sec: int = 60 * 60  # 1 hour

    @staticmethod
    def current_timestamp_sec() -> int:
        return int(time())

    def hot_news(
        self,
        bypass_cache: bool = False,
    ) -> HitModel:
        """get hot news from hacker news
        :param bypass_cache: if True, bypass cache. cache_expire_sec is ignored.
        """
        return self.hacker_news.search_by_date(
            tags=HackerNewsTag.STORY,
            numeric_filters=[
                HackerNewsNumericFilter(
                    key=HackerNewsNumericFiltersKey.POINTS,
                    condition=">=",
                    value=int(os.getenv("NEWS_POINTS_THRESHOLD") or 200),
                ),
                HackerNewsNumericFilter(
                    key=HackerNewsNumericFiltersKey.CREATED_AT_I,
                    condition=">=",
                    value=self.current_timestamp_sec() - (int(os.getenv("NEWS_CREATED_AT_THRESHOLD_SEC") or 3600)),
                ),
            ],
            bypass_cache=bypass_cache,
            cache_expire_sec=self.cache_expire_sec,
        )
