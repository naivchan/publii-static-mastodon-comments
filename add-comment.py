import json
import os
from datetime import datetime

# ================= CONFIGURATION =================
# Same directory as your Mastodon JSONs
COMMENTS_DIR = r'C:\Users\[PC User Name]\Documents\Publii\sites\[your-site]\input\media\files\comments'
# =================================================

def add_manual_comment():
    print("--- Manual Comment Helper ---")
    m_id = input("Enter the Mastodon ID of the post: ").strip()
    
    name = input("Commenter Name: ")
    handle = input("Handle (e.g. Reader@web): ") or "Reader@web"
    content = input("Comment Content: ")
    
    # Optional: If you want to reply to a specific comment
    reply_to = input("Reply to specific ID? (Press Enter for none): ").strip() or None

    file_path = os.path.join(COMMENTS_DIR, f"{m_id}-manual.json")
    
    # Load existing manual comments or start new
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"descendants": []}

    # Create new entry
    new_comment = {
        "id": f"manual-{int(datetime.now().timestamp())}", # Unique ID based on time
        "created_at": datetime.now().isoformat() + "Z",
        "in_reply_to_id": reply_to,
        "content": f"<p>{content}</p>",
        "account": {
            "acct": handle,
            "display_name": name,
            "avatar": "/media/files/comments/default-avatar.png", # Default avatar
            "url": "#"
        },
        "media_attachments": []
    }

    data["descendants"].append(new_comment)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\n[✔] Added! Saved to {m_id}-manual.json")

if __name__ == "__main__":

    add_manual_comment()
