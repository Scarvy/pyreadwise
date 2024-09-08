from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ReadwiseTag(BaseModel):
    """Represents a Readwise tag."""

    id: int
    name: str


class ReadwiseBook(BaseModel):
    """Represents a Readwise book."""

    id: int
    title: str
    author: str
    category: str
    source: str
    num_highlights: int
    last_highlight_at: datetime
    updated: datetime
    cover_image_url: str
    highlights_url: str
    source_url: str
    asin: str
    tags: List[ReadwiseTag]
    document_note: str


class ReadwiseHighlight(BaseModel):
    """Represents a Readwise highlight."""

    id: int
    text: str
    note: str
    location: int
    location_type: str
    highlighted_at: Optional[datetime] = None
    url: Optional[str] = None
    color: str
    updated: Optional[datetime] = None
    book_id: int
    tags: List[ReadwiseTag]


class ReadwiseExportHighlight(BaseModel):
    """Represents a Readwise highlight export."""

    id: int
    text: str
    location: int | None
    location_type: str | None
    note: str
    color: str
    highlighted_at: datetime | None
    created_at: datetime | None
    updated_at: datetime | None
    external_id: str | None
    book_id: int
    readwise_url: str
    tags: List[ReadwiseTag] = Field(default_factory=list)
    is_favorite: bool = False
    is_discard: bool = False
    url: Optional[str] = None
    end_location: Optional[int] = None


class ReadwiseExportResults(BaseModel):
    """Represents a Readwise export result."""

    user_book_id: int
    title: str
    author: str
    readable_title: str
    source: str
    cover_image_url: str
    unique_url: str | None
    category: str
    document_note: str | None
    summary: str | None
    readwise_url: str
    source_url: str | None
    book_tags: List[ReadwiseTag] = Field(default_factory=list)
    highlights: List[ReadwiseExportHighlight] = Field(default_factory=list)
    asin: Optional[str] = None


class DailyReviewHighlight(BaseModel):
    """Represents a Readwise Daily Review highlight."""

    text: str
    title: str
    author: str
    url: str
    source_url: str
    source_type: str
    category: str
    location_type: str
    location: int
    note: str
    highlighted_at: Optional[datetime] = None
    highlight_url: str
    image_url: str
    id: int
    api_source: str


class ReadwiseDailyReview(BaseModel):
    """Represents a Readwise Daily Review."""

    review_id: int
    review_url: str
    review_completed: bool
    highlights: List[Dict[str, Any]]


class ReadwiseReaderDocument(BaseModel):
    """Represents a Readwise Reader Document."""

    id: str
    url: str
    source_url: str
    title: str
    author: str
    source: str
    category: str
    location: str
    tags: Dict[str, Any]
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
