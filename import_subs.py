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
    
    required_keys = ['client_id', 'client_secret', 'user_agent']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required key in config: {key}")
    
    return config

def import_subscriptions():
    try:
        config = load_config()
        username = input("Enter Reddit username to import to: ")
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

        logging.info("Loading subreddits from file...")
        with open('subreddits.json', 'r') as f:
            subs = json.load(f)
        
        logging.info(f"Found {len(subs)} subreddits. Starting import...")
        success_count = 0
        failure_count = 0
        failures = []

        print("")

        for idx, sub_name in enumerate(subs, 1):
            try:
                reddit.subreddit(sub_name).subscribe()
                logging.info(f"[{idx}/{len(subs)}] Subscribed to r/{sub_name}")
                success_count += 1
            except Exception as e:
                error_msg = str(e)
                logging.error(f"[{idx}/{len(subs)}] Failed to subscribe to r/{sub_name}: {error_msg}")
                failure_count += 1
                failures.append({
                    'subreddit': sub_name,
                    'error': error_msg
                })
        print("")
        logging.info(f"Import summary:")
        logging.info(f"Success: {success_count}")
        logging.info(f"Failures: {failure_count}")
        
        if failures:
            print()
            logging.info("Failed subreddits:")
            for failure in failures:
                logging.info(f"r/{failure['subreddit']} - {failure['error']}")
            logging.info(f"Total failed: {len(failures)}")

        return True
        
    except Exception as e:
        logging.error(f"Import failed: {str(e)}")
        return False

if __name__ == '__main__':
    start_time = datetime.now()
    logging.info("=== Starting import process ===")
    
    if import_subscriptions():
        print()
        logging.info(f"Import completed in {datetime.now() - start_time}")
    else:
        print()
        logging.error("Import failed due to errors")