import asyncio
import collections
from typing import Optional, Union, Mapping, Dict

import aiohttp
import xmltodict

from aio_goodreads.types.author import GoodreadsAuthor
from aio_goodreads.types.book import GoodreadsBook
from .utils import exceptions

API_URL = 'https://www.goodreads.com/'


class GoodreadsClient:
    def __init__(self,
                 key: str,
                 secret: str,
                 loop: Optional[Union[asyncio.BaseEventLoop, asyncio.AbstractEventLoop]] = None):
        self.key = key
        self.secret = secret

        self.loop = loop
        self._session: Optional[aiohttp.ClientSession] = None

    def get_new_session(self) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(
            loop=self.loop
        )

    @property
    def session(self) -> Optional[aiohttp.ClientSession]:
        if self._session is None or self._session.closed:
            self._session = self.get_new_session()
        return self._session

    @property
    def query_dict(self):
        return {'key': self.key}

    async def request(self,
                      method: str,
                      url: str,
                      params: Optional[Dict[str, str]] = None,
                      **kwargs) -> Optional[dict]:
        if not params:
            params = self.query_dict
        else:
            params = self.query_dict | params

        try:
            async with self.session as session:
                async with session.request(method, f'{API_URL}{url}', params=params, **kwargs) as response:
                    if response.status == 200:
                        data_dict = xmltodict.parse(await response.read())
                        return data_dict['GoodreadsResponse']
                    else:
                        return None
        except aiohttp.ClientError as e:
            raise exceptions.NetworkError(f"aiohttp client throws an error: {e.__class__.__name__}: {e}")

    async def get(self,
                  url: str,
                  params: Optional[Mapping[str, str]] = None,
                  **kwargs):
        return await self.request('GET', url, params=params, **kwargs)

    async def post(self,
                   url: str,
                   params: Optional[Mapping[str, str]] = None,
                   **kwargs):
        return await self.request('POST', url, params=params, **kwargs)

    async def get_author(self, id):
        """Get info about an author"""
        response = await self.get('author/show', params={'id': id})
        return GoodreadsAuthor(response['author'], self)

    async def find_author(self, name):
        """Find an author by name"""
        response = await self.get(f'api/author_url/{name}')
        return self.get_author(response['author']['@id']) if 'author' in response else None

    async def get_book(self, id=None, isbn=None):
        """Get info about a book"""
        if id:
            response = await self.get('book/show', params={'id': id})
            return GoodreadsBook(response['book'], self)
        elif isbn:
            response = await self.get('book/isbn', params={'isbn': isbn})
            return GoodreadsBook(response['book'], self)
        else:
            raise exceptions.GoodreadsClientException('id or isbn is required')

    async def search_books(self, q: str, page: int = 1, search_field='all'):
        """Get the most popular books for the given query. This will search all
        books in the title/author/ISBN fields and show matches, sorted by
        popularity on Goodreads.
        :param q: query text
        :param page: which page to return (default 1)
        :param search_field: field to search, one of 'title', 'author' or
        'genre' (default is 'all')
        """
        response = await self.get('search/index.xml',
                                  params={'q': q, 'page': page, 'search[field]': search_field})
        works = response['search']['results']['work']
        # If there's only one work returned, put it in a list.
        if type(works) == collections.OrderedDict:
            works = [works]
        return [await self.get_book(work['best_book']['id']['#text']) for work in works]
