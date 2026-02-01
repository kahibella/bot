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
    default_points_threshold: int = 200
    default_created_at_threshold_sec: int = 1 * 60 * 60  # 1 hour

    @staticmethod
    def current_timestamp_sec() -> int:
        return int(time())

    def hot_news(
        self,
        points_threshold: int | None = None,
        created_at_threshold_sec: int | None = None,
        bypass_cache: bool = False,
    ) -> HitModel:
        """get hot news from hacker news
        :param points_threshold: points threshold
        :param created_at_threshold_sec: created at threshold
        :param bypass_cache: if True, bypass cache. cache_expire_sec is ignored.
        """
        return self.hacker_news.search_by_date(
            tags=HackerNewsTag.STORY,
            numeric_filters=[
                HackerNewsNumericFilter(
                    key=HackerNewsNumericFiltersKey.POINTS,
                    condition=">=",
                    value=points_threshold or self.default_points_threshold,
                ),
                HackerNewsNumericFilter(
                    key=HackerNewsNumericFiltersKey.CREATED_AT_I,
                    condition=">=",
                    value=self.current_timestamp_sec()
                    - (created_at_threshold_sec or self.default_created_at_threshold_sec),
                ),
            ],
            bypass_cache=bypass_cache,
            cache_expire_sec=self.cache_expire_sec,
        )
