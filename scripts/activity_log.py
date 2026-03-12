import os
import json
import urllib.request
import threading

WEBHOOK_URL = "https://azoni.ai/.netlify/functions/log-agent-activity"


def log_activity(type, title, description=""):
    secret = os.environ.get("AGENT_WEBHOOK_SECRET")
    if not secret:
        return

    def _send():
        try:
            data = json.dumps({
                "type": type,
                "title": title,
                "description": description[:500],
                "source": "azoni-ai",
                "secret": secret,
            }).encode()
            req = urllib.request.Request(
                WEBHOOK_URL,
                data=data,
                headers={"Content-Type": "application/json"},
            )
            urllib.request.urlopen(req, timeout=10)
        except Exception:
            pass

    threading.Thread(target=_send, daemon=True).start()
