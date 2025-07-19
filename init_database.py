from database_config import DatabaseManager
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_database():
    db_manager = DatabaseManager()
    
    if db_manager.connect():
        if db_manager.create_tables():
            print("Database initialized successfully!")
            print("Tables created:")
            print("- intrusion_logs: Lưu thông tin các lần phát hiện xâm nhập")
        else:
            print("Failed to create tables")
        
        db_manager.disconnect()
    else:
        print("Failed to connect to database")

if __name__ == "__main__":
    initialize_database()
