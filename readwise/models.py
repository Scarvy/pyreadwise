from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Optional


@dataclass
class ReadwiseTag:
    """Represents a Readwise tag."""

    id: str
    name: str


@dataclass
class ReadwiseBook:
    """
    Represents a Readwise book.
    """

    id: str
    title: str
    author: str
    category: str
    source: str
    num_highlights: int
    cover_image_url: str
    highlights_url: str
    source_url: str
    document_note: str


@dataclass
class ReadwiseHighlight:
    """
    Represents a Readwise highlight.
    """

    id: str
    text: str
    note: str
    location: int
    location_type: str
    url: str | None
    color: str
    updated: datetime | None
    book_id: str
    tags: list[ReadwiseTag]


@dataclass
class ReadwiseExportHighlight:
    """
    Represents a Readwise highlight.
    """

    id: int
    text: str
    location: int
    location_type: str
    note: str
    color: str
    highlighted_at: str
    created_at: str
    updated_at: str
    external_id: str
    book_id: int
    readwise_url: str
    tags: List[ReadwiseTag] = field(default_factory=list)
    is_favorite: bool = False
    is_discard: bool = False
    url: Optional[str] = None
    end_location: Optional[int] = None


@dataclass
class ReadwiseExportResults:
    user_book_id: str
    title: str
    author: str
    readable_title: str
    source: str
    cover_image_url: str
    unique_url: str
    category: str
    document_note: str
    summary: str
    readwise_url: str
    source_url: str
    book_tags: List[ReadwiseTag] = field(default_factory=list)
    highlights: List[ReadwiseExportHighlight] = field(default_factory=list)
    asin: Optional[str] = None


@dataclass
class ReadwiseReaderDocument:
    id: str
    url: str
    source_url: str
    title: str
    author: str
    source: str
    category: str
    location: str
    tags: dict[str, Any]
    site_name: str
    word_count: int
    created_at: datetime
    updated_at: datetime
    notes: str
    published_date: str
    summary: str
    image_url: str
    reading_progress: float
    parent_id: Optional[str] = None
