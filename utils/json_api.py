import json
from typing import Any, Dict

import config
import requests
import base64


def update_json(data: Dict[str, Any]) -> Dict[str, str]:
    json_str = json.dumps(data)
    message_bytes = json_str.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode("ascii")
    r = requests.get(f"{config.JSON_API_ENDPOINT}&data={base64_message}")
    return json.loads(r.json())


def fetch_json() -> Dict[str, Any]:
    r = requests.get(config.JSON_API_ENDPOINT)
    return json.loads(r.json())
