# Python Module to use the Readwise API

This module is a wrapper for the Readwise API.

It allows you to easily access your Readwise data in Python.

## Installation

```bash
pip install -U readwise
```

## How to use

### Readwise API

```python
from readwise import Readwise

client = Readwise('token')

books = client.get_books(category='articles')

for book in books:
	highlights = client.get_book_highlights(book.id)
	if len(highlights) > 0:
		print(book.title)
		for highlight in highlights:
			print(highlight.text)
```

#### Export All Highlights

```python
from readwise import Readwise

client = Readwise(token='<your_api_token>')

# Get all of a user's books/highlights from all time
all_data = client.export_highlights()

# Later, if you want to get new highlights updated since your last fetch of allData, do this.
last_fetch_was_at = datetime.datetime.now() - datetime.timedelta(days=1)  # use your own stored date
new_data = client.export_highlights(last_fetch_was_at.isoformat())
```

#### Daily Review Highlights

Get the daily review details and highlights

```python
daily_review = client.get_daily_review()

completed = daily_review.review_completed # True or False
print(completed) # True or False

highlights = daily_review.highlights
```

or a generator of only the highlights.

```python
for highlight in client.get_daily_review_highlights():
	print(highlight.text)
```

### Readwise Readwise API

```python
from readwise import ReadwiseReader

client = ReadwiseReader('token')

response = client.create_document('https://www.example.com')
response.raise_for_status()
```

## Documentation

The latest documentation can be found at <https://rwxd.github.io/pyreadwise/>

If you've checked out the source code (for example to review a PR), you can build the latest documentation by running `make serve-docs`.
