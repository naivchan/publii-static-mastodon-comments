import sqlite3
import json
import os
import requests
import shutil
import time

# ================= CONFIGURATION =================
DB_PATH = r'C:\Users\Naive\Documents\Publii\sites\navis-ranobe-blog\input\db.sqlite'
OUTPUT_DIR = r'C:\Users\Naive\Documents\Publii\sites\navis-ranobe-blog\input\media\files\comments'
INSTANCE = 'sakurajima.moe'

# Your Access Token (Cleaned to avoid "Bearer Bearer" issue)
ACCESS_TOKEN = 'B3UjqntrooFW-QTGlrQ957YcDbrNyrtcIQMjM77oU4U'
# =================================================

def fetch_comments_with_stats(status_id):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    
    status_url = f"https://{INSTANCE}/api/v1/statuses/{status_id}"
    context_url = f"https://{INSTANCE}/api/v1/statuses/{status_id}/context"
    
    try:
        # 1. Get Status with headers
        s_resp = requests.get(status_url, headers=headers, timeout=10)
        s_resp.raise_for_status()
        status_data = s_resp.json()

        # 2. Get Context with headers
        c_resp = requests.get(context_url, headers=headers, timeout=10)
        c_resp.raise_for_status()
        context_data = c_resp.json()

        replies = context_data.get('descendants', [])

        return {
            "replies_count": status_data.get('replies_count', len(replies)), 
            "reblogs_count": status_data.get('reblogs_count', 0),
            "favourites_count": status_data.get('favourites_count', 0),
            "url": status_data.get('url'),
            "descendants": replies
        }
    except Exception as e:
        print(f"   [!] Error fetching ID {status_id}: {e}")
        return None

def sync_mastodon_comments():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    temp_db = "temp_publii_full_sync.sqlite"
    shutil.copyfile(DB_PATH, temp_db)

    try:
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        print("[*] Starting FULL sync of all published posts...")
        
        # UNRESTRICTED QUERY: No dates, no limits.
        query = """
        SELECT p.title, ad.value 
        FROM posts p
        JOIN posts_additional_data ad ON p.id = ad.post_id
        WHERE p.status = 'published' 
          AND ad.key = 'postViewSettings'
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        sync_count = 0
        for title, settings_json in rows:
            try:
                settings = json.loads(settings_json)
                m_id_obj = settings.get('mastodonId', {})
                
                # Check if it's a dict or a direct value
                m_id = m_id_obj.get('value') if isinstance(m_id_obj, dict) else m_id_obj

                if m_id:
                    print(f"[*] Syncing: {title} (ID: {m_id})")
                    data = fetch_comments_with_stats(m_id)
                    
                    if data:
                        output_path = os.path.join(OUTPUT_DIR, f"{m_id}.json")
                        with open(output_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        sync_count += 1
                        
                        # Anti-spam delay: helps prevent your instance from getting annoyed
                        time.sleep(0.5) 
            except Exception as e:
                print(f"   [!] Skipping {title} due to error: {e}")

        print(f"\n[✔] Success! {sync_count} posts updated in total.")

    except Exception as e:
        print(f"\n[X] A script error occurred: {e}")
    finally:
        conn.close()
        if os.path.exists(temp_db):
            os.remove(temp_db)

if __name__ == "__main__":
    sync_mastodon_comments()