# Google News Image Captioning Pipeline

**A scalable pipeline to generate <image, caption> tuples from Google News**  
*Designed for CronJob integration with configurable components*

---

## Modules Overview

| Module | Purpose | Key Features |
|--------|---------|--------------|
| **1**  | Scrape Google News homepage | Configurable URL handling |
| **2**  | Extract "Top Stories" link | Dynamic XPath/CSS selector config |
| **3**  | Scrape thumbnails & headlines | Lazy loading handling, Bulk image download |
| **4**  | Store in database | PostgreSQL/MariaDB/MongoDB support, Schema management |
| **5**  | Deduplication | Perceptual hashing + headline similarity |
| **6**  | Orchestration | Cron-friendly logging, Error recovery |

---

## Requirements

1. **Python 3.7+**
2. **Database**: PostgreSQL/MariaDB/MongoDB
3. **System Dependencies**:  
   ```bash
   sudo apt-get install chromium-driver  # For headless browsing
   ```
4. **Python Packages**:
   ```bash
   pip install -r requirements.txt
   ```
   *Sample requirements.txt*:
   ```
   selenium>=4.0
   psycopg2-binary
   imagehash
   Pillow
   python-dotenv
   ```

---

## Configuration

1. **Database Setup** (`database.ini`):
   ```ini
   [postgresql]
   host=localhost
   database=news_data
   user=postgres
   password=your_password
   port=5432
   ```

2. **Pipeline Config** (`config.ini`):
   ```ini
   [scraping]
   user_agent = Mozilla/5.0 (...)
   scroll_count = 8
   similarity_threshold = 0.85
   ```

---

## Execution

**Manual Run**:
```bash
python module6_orchestrate.py
```

**CronJob Setup**:
```bash
0 */2 * * * /path/to/python /path/to/module6_orchestrate.py >> /var/log/news_pipeline.log
```

---

## Output Structure

1. **Database Tables**:
   ```sql
   TABLE images (image_id, image_url, image_data, phash, ...)
   TABLE articles (article_id, headline, url, image_id, ...)
   ```

2. **Artifacts**:
   - `./output/YYYY-MM-DD/images/` (JPEG thumbnails)
   - `./output/YYYY-MM-DD/metadata.json`  
   *Sample JSON*:
   ```json
   {
     "headline": "Climate Summit Breakthrough",
     "image_url": "2025-02-02/images/1.jpg",
     "source": "Reuters",
     "timestamp": "2025-02-02T18:30:45Z"
   }
   ```

---

## Troubleshooting

1. **Common Issues**:
   - Update CSS selectors in `config.ini` if layout changes
   - Check disk space for image storage
   - Monitor database connection limits

2. **Logs**:
   - `pipeline_YYYYMMDDHHMM.log` (Detailed execution traces)
   - `deduplication_errors.log` (Hash collisions & similarity mismatches)

---