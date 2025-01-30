import praw
import json
import logging
import getpass
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def load_config():
    config_path = Path('config.json')
    if not config_path.exists():
        logging.error("Config file not found. Create config.json from config.json.example")
        raise FileNotFoundError("config.json missing")

    with open(config_path) as f:
        config = json.load(f)
    
    required_keys = ['client_id', 'client_secret', 'user_agent']  # Removed username
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required key in config: {key}")
    
    return config

def export_subscriptions():
    try:
        config = load_config()
        username = input("Enter Reddit username to export from: ")
        password = getpass.getpass("Enter password (input hidden for security): ")
        print()
        
        logging.info(f"Initializing connection for {username}...")
        reddit = praw.Reddit(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            user_agent=config['user_agent'],
            username=username,
            password=password
        )

        logging.info("Fetching subscribed subreddits...")
        subs = [sub.display_name for sub in reddit.user.subreddits(limit=None)]
        
        logging.info(f"Found {len(subs)} subscriptions. Saving to file...")
        with open('subreddits.json', 'w') as f:
            json.dump(subs, f, indent=4)
        
        logging.info(f"Successfully exported {len(subs)} subreddits")
        return True
        
    except Exception as e:
        logging.error(f"Export failed: {str(e)}")
        return False

if __name__ == '__main__':
    start_time = datetime.now()
    logging.info("=== Starting export process ===")
    
    if export_subscriptions():
        logging.info(f"Export completed in {datetime.now() - start_time}")
    else:
        logging.error("Export failed due to errors")