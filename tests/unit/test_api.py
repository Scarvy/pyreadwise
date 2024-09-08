from datetime import datetime
from unittest.mock import Mock, patch

from requests import Session

from readwise.api import Readwise, ReadwiseReader

readwise_client = Readwise("test_token")
readwise_reader = ReadwiseReader("test_token")


@patch.object(Session, "request")
def test_paging(mock_get):
    page1 = Mock()
    page1.status_code = 200
    page1.json.return_value = {
        "next": "https://example.com/api/v2/books/?page=2",
        "results": [
            {
                "id": 1,
                "title": "Test Book",
            }
        ],
    }

    page2 = Mock()
    page2.status_code = 200
    page2.json.return_value = {
        "next": None,
        "results": [
            {
                "id": 2,
                "title": "Test Book 2",
            }
        ],
    }

    mock_get.side_effect = [
        page1,
        page2,
    ]

    generator = readwise_client.get_pagination("test/")
    assert next(generator) == page1.json.return_value
    assert next(generator) == page2.json.return_value


@patch.object(Session, "request")
def test_get_books_empty(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"results": [], "next": None}
    highlights = list(readwise_client.get_books("articles"))
    assert len(highlights) == 0


@patch.object(Session, "request")
def test_get_books(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "next": None,
        "results": [
            {
                "id": 1,
                "title": "Test Book",
                "author": "Test Author",
                "category": "article",
                "source": "Test Source",
                "num_highlights": 1,
                "last_highlight_at": "2022-12-27T11:33:09Z",
                "updated": "2020-01-01T00:00:00Z",
                "cover_image_url": "https://example.com/image.jpg",
                "highlights_url": "https://example.com/highlights",
                "source_url": "https://example.com/source",
                "asin": "test_asin",
                "tags": [
                    {"id": 1, "name": "test_tag"},
                    {"id": 2, "name": "test_tag_2"},
                ],
                "document_note": "test_note",
            }
        ],
    }
    books = list(readwise_client.get_books("articles"))
    assert len(books) == 1
    assert books[0].id == 1
    assert books[0].title == "Test Book"
    assert books[0].author == "Test Author"
    assert books[0].category == "article"
    assert books[0].source == "Test Source"
    assert books[0].num_highlights == 1
    assert books[0].last_highlight_at == datetime.fromisoformat("2022-12-27T11:33:09Z")
    assert books[0].updated == datetime.fromisoformat("2020-01-01T00:00:00Z")
    assert books[0].cover_image_url == "https://example.com/image.jpg"
    assert books[0].highlights_url == "https://example.com/highlights"
    assert books[0].source_url == "https://example.com/source"
    assert books[0].asin == "test_asin"
    assert len(books[0].tags) == 2
    assert books[0].tags[0].id == 1
    assert books[0].tags[0].name == "test_tag"
    assert books[0].tags[1].id == 2
    assert books[0].tags[1].name == "test_tag_2"
    assert books[0].document_note == "test_note"


@patch.object(Session, "request")
def test_get_book_highlights_empty(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "next": None,
        "results": [],
    }
    highlights = list(readwise_client.get_book_highlights("1"))
    assert len(highlights) == 0


@patch.object(Session, "request")
def test_get_book_highlights(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "next": None,
        "results": [
            {
                "id": 1,
                "text": "Test Highlight",
                "note": "Test Note",
                "location": 1,
                "location_type": "page",
                "url": "https://example.com/highlight",
                "color": "yellow",
                "updated": "2020-01-01T00:00:00Z",
                "book_id": 1,
                "tags": [
                    {"id": 1, "name": "test_tag"},
                    {"id": 2, "name": "test_tag_2"},
                ],
            }
        ],
    }
    highlights = list(readwise_client.get_book_highlights("1"))
    assert len(highlights) == 1
    assert highlights[0].id == 1
    assert highlights[0].text == "Test Highlight"
    assert highlights[0].note == "Test Note"
    assert highlights[0].location == 1
    assert highlights[0].location_type == "page"
    assert highlights[0].url == "https://example.com/highlight"
    assert highlights[0].color == "yellow"
    assert highlights[0].updated == datetime.fromisoformat("2020-01-01T00:00:00Z")
    assert highlights[0].book_id == 1
    assert len(highlights[0].tags) == 2
    assert highlights[0].tags[0].id == 1
    assert highlights[0].tags[0].name == "test_tag"
    assert highlights[0].tags[1].id == 2
    assert highlights[0].tags[1].name == "test_tag_2"


