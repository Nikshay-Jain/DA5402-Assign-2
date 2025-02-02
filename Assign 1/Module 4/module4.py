import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor
from datetime import datetime
import hashlib
import requests
from typing import List, Dict
from configparser import ConfigParser
import json

class NewsDatabase:
    def __init__(self, config_file='database.ini'):
        self.config = self._load_db_config(config_file)
        self.conn = None
        
    def _load_db_config(self, filename: str) -> Dict:
        """Load database configuration from .ini file"""
        parser = ConfigParser()
        parser.read(filename)
        return {
            'host': parser.get('postgresql', 'host'),
            'database': parser.get('postgresql', 'database'),
            'user': parser.get('postgresql', 'user'),
            'password': parser.get('postgresql', 'password'),
            'port': parser.get('postgresql', 'port', fallback='5432')
        }

    def connect(self):
        """Establish database connection"""
        self.conn = psycopg2.connect(
            host=self.config['host'],
            database=self.config['database'],
            user=self.config['user'],
            password=self.config['password'],
            port=self.config['port'],
            cursor_factory=DictCursor
        )

    def initialize_schema(self):
        """Create database tables if they don't exist"""
        with self.conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS images (
                    image_id SERIAL PRIMARY KEY,
                    image_url TEXT UNIQUE,
                    image_data BYTEA,
                    image_hash TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    article_id SERIAL PRIMARY KEY,
                    headline TEXT NOT NULL,
                    url TEXT UNIQUE NOT NULL,
                    source TEXT,
                    scrape_timestamp TIMESTAMP NOT NULL,
                    article_date TIMESTAMP,
                    image_id INTEGER REFERENCES images(image_id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            self.conn.commit()

    def store_image(self, image_url: str) -> int:
        """Store image data and return image_id"""
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            image_data = response.content
            image_hash = hashlib.sha256(image_data).hexdigest()
            
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO images (image_url, image_data, image_hash)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (image_hash) DO NOTHING
                    RETURNING image_id;
                """, (image_url, image_data, image_hash))
                
                result = cursor.fetchone()
                if result:
                    return result['image_id']
                
                # If image exists, return existing ID
                cursor.execute("SELECT image_id FROM images WHERE image_hash = %s", (image_hash,))
                return cursor.fetchone()['image_id']
                
        except Exception as e:
            print(f"Error storing image: {str(e)}")
            return None

    def store_article(self, article_data: Dict):
        """Store article metadata with image reference"""
        required_fields = ['headline', 'url', 'image_url']
        if not all(field in article_data for field in required_fields):
            raise ValueError("Missing required article fields")

        try:
            image_id = self.store_image(article_data['image_url'])
            if not image_id:
                return False

            with self.conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO articles (
                        headline, 
                        url, 
                        source, 
                        scrape_timestamp, 
                        article_date, 
                        image_id
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (url) DO NOTHING;
                """, (
                    article_data.get('title'),
                    article_data.get('url'),
                    article_data.get('source'),
                    datetime.now(),
                    article_data.get('timestamp'),
                    image_id
                ))
                return cursor.rowcount > 0
                
        except Exception as e:
            print(f"Error storing article: {str(e)}")
            return False

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    # Example usage
    db = NewsDatabase()
    db.connect()
    db.initialize_schema()
    
    # Load data from Module 3 output
    with open('images_titles.json', 'r') as f:
        articles = json.load(f)
    
    for article in articles:
        success = db.store_article(article)
        if success:
            print(f"Stored article: {article['title']}")
        else:
            print(f"Failed to store article: {article['title']}")
    
    db.close()