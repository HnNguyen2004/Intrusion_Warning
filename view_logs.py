from database_config import DatabaseManager
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def view_intrusion_logs():
    db_manager = DatabaseManager()
    
    if db_manager.connect():
        logs = db_manager.get_recent_logs(20)
        
        print("\n" + "="*80)
        print("INTRUSION DETECTION LOGS")
        print("="*80)
        
        if logs:
            for log in logs:
                print(f"\nID: {log['id']}")
                print(f"Time: {log['timestamp']}")
                print(f"Person: {log['person_name']}")
                print(f"Confidence: {log['confidence']:.2f}")
                print(f"Location: {log['location']}")
                print(f"Image: {log['image_path']}")
                print(f"Telegram Sent: {'Yes' if log['telegram_sent'] else 'No'}")
                if log['notes']:
                    print(f"Notes: {log['notes']}")
                print("-" * 50)
        else:
            print("No intrusion logs found.")
        
        db_manager.disconnect()
    else:
        print("Failed to connect to database")

if __name__ == "__main__":
    view_intrusion_logs()
