# Nikshay Jain | MM21B044
# Airflow-backed Google News Scraper

## Overview

This project is an automated Google News scraper that extracts articles from various sections of the Google News website. 

It utilizes Docker and Apache Airflow to create a robust, self-executing pipeline that runs hourly without manual intervention.

We have also set up a cronjob which automated the trigger on an hourly basis too. This won't need manual intervention at all.

## Key Features

- Scrapes Google News Home Page, Top Stories, or custom topics
- Automated hourly execution via cron job
- Docker-based setup for easy deployment
- Airflow-orchestrated workflow
- PostgreSQL database for data storage
- Email notifications for database updates

## System Requirements

- Python 3.9+
- Linux/MacOS/Windows (with WSL2 support)
- Docker and Docker Compose

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/DA5402-MLOps-JanMay2025/assignment-02-Nikshay-Jain.git
   cd assignment-02-Nikshay-Jain
   ```

2. Configure the scraper:
   Edit `config.ini` and set `search_query` to one of:
   - `'home'`: Scrapes the entire homepage
   - `'top_stories'`: Scrapes only top stories
   - Any specific topic (e.g., 'technology', 'sports')

## Execution Methods

Specify the page you would like to scrape from Google News website by updating the `search_query` field in the `config.ini` file with one of the following options:  

1. `'home'` – Scrapes the entire homepage.  
2. `'top_stories'` – Scrapes only the top stories section.  
3. Any specific topic – Scrapes news articles related to the specified topic.  

Once the `config.ini` file is updated and saved, you can either run the workflow $\textbf{manually or use airflow}$. 

### 1. Manual Execution

a. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

b. Run the scripts sequentially:
   ```bash
   python3 main12.py
   python3 main3.py
   python3 main4.py
   ```
The extracted results will be stored in a directory named after the specified `search_query` as html files which will then be parsed for extracting headlines, thumbnails and encode them using `base64 encoders`.

All of the extracted data is initially stored in a `*.csv` file which is then imported into a PostgreSQL database.

### 2. Automated Airflow Workflow

a. Build the Docker image and initialize Airflow:
   ```bash
   docker build -t ext_airflow:1.2 .
   docker compose up airflow-init
   docker compose up -d
   ```

b. Access Airflow UI:
   Open `http://localhost:8080/` in a web browser
   Login with default credentials (username: airflow, password: airflow)

c. Activate DAGs:
   Enable `dag_hourly_scraper` and `dag_email_on_new_data` in the Airflow UI

You would need to setup a Postgres and SMTP connection on Airflow by the UI to get things functional. Post that, on every change in the Postgres database, the email specified in the `dag_6.py` file gets a mail regarding the same. No further intervention is needed.

## Data Flow

1. Web scraping extracts headlines and thumbnails
2. Data is encoded using base64
3. Results are stored in CSV files
4. CSV data is imported into PostgreSQL database
5. Email notifications are sent on database updates

## Troubleshooting

If you encounter issues, check Docker logs and Airflow task logs for detailed error messages.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements.
