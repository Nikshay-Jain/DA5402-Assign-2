# Database Storage Module (Module 4) - README

This module handles persistent storage of scraped news articles and images in a PostgreSQL database, implementing deduplication and relational data management.

## Features

- **Relational Storage**: Maintains separate tables for images and articles
- **Deduplication**: 
  - SHA-256 image hashing for duplicate detection
  - URL-based article uniqueness constraint
- **Schema Management**: Automatic table creation
- **Data Integrity**: Foreign key constraints between articles and images

## Requirements

1. PostgreSQL server (v12+ recommended)
2. Python 3.7+
3. Required packages:
   ```bash
   pip install psycopg2-binary requests
   ```

## Database Setup

1. Create a new PostgreSQL database:
   ```sql
   CREATE DATABASE news_db;
   ```

2. Create `database.ini` in your project root:
   ```ini
   [postgresql]
   host = localhost
   database = news_db
   user = postgres
   password = your_password
   port = 5432
   ```

## Schema Design

### Images Table
| Column | Type | Description |
|--------|------|-------------|
| image_id | SERIAL | Primary key |
| image_url | TEXT | Original image
