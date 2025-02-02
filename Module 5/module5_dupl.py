import requests
import imagehash
from PIL import Image
from difflib import SequenceMatcher
import psycopg2
from psycopg2 import sql
from io import BytesIO
from configparser import ConfigParser

class NewsDeduplicator:
    def __init__(self):
        self.conn = None
        self.config = self._load_config()
        
    def _load_config(self):
        """Load database configuration"""
        config = ConfigParser()
        config.read('database.ini')
        return {
            'host': config.get('postgresql', 'host'),
            'database': config.get('postgresql', 'database'),
            'user': config.get('postgresql', 'user'),
            'password': config.get('postgresql', 'password'),
            'port': config.get('postgresql', 'port', '5432')
        }

    def connect(self):
        """Establish database connection"""
        self.conn = psycopg2.connect(
            host=self.config['host'],
            database=self.config['database'],
            user=self.config['user'],
            password=self.config['password'],
            port=self.config['port']
        )

    def _get_image_phash(self, image_url: str) -> str:
        """Calculate perceptual hash for image deduplication"""
        try:
            response = requests.get(image_url, timeout=10)
            img = Image.open(BytesIO(response.content))
            return str(imagehash.phash(img))
        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return None

    def _headline_similarity(self, headline1: str, headline2: str) -> float:
        """Calculate headline similarity ratio using difflib"""
        return SequenceMatcher(None, headline1.lower(), headline2.lower()).ratio()

    def is_duplicate(self, headline: str, image_url: str, threshold: float = 0.9) -> bool:
        """
        Check for duplicate using:
        1. Perceptual image hashing (for similar images)
        2. Headline similarity ratio
        3. Existing URL check
        """
        if not self.conn:
            self.connect()

        with self.conn.cursor() as cursor:
            # Check URL existence
            cursor.execute("SELECT 1 FROM articles WHERE url = %s", (image_url,))
            if cursor.fetchone():
                return True

            # Calculate perceptual hash
            phash = self._get_image_phash(image_url)
            if not phash:
                return False

            # Find similar images (allows some pixel variation)
            cursor.execute("""
                SELECT a.headline 
                FROM articles a
                JOIN images i ON a.image_id = i.image_id
                WHERE i.phash LIKE %s
                LIMIT 50
            """, (phash[:5] + '%',))  # Match first 5 characters of phash

            # Check headline similarity
            for (existing_headline,) in cursor.fetchall():
                if self._headline_similarity(headline, existing_headline) > threshold:
                    return True

        return False

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

# Example usage
if __name__ == "__main__":
    dedupe = NewsDeduplicator()
    dedupe.connect()
    
    test_cases = [
        ("Breaking News: Climate Summit", "https://example.com/image1.jpg"),
        ("New Tech Innovation Revealed", "https://example.com/image2.jpg")
    ]

    for headline, image_url in test_cases:
        if dedupe.is_duplicate(headline, image_url):
            print(f"Duplicate found: {headline}")
        else:
            print(f"New entry: {headline}")

    dedupe.close()
