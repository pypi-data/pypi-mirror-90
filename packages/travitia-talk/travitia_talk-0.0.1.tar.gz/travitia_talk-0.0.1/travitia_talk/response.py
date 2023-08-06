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

from __future__ import annotations

from typing import Any, Dict, Sequence

from .enums import Emotion


class Response:
    """Text response from API"""

    __slots__ = (
        "text",
        "status",
        "emotion",
        "context",
    )

    def __init__(
        self, text: str, status: str, emotion: Emotion, context: Sequence[str]
    ):
        self.text = text
        # not sure why status exists
        self.status = status
        self.emotion = emotion
        self.context = context

    @classmethod
    def from_data(
        cls, data: Dict[str, Any], emotion: Emotion, context: Sequence[str]
    ) -> Response:
        return cls(data["response"], data["status"], emotion, context)

    def __str__(self) -> str:
        return self.text

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} status= {self.status} text={self.text} emotion={self.emotion} context={self.context}>"
