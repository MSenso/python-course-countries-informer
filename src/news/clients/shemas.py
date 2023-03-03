"""
Описание моделей данных (DTO).
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NewsItemDTO(BaseModel):
    """
    Модель данных для представления новости.

    .. code-block::
        NewsItemDTO(
            source="Google News",
            author="Коммерсантъ",
            title="Теннисист Андрей Рублев вышел в четвертьфинал Dubai Duty Free - Коммерсантъ",
            description="",
            url="https://news.google.com/rss/articles/CBMiJWh0",
            published_at="2023-03-01T13:55:06Z",
        )
    """

    source: str
    author: Optional[str]
    title: str
    description: Optional[str]
    url: Optional[str]
    published_at: datetime
