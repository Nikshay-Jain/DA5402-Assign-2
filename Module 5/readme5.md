# News Deduplicator

This Python script implements a sophisticated deduplication system for news articles, using a combination of image perceptual hashing and headline similarity checking.

## Features

- Perceptual image hashing for detecting similar images
- Headline similarity comparison using sequence matching
- URL-based duplication check
- Configurable similarity threshold
- PostgreSQL database integration

## Requirements

- Python 3.7+
- PostgreSQL database
- Required Python packages:
  - requests
  - Pillow
  - imagehash
  - psycopg2-binary

## Installation

1. Clone the repository or download the script.
2. Install the required packages:
   ```
   pip install requests Pillow imagehash psycopg2-binary
   ```
3. Set up a PostgreSQL database and create the necessary tables.
4. Create a `database.ini` file with your database configuration.

## Configuration

Create a `database.ini` file in the same directory as the script:

```ini
[postgresql]
host = localhost
database = your_database_name
user = your_username
password = your_password
port = 5432
```

## Usage

```python
from news_deduplicator import NewsDeduplicator

dedupe = NewsDeduplicator()
dedupe.connect()

# Check if an article is a duplicate
is_duplicate = dedupe.is_duplicate("Headline", "https://example.com/image.jpg")

dedupe.close()
```

## How It Works

1. Checks if the URL already exists in the database.
2. Calculates a perceptual hash of the image.
3. Searches for similar images in the database.
4. Compares headlines of articles with similar images.
5. Returns True if a duplicate is found, False otherwise.

## Customization

- Adjust the `threshold` parameter in `is_duplicate()` to change the similarity threshold.
- Modify the SQL queries to fit your specific database schema.

## Note

Ensure your database schema includes a `phash` column in the `images` table and appropriate indexes for optimal performance.