# Reddit Subscription Manager

A Python tool to export/import Reddit subreddit subscriptions using the Reddit API.

## Setup

1. **Install Requirements**
   ```bash
   pip install praw python-dotenv
   ```

2. **Create Reddit App**
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create App"
   - Choose "script" type
   - Set name to whatever you want (note it can't contain the word `reddit`), set redirect uri to something like https://localhost:6969, it doesn't really matter
   - Note: client ID (that's the long string below "personal use script" and the application name), client secret
   - Add your other account as a developer so the script has access to both accounts

3. **Configure Credentials**
   ```bash
   cp config.json.example config.json
   ```
   Edit `config.json` with your credentials:
   ```json
   {
       "client_id": "YOUR_CLIENT_ID",
       "client_secret": "YOUR_CLIENT_SECRET",
       "user_agent": "script:subscription_manager:v1.0"
   }
   ```

## Usage

**Export Subscriptions**
```bash
python export_subs.py
```
- Will ask for username and password, it will not be stored on disk
- Will create `subreddits.json` with your current subscriptions

**Import Subscriptions**
```bash
python import_subs.py
```
- Will ask for username and password, it will not be stored on disk
- Requires existing `subreddits.json` file

## Troubleshooting

- May not work with 2FA accounts, have not tested.