@patch.object(Session, "request")
def test_get_export_highlights(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "count": 1,
        "nextPageCursor": None,
        "results": [
            {
                "user_book_id": 1,
                "title": "Test Book",
                "author": "Test Author",
                "readable_title": "Test Book",
                "source": "Test Source",
                "cover_image_url": "https://example.com/image.jpg",
                "unique_url": "https://example.com/highlights",
                "book_tags": [
                    {"id": 1, "name": "test_tag"},
                    {"id": 2, "name": "test_tag_2"},
                ],
                "category": "article",
                "document_note": "test_note",
                "summary": "",
                "readwise_url": "https://example.com/readwise",
                "source_url": "https://example.com/source",
                "asin": None,
                "highlights": [
                    {
                        "id": 1,
                        "text": "Test Highlight",
                        "location": 1,
                        "location_type": "page",
                        "note": "Test Note",
                        "color": "yellow",
                        "highlighted_at": "2020-01-01T00:00:00Z",
                        "created_at": "2020-01-01T00:00:00Z",
                        "updated_at": "2020-01-01T00:00:00Z",
                        "external_id": "test_id",
                        "end_location": None,
                        "url": None,
                        "book_id": 1,
                        "tags": [
                            {"id": 1, "name": "test_tag"},
                            {"id": 2, "name": "test_tag_2"},
                        ],
                        "is_favorite": False,
                        "is_discard": False,
                        "readwise_url": "https://example.com/readwise",
                    }
                ],
            }
        ],
    }
    export = list(readwise_client.get_export_highlights())
    assert len(export) == 1
    assert export[0].user_book_id == 1
    assert export[0].title == "Test Book"
    assert export[0].author == "Test Author"
    assert export[0].readable_title == "Test Book"
    assert export[0].source == "Test Source"
    assert export[0].cover_image_url == "https://example.com/image.jpg"
    assert export[0].unique_url == "https://example.com/highlights"
    assert len(export[0].book_tags) == 2
    assert export[0].book_tags[0].id == 1
    assert export[0].book_tags[0].name == "test_tag"
    assert export[0].book_tags[1].id == 2
    assert export[0].book_tags[1].name == "test_tag_2"
    assert export[0].category == "article"
    assert export[0].document_note == "test_note"
    assert export[0].summary == ""
    assert export[0].readwise_url == "https://example.com/readwise"
    assert export[0].source_url == "https://example.com/source"
    assert export[0].asin is None
    assert len(export[0].highlights) == 1
    assert export[0].highlights[0].id == 1
    assert export[0].highlights[0].text == "Test Highlight"
    assert export[0].highlights[0].location == 1
    assert export[0].highlights[0].location_type == "page"
    assert export[0].highlights[0].note == "Test Note"
    assert export[0].highlights[0].color == "yellow"
    assert export[0].highlights[0].highlighted_at == datetime.fromisoformat(
        "2020-01-01T00:00:00Z"
    )
    assert export[0].highlights[0].created_at == datetime.fromisoformat(
        "2020-01-01T00:00:00Z"
    )
    assert export[0].highlights[0].updated_at == datetime.fromisoformat(
        "2020-01-01T00:00:00Z"
    )
    assert export[0].highlights[0].external_id == "test_id"
    assert export[0].highlights[0].end_location is None
    assert export[0].highlights[0].url is None
    assert export[0].highlights[0].book_id == 1
    assert len(export[0].highlights[0].tags) == 2
    assert export[0].highlights[0].tags[0].id == 1
    assert export[0].highlights[0].tags[0].name == "test_tag"
    assert export[0].highlights[0].tags[1].id == 2
    assert export[0].highlights[0].tags[1].name == "test_tag_2"
    assert export[0].highlights[0].is_favorite is False
    assert export[0].highlights[0].is_discard is False
    assert export[0].highlights[0].readwise_url == "https://example.com/readwise"
