import asyncio
import re
from typing import Set, List
from urllib.parse import urlparse, urljoin

import aiohttp


class AsyncCrawler:
    def __init__(self, max_depth: int = 3):
        self.max_depth = max_depth
        self.visited_urls: Set[str] = set()
        self.external_links: Set[str] = set()
        self.session = None
        self.base_domain = ''

    async def fetch(self, url: str) -> str:
        async with self.session.get(url) as response:
            return await response.text()

    def extract_links(self, html: str, base_url: str) -> Set[str]:
        links = set()
        pattern = re.compile(r'href=["\'](.*?)["\']', re.IGNORECASE)
        for match in pattern.finditer(html):
            link = match.group(1)
            absolute_link = urljoin(base_url, link)
            parsed_link = urlparse(absolute_link)
            if parsed_link.scheme in ('http', 'https'):
                links.add(absolute_link)
        return links

    def is_external(self, url: str) -> bool:
        parsed_url = urlparse(url)
        return parsed_url.netloc != self.base_domain and parsed_url.netloc != ''

    async def crawl(self, url: str, depth: int = 0):
        if depth > self.max_depth or url in self.visited_urls:
            return

        self.visited_urls.add(url)
        print(f'Crawling: {url} (depth {depth})')

        try:
            html = await self.fetch(url)
            links = self.extract_links(html, url)

            for link in links:
                if self.is_external(link):
                    self.external_links.add(link)
                else:
                    await self.crawl(link, depth + 1)

        except Exception as e:
            print(f'Error crawling {url}: {str(e)}')

    async def run(self, start_urls: List[str], output_file: str = 'links.txt'):
        async with aiohttp.ClientSession() as self.session:
            if not start_urls:
                return

            self.base_domain = urlparse(start_urls[0]).netloc
            tasks = [self.crawl(url) for url in start_urls]
            await asyncio.gather(*tasks)

        with open(output_file, 'w') as f:
            for link in sorted(self.external_links):
                f.write(f'{link}\n')

        print(f'Found {len(self.external_links)} external links')
        print(f'Results saved to {output_file}')


async def main():
    crawler = AsyncCrawler(max_depth=3)
    await crawler.run(
        start_urls=['https://doodles.google'], output_file='external_links.txt'
    )


if __name__ == '__main__':
    asyncio.run(main())
