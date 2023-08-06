"""
MIT License

Copyright (c) 2021 Eugene

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import abc

from typing import Any, Dict, Deque, Sequence
from collections import deque


class Context(abc.ABC):
    """Context is used to store previous user queries"""

    def __init__(self, max_length: int = 2) -> None:
        self.max_length = max_length

    async def push(self, id: Any, text: str) -> Sequence[str]:
        context = await self.get(id)
        await self.add(id, text)

        return context

    @abc.abstractmethod
    async def add(self, id: Any, text: str) -> None:
        ...

    @abc.abstractmethod
    async def get(self, id: Any) -> Sequence[str]:
        ...

    @abc.abstractmethod
    async def remove(self, id: Any) -> None:
        ...


class InMemoryContext(Context):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

        self._entries: Dict[Any, Deque[str]] = {}

    async def add(self, id: Any, text: str) -> None:
        if id in self._entries:
            self._entries[id].append(text)
        else:
            self._entries[id] = deque([text], self.max_length)

    async def get(self, id: Any) -> Sequence[str]:
        return self._entries.get(id, [])

    async def remove(self, id: Any) -> None:
        if id in self._entries:
            del self._entries[id]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} size: {len(self._entries)}>"


class NoContext(Context):
    async def add(self, id: Any, text: str) -> None:
        pass

    async def get(self, id: Any) -> Sequence[str]:
        return []

    async def remove(self, id: Any) -> None:
        pass
