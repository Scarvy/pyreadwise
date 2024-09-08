import datetime
import json
import os
from collections import Counter

import click
from click_default_group import DefaultGroup

from readwise.api import Readwise, ReadwiseReader


@click.group(cls=DefaultGroup, default="highlights")
@click.version_option()
def cli():
    """A command-line interface for the Readwise API."""


@cli.group(
    name="highlights",
)
def highlights():
    """Commands to export highlights."""


@highlights.command(name="export")
@click.option(
    "--token",
    "-t",
    help="Readwise API token.",
)
@click.option("--book_ids", "-b", help="Comma separated list of book IDs.")
@click.option(
    "--updated_after", "-u", help="Only export highlights updated after this date."
)
@click.option("--days", "-d", help="Only export highlights updated in the last N days.")
def export_highlights(token, book_ids, updated_after, days):
    """Export highlights."""

    client = Readwise(check_token(token))

    if book_ids:
        book_ids = book_ids.split(",")

    if days:
        updated_after = (
            datetime.datetime.now() - datetime.timedelta(days=int(days))
        ).isoformat()

    for results in client.export_highlights(ids=book_ids, updated_after=updated_after):
        for highlight in results.highlights:
            click.echo(
                highlight.model_dump_json(
                    include={"id", "book_id", "text", "note", "tags", "highlighted_at"},
                    indent=4,
                )
            )


@highlights.command(name="list")
@click.option("--book_ids", "-i", help="Comma separated list of book IDs.")
@click.option(
    "--updated_after",
    "-u",
    type=click.DateTime(),
    help="Only export highlights updated after this date.",
)
@click.option(
    "--updated_before",
    "-b",
    type=click.DateTime(),
    help="Only export highlights updated before this date.",
)
@click.option(
    "--highlighted_at_after",
    "-ha",
    type=click.DateTime(),
    help="Only export highlights highlighted after this date.",
)
@click.option(
    "--highlighted_at_before",
    "-hb",
    type=click.DateTime(),
    help="Only export highlights highlighted before this date.",
)
@click.option(
    "--limit", "-l", type=int, help="Limit the number of highlights to return."
)
@click.option(
    "--token",
    "-t",
    help="Readwise API token.",
)
def list_highlights(
    book_ids,
    updated_after,
    updated_before,
    highlighted_at_after,
    highlighted_at_before,
    limit,
    token,
):
    """Get highlights."""
    client = Readwise(check_token(token))

    if highlighted_at_after:
        highlighted_at_after = datetime.datetime.strptime(
            highlighted_at_after, "%Y-%m-%d"
        ).isoformat()

    if highlighted_at_before:
        highlighted_at_before = datetime.datetime.strptime(
            highlighted_at_before, "%Y-%m-%d"
        ).isoformat()

    for highlight in client.get_highlights(
        book_ids=book_ids,
        updated_after=updated_after,
        updated_before=updated_before,
        highlighted_at_after=highlighted_at_after,
        highlighted_at_before=highlighted_at_before,
    ):
        click.echo(
            highlight.model_dump_json(
                include={"id", "book_id", "text", "note", "tags", "highlighted_at"},
                indent=4,
            )
        )

        if limit:
            limit -= 1
            if limit == 0:
                break


@highlights.command(name="details")
@click.argument("highlight_id")
@click.option(
    "--token",
    "-t",
    help="Readwise API token.",
)
def details_highlight(highlight_id, token):
    """Get highlight details."""
    client = Readwise(check_token(token))

    highlight = client.get("/highlights/{}".format(highlight_id))

    print(
        json.dumps(
            {
                "title": highlight.title,
                "book_id": highlight.id,
                "highlight": highlight.text,
                "note": highlight.note,
                "tags": ", ".join(tag.name for tag in highlight.tags),
            },
            indent=2,
        )
    )


@highlights.command(name="tags")
@click.argument("highlight_id")
@click.option("--api-token", "-t", help="Readwise API token.")
def highlights_tags_list(highlight_id, token):
    """Get tags."""
    client = Readwise(check_token(token))

    tags = client.get("highlights/{}".format(highlight_id))

    print(tags)


@cli.command(name="daily-review")
@click.option(
    "--api-token",
    "-t",
    help="Readwise API token.",
)
def daily_review(token):
    """Get daily review highlights."""
    client = Readwise(check_token(token))

    for highlight in client.get_daily_review_highlights():
        print(
            json.dumps(
                {
                    "title": highlight.title,
                    "book_id": highlight.id,
                    "highlight": highlight.text,
                    "note": highlight.note,
                },
                indent=2,
            )
        )


@cli.group(name="books")
def books():
    """Commands to list and create books in Readwise."""


@books.command(name="list")
@click.argument(
    "category",
    type=click.Choice(
        ["articles", "books", "tweets", "podcasts", "supplementals"],
        case_sensitive=False,
    ),
    default="articles",
)
@click.option("--limit", "-l", type=int, help="Limit the number of books to return.")
@click.option(
    "--token",
    "-t",
    help="Readwise API token.",
)
def books_list(category, limit, token):
    """Get books."""
    client = Readwise(check_token(token))

    for book in client.get_books(category):
        print(
            json.dumps(
                {
                    "id": book.id,
                    "title": book.title,
                    "author": book.author,
                    "category": book.category,
                    "source": book.source,
                    "num_highlights": book.num_highlights,
                    "cover_image_url": book.cover_image_url,
                    "highlights_url": book.highlights_url,
                    "source_url": book.source_url,
                    "document_note": book.document_note,
                },
                indent=2,
            )
        )
        if limit:
            limit -= 1
            if limit == 0:
                break


@books.command(name="tags")
@click.argument("book_id")
@click.option("--token", "-t", help="Readwise API token.")
def book_tags(book_id, token):
    """Get book tags."""
    client = Readwise(check_token(token))

    for tag in client.get_book_tags(book_id):
        print(json.dumps({"id": tag.id, "tag": tag.name}, indent=2))


@cli.group(name="tags")
def tags():
    """Get tags."""


@tags.command(name="list")
@click.option(
    "--token",
    "-t",
    help="Readwise API token.",
)
def tags_list(token):
    """Get tags."""
    client = Readwise(check_token(token))

    tags = Counter()

    for results in client.export_highlights():
        for highlight in results.highlights:
            tags.update(tag.name for tag in highlight.tags)

    for tag, count in tags.items():
        print(f"{tag}: {count}")


@cli.group(name="reader")
def reader():
    """Commands to interact with the Readwise Reader API Endpoints."""


@reader.command(name="list")
@click.option(
    "--token",
    "-t",
    help="Readwise API token.",
)
def reader_list(token):
    """List documents in Readwise Reader."""
    client = ReadwiseReader(check_token(token))

    for document in client.get_documents():
        print(
            json.dumps(
                {
                    "id": document.id,
                    "title": document.title,
                    "author": document.author,
                    "category": document.category,
                    "source": document.source,
                    "num_highlights": document.num_highlights,
                    "cover_image_url": document.cover_image_url,
                    "highlights_url": document.highlights_url,
                    "source_url": document.source_url,
                    "document_note": document.document_note,
                },
                indent=2,
            )
        )


def check_token(token):
    if not token:
        try:
            token = os.environ.get("READWISE_TOKEN")
        except KeyError:
            click.echo("API token not provided.")
            return
    return token
