# Google News Image Captioning Pipeline (Assign 1 | DA5402) - README  
**A Complete Guide to Building an Automated <Image, Caption> Dataset**  
*Last Updated: February 2, 2025 | Designed for CronJob Deployment*  

---

## Overview  
This pipeline automates the creation of an image captioning dataset using Google News as the source. The system comprises 6 modules that work in cascade to scrape, process, deduplicate, and store news images with their headlines. 

Each module is in its seperate directory and has respective readme.md files as a guide to use them.

It is to be taken utmost care of that the user starts execution in the required directory for the modules to run successfully.

---

## Requirements  

### **System Requirements**  
1. **Python 3.9+**  
2. **Database**: PostgreSQL 14+  
3. **Linux/MacOS** (Windows WSL2 supported)  
4. **ChromeDriver** (for headless browsing)  

### **Python Packages**  
```bash
pip install -r requirements.txt  
```
*Sample requirements.txt*:  
```
selenium==4.15.0  
psycopg2-binary==2.9.9  
imagehash==4.3.1  
python-dotenv==1.0.0  
undetected-chromedriver==3.5.3  
```

---

## Installation  

1. **Clone Repository**  
```bash  
git https://github.com/Nikshay-Jain/DA5402.git  
cd "Assign 1"  
```

2. **Database Setup**  
```sql  
-- For PostgreSQL  
CREATE DATABASE news_db;  
CREATE USER pipeline_user WITH PASSWORD 'secure_pass';  
GRANT ALL PRIVILEGES ON DATABASE news_db TO pipeline_user;  
```

3. **Configuration Files**  
   - `database.ini` (Database credentials):  
   ```ini  
   [postgresql]  
   host=localhost  
   database=news_db  
   user=pipeline_user  
   password=secure_pass  
   port=5432  
   ```

   - `pipeline.ini` (Pipeline settings):  
   ```ini  
   [scraping]  
   user_agent = Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36  
   scroll_count = 8  
   similarity_threshold = 0.85  

   [logging]  
   level = INFO  
   max_log_files = 7  
   ```

---

## Execution  

### **Manual Run**  
```bash  
python module6_orchestrate.py  
```

### **Automated CronJob**  
1. Edit crontab:  
```bash  
crontab -e  
```

2. Add entry (runs every 2 hours):  
```bash  
0 */2 * * * /usr/bin/python3 /path/to/module6_orchestrate.py >> /var/log/news_pipeline.log 2>&1  
```

3. Enable log rotation:  
```bash  
sudo nano /etc/logrotate.d/news_pipeline  
```
Add:  
```  
/var/log/news_pipeline.log {  
    daily  
    rotate 7  
    compress  
    missingok  
    notifempty  
}  
```

---

## Database Schema  

### **Images Table**  
| Column | Type | Description |  
|---------|------|-------------|  
| image_id | SERIAL | Primary key |  
| image_url | TEXT | Original URL |  
| image_data | BYTEA | Binary image |  
| phash | VARCHAR(64) | Perceptual hash |  

### **Articles Table**  
| Column | Type | Description |  
|---------|------|-------------|  
| article_id | SERIAL | Primary key |  
| headline | TEXT | News headline |  
| url | TEXT | Article URL |  
| image_id | INT | Foreign key to images |  

---

## 🔍 Troubleshooting  

### **Common Issues**  
1. **Selector Changes**:  
   - Update CSS/XPath in `pipeline.ini`  
   - Check `debug.html` from Module 1  

2. **Database Connection Issues**:  
   ```bash  
   sudo -u postgres psql -c "ALTER USER pipeline_user CONNECTION LIMIT 100;"  
   ```

3. **Lazy Loading Failures**:  
   Increase `scroll_count` in config  

### **Log Analysis**  
1. **Execution Logs**:  
   ```bash  
   tail -f /var/log/news_pipeline.log  
   ```

2. **Deduplication Logs**:  
   ```bash  
   grep "DUPLICATE" /var/log/news_pipeline.log  
   ```

---

## Output Structure  

1. **Database Storage**  
   - Images stored as binary blobs  
   - Article metadata with timestamps  

2. **File System**  
   ```  
   ./output/  
   ├── 2025-02-02/  
   │   ├── images/  
   │   │   ├── 1.jpg  
   │   │   └── 2.jpg  
   │   └── metadata.json  
   └── pipeline_report.json  
   ```

## Final Conclusion

The sample outputs are attached in respective directories which were achieved after executing the files successfully in local Windows environment. 

User discretion is reqested in case of any deployment issue.

---