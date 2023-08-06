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

import logging

from typing import Any, Optional, Sequence

from aiohttp import ClientSession

from .enums import Emotion
from .errors import APIError, UnknownAPIError
from .context import Context, InMemoryContext
from .response import Response

log = logging.getLogger(__name__)


class ChatBot:
    """Main wrapper class"""

    def __init__(
        self,
        token: str,
        *,
        api_url: str = "https://public-api.travitia.xyz/talk",
        session: Optional[ClientSession] = None,
        context: Optional[Context] = None,
    ):
        self._token = token
        self._api_url = api_url

        self._session = session
        self._context = InMemoryContext() if context is None else context

        self._headers = {"authorization": token}

    async def _ensure_session(self) -> ClientSession:
        if self._session is None:
            self._session = ClientSession()

        return self._session

    async def ask(
        self,
        text: str,
        *,
        id: Any = None,
        context: Optional[Sequence[str]] = None,
        emotion: Emotion = Emotion.neutral,
    ) -> Response:
        """
        Send query and get response.

        Prameters:
            id: session id to get context from
            context: overwrites context
            emotion: emotion to use
        """

        session = await self._ensure_session()

        if context is not None:
            context = []
        elif id is not None:
            context = await self._context.push(id, text)
        else:
            context = []

        data = {
            "text": text,
            "emotion": emotion.value,
            "context": context,
        }

        async with session.post(self._api_url, headers=self._headers, data=data) as r:
            if r.status != 200:
                try:
                    data = await r.json()
                except Exception as e:
                    data = {}
                    log.error(f"Error reading error data: {e}")

                if "response" not in data:
                    raise UnknownAPIError("Bad response from server", status=r.status)

                raise APIError(data["response"], status=r.status)

            return Response.from_data(await r.json(), emotion, context)

    async def close(self) -> None:
        """
        Close internal session.

        Note that it closes custom session if you used one.
        """

        if self._session is not None:
            await self._session.close()
