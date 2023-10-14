from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict
    from .config import Config
    from .http_client import HTTPClient
    from .media import Metadata, Series, Movie, LiveTV

from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from devgoldyutils import LoggerAdapter

from . import mov_cli_logger, errors

__all__ = ("Scraper", "MediaNotFound")

class Scraper(ABC):
    def __init__(self, config: Config, http_client: HTTPClient) -> None:
        """A base class for building scrapers from."""
        self.config = config
        self.http_client = http_client
        self.logger = LoggerAdapter(mov_cli_logger, prefix = self.__class__.__name__)

        super().__init__()

    def soup(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, self.config.parser)

    @abstractmethod
    def scrape(self, metadata: Metadata, season: int = None, episode: int = None) -> Series | Movie | LiveTV:
        """
        Where your searching and scraping for the media should be performed done. 
        Should return an instance of Media.
        """
        ...

    @abstractmethod
    def scrape_metadata_episodes(self, metadata: Metadata) -> Dict[int | None, int]:
        """Returns episode count for each season in that Movie/Series."""
        ...


class MediaNotFound(errors.MovCliException):
    """Raises when a scraper fails to find a show/movie/tv-station."""
    def __init__(self, message, scraper: Scraper) -> None:
        super().__init__(
            f"Failed to find media: {message}",
            logger = scraper.logger
        )