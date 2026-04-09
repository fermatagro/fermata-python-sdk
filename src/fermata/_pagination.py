from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class Page(Generic[T]):
    """A single page of results from a paginated endpoint."""

    items: list[T]
    next_cursor: str | None


class AsyncPaginator(Generic[T]):
    """Auto-paginating async iterator over cursor-based responses.

    Usage:
        async for item in paginator:
            print(item)

        # Or fetch a single page manually:
        page = await paginator.first_page(limit=50)
    """

    def __init__(self, fetch_page: Callable[..., Awaitable[Page[T]]], **kwargs: object) -> None:
        self._fetch_page = fetch_page
        self._kwargs = kwargs
        self._buffer: list[T] = []
        self._cursor: str | None = None
        self._exhausted = False
        self._started = False

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
        if self._buffer:
            return self._buffer.pop(0)

        if self._exhausted and self._started:
            raise StopAsyncIteration

        page = await self._fetch_page(cursor=self._cursor, **self._kwargs)
        self._started = True
        self._cursor = page.next_cursor
        if page.next_cursor is None:
            self._exhausted = True

        if not page.items:
            raise StopAsyncIteration

        self._buffer = page.items[1:]
        return page.items[0]

    async def first_page(self, *, limit: int = 100) -> Page[T]:
        """Fetch a single page without auto-iteration."""
        return await self._fetch_page(cursor=None, limit=limit, **self._kwargs)


class SyncPaginator(Generic[T]):
    """Sync wrapper around AsyncPaginator."""

    def __init__(self, async_paginator: AsyncPaginator[T], run: Callable[..., T]) -> None:
        self._async = async_paginator
        self._run = run

    def __iter__(self) -> Iterator[T]:
        return self

    def __next__(self) -> T:
        try:
            return self._run(self._async.__anext__())
        except StopAsyncIteration:
            raise StopIteration from None

    def first_page(self, *, limit: int = 100) -> Page[T]:
        """Fetch a single page without auto-iteration."""
        return self._run(self._async.first_page(limit=limit))
