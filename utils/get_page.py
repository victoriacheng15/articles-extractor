import httpx
import asyncio
import logging
import time
from bs4 import BeautifulSoup
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PageFetcher:
    def __init__(self):
        self.last_request_time = 0
        self.request_interval = 1.0
        self.client = httpx.AsyncClient(timeout=30.0, http2=True)

    async def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage with rate limiting"""
        # Rate limiting
        elapsed = time.time() - self.last_request_time
        if elapsed < self.request_interval:
            await asyncio.sleep(self.request_interval - elapsed)

        try:
            response = await self.client.get(url)
            self.last_request_time = time.time()

            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")

            logger.error(f"HTTP {response.status_code} from {url}")
            return None

        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return None

    async def close(self):
        await self.client.aclose()
