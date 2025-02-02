import logging
from datetime import datetime
import json
import sys
from configparser import ConfigParser
from module1 import GoogleNewsScraper
from module2 import TopStoriesExtractor
from module3 import ArticleScraper
from module4 import NewsDatabase
from module5 import NewsDeduplicator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'pipeline_{datetime.now().strftime("%Y%m%d%H%M")}.log'),
        logging.StreamHandler()
    ]
)

class NewsPipeline:
    def __init__(self):
        self.config = self.load_config()
        self.state = {
            'current_module': None,
            'success': False,
            'error': None
        }
        
    def load_config(self):
        """Load central configuration"""
        config = ConfigParser()
        config.read('pipeline.ini')
        return config

    def run_module(self, module_func, module_name):
        """Generic module runner with error handling"""
        self.state['current_module'] = module_name
        logging.info(f"Starting {module_name}")
        
        try:
            result = module_func()
            logging.info(f"Completed {module_name} successfully")
            return result
        except Exception as e:
            self.state['error'] = str(e)
            logging.error(f"Failed {module_name}: {str(e)}", exc_info=True)
            raise
        finally:
            self.state['current_module'] = None

    def execute_pipeline(self):
        """Main pipeline execution flow"""
        pipeline_start = datetime.now()
        logging.info("Pipeline execution started")
        
        try:
            # Module 1: Scrape homepage
            base_data = self.run_module(
                lambda: GoogleNewsScraper().scrape(),
                "Module 1 - Homepage Scraper"
            )
            
            # Module 2: Get Top Stories URL
            top_stories_url = self.run_module(
                lambda: TopStoriesExtractor().extract(base_data),
                "Module 2 - Top Stories Extractor"
            )
            
            # Module 3: Scrape articles
            articles = self.run_module(
                lambda: ArticleScraper().scrape(top_stories_url),
                "Module 3 - Article Scraper"
            )
            
            # Module 4: Store in database
            db = NewsDatabase()
            stored_count = self.run_module(
                lambda: self.store_articles(db, articles),
                "Module 4 - Database Storage"
            )
            
            # Module 5: Deduplication check
            dup_count = self.run_module(
                lambda: self.check_duplicates(db, articles),
                "Module 5 - Deduplication Check"
            )
            
            # Final report
            self.state.update({
                'success': True,
                'stats': {
                    'total_articles': len(articles),
                    'stored': stored_count,
                    'duplicates': dup_count,
                    'duration': str(datetime.now() - pipeline_start)
                }
            })
            
        except Exception as e:
            logging.error("Pipeline aborted due to critical error")
            return False
        finally:
            db.close()
            self.generate_report()
            
        return True

    def store_articles(self, db, articles):
        """Wrapper for Module 4"""
        success_count = 0
        for article in articles:
            if db.store_article(article):
                success_count += 1
        return success_count

    def check_duplicates(self, db, articles):
        """Wrapper for Module 5"""
        dedupe = NewsDeduplicator()
        dedupe.connect()
        duplicate_count = 0
        
        for article in articles:
            if dedupe.is_duplicate(article['title'], article['image_url']):
                duplicate_count += 1
                
        dedupe.close()
        return duplicate_count

    def generate_report(self):
        """Generate final execution report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'status': 'success' if self.state['success'] else 'failed',
            'last_module': self.state['current_module'],
            'error': self.state['error'],
            'stats': self.state.get('stats', {})
        }
        
        with open('pipeline_report.json', 'w') as f:
            json.dump(report, f, indent=2)

if __name__ == "__main__":
    pipeline = NewsPipeline()
    success = pipeline.execute_pipeline()
    sys.exit(0 if success else 1)