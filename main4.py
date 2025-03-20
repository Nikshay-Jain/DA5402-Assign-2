# Create a table in PostgreSQL database and insert data from a CSV file

import os
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook

def main4():
    csv_file_path = [f for f in os.listdir('/opt/airflow/assign2') if f.endswith('.csv')]
    if csv_file_path:
        csv_file_path = os.path.join('/opt/airflow/assign2', csv_file_path[0])
    
    print(f"CSV file path: {csv_file_path}")

    # Read CSV file
    df = pd.read_csv(csv_file_path)
    print(f"Columns in CSV: {df.columns.tolist()}")
    
    # Connect to PostgreSQL
    postgres_hook = PostgresHook(postgres_conn_id="postgres_default")
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()
    
    # Create headlines table
    create_headlines_table_query = """
    CREATE TABLE IF NOT EXISTS headlines (
        id SERIAL PRIMARY KEY,
        headline VARCHAR(255)
    )
    """
    cursor.execute(create_headlines_table_query)
    
    # Create images table
    create_images_table_query = """
    CREATE TABLE IF NOT EXISTS images (
        id SERIAL PRIMARY KEY,
        headline_id INTEGER REFERENCES headlines(id),
        image_path VARCHAR(255),
        encoding TEXT
    )
    """
    cursor.execute(create_images_table_query)
    
    # Insert data
    successful_inserts = 0
    for _, row in df.iterrows():
        # Insert headline data
        insert_headline_query = """
        INSERT INTO headlines (headline)
        VALUES (%s)
        RETURNING id
        """
        cursor.execute(insert_headline_query, (row['Headline'],))
        headline_id = cursor.fetchone()[0]
        
        # Insert image data
        insert_image_query = """
        INSERT INTO images (headline_id, image_path, encoding)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_image_query, (headline_id, row['Image Path'], row['Encoding']))
        
        successful_inserts += 1
    
    conn.commit()
    cursor.close()
    conn.close()
    
    status_dir = '/opt/airflow/dags/run/'
    os.makedirs(status_dir, exist_ok=True)  # Create directory if it doesn't exist
    with open(os.path.join(status_dir, 'status'), 'w') as f:
        f.write(str(successful_inserts))
    
    print(f"Data insertion completed successfully. {successful_inserts} records inserted.")

if __name__ == "__main__":
    main4()