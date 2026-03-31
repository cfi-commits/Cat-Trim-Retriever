from datetime import datetime
from typing import List, Dict, Any

from deta import Deta

deta = Deta()  # In Deta Space, credentials are provided automatically
logs_db = deta.Base("trim_access_logs")


def log_request(
    part_number: str,
    serial_number: str,
    client_ip: str,
    success: bool,
    message: str = "",
) -> None:
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "part_number": part_number.strip(),
        "serial_number": serial_number.strip(),
        "client_ip": client_ip,
        "success": success,
        "message": message,
    }
    logs_db.put(entry)


def fetch_logs(limit: int = 200) -> List[Dict[str, Any]]:
    # Simple scan; for small admin tools this is fine
    res = logs_db.fetch()
    items = res.items

    while res.last and len(items) < limit:
        res = logs_db.fetch(last=res.last)
        items.extend(res.items)

    # Sort newest first
    items.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return items[:limit]