import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_alert(message: str, is_error: bool = True):
    if not WEBHOOK_URL or "example" in WEBHOOK_URL:
        print("Warning: Valid DISCORD_WEBHOOK_URL not configured in .env file.")
        return

    embed_color = 15158332 if is_error else 3066993
    status_title = "🚨 [PIPELINE FAILURE]" if is_error else "✅ [PIPELINE SUCCESS]"

    payload = {
        "embeds": [
            {
                "title": status_title,
                "description": message,
                "color": embed_color,
                "footer": {
                    "text": "OpenSky Flight Data Pipeline • Observability System"
                }
            }
        ]
    }
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print("Alert successfully sent to Discord.")
    except Exception as e:
        print(f"Failed to send Discord alert: {e}")

if __name__ == "__main__":
    msg = sys.argv[1] if len(sys.argv) > 1 else "Pipeline test execution triggered."
    is_err = sys.argv[2].lower() == "true" if len(sys.argv) > 2 else True
    send_alert(msg, is_error=is_err)