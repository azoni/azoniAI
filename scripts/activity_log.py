"""
Fire-and-forget activity logger — logs to MCP ecosystem feed.
"""
import os
import json
import urllib.request
import threading

MCP_URL = os.environ.get('MCP_URL', 'https://azoni-mcp.onrender.com')
MCP_KEY = os.environ.get('MCP_ADMIN_KEY')


def log_activity(type='activity', title='Activity', description=''):
    if not MCP_KEY:
        return

    def _send():
        try:
            data = json.dumps({
                'type': type,
                'title': title,
                'source': 'azoni-ai',
                'description': description[:500],
            }).encode()
            req = urllib.request.Request(
                f'{MCP_URL}/activity/log',
                data=data,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {MCP_KEY}',
                },
            )
            urllib.request.urlopen(req, timeout=10)
        except Exception:
            pass

    threading.Thread(target=_send, daemon=True).start()
