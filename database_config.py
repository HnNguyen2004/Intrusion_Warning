import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.connection_params = {
            'host': 'localhost',
            'database': 'warning_data',
            'user': 'phidinh',
            'password': 'phi01478965',
            'port': 5432
        }
        self.connection = None
        
    def connect(self):
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            logging.info("Database connection established")
            return True
        except Exception as e:
            logging.error(f"Database connection failed: {e}")
            return False
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed")
    
    def create_tables(self):
        try:
            cursor = self.connection.cursor()
            
            # Tạo bảng intrusion_logs
            create_table_query = """
            CREATE TABLE IF NOT EXISTS intrusion_logs (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                person_name VARCHAR(100),
                confidence FLOAT,
                image_path VARCHAR(255),
                location VARCHAR(100),
                telegram_sent BOOLEAN DEFAULT FALSE,
                notes TEXT
            );
            """
            
            cursor.execute(create_table_query)
            self.connection.commit()
            cursor.close()
            logging.info("Tables created successfully")
            return True
            
        except Exception as e:
            logging.error(f"Error creating tables: {e}")
            return False
    
    def insert_intrusion_log(self, person_name, confidence, image_path, location="Unknown", telegram_sent=False, notes=""):
        try:
            cursor = self.connection.cursor()
            
            insert_query = """
            INSERT INTO intrusion_logs (person_name, confidence, image_path, location, telegram_sent, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
            """
            
            cursor.execute(insert_query, (person_name, confidence, image_path, location, telegram_sent, notes))
            log_id = cursor.fetchone()[0]
            self.connection.commit()
            cursor.close()
            
            logging.info(f"Intrusion log saved with ID: {log_id}")
            return log_id
            
        except Exception as e:
            logging.error(f"Error inserting intrusion log: {e}")
            return None
    
    def get_recent_logs(self, limit=10):
        try:
            cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            
            query = """
            SELECT * FROM intrusion_logs 
            ORDER BY timestamp DESC 
            LIMIT %s;
            """
            
            cursor.execute(query, (limit,))
            logs = cursor.fetchall()
            cursor.close()
            
            return logs
            
        except Exception as e:
            logging.error(f"Error fetching logs: {e}")
            return []
    
    def update_telegram_status(self, log_id, sent=True):
        try:
            cursor = self.connection.cursor()
            
            update_query = """
            UPDATE intrusion_logs 
            SET telegram_sent = %s 
            WHERE id = %s;
            """
            
            cursor.execute(update_query, (sent, log_id))
            self.connection.commit()
            cursor.close()
            
            logging.info(f"Telegram status updated for log ID: {log_id}")
            return True
            
        except Exception as e:
            logging.error(f"Error updating telegram status: {e}")
            return False
