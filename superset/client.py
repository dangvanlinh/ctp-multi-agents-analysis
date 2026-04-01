"""
Superset SQL Lab client — execute ClickHouse queries via Superset API.
Extracted from daily report project, stripped to essentials.
"""

import json
import logging
import os
import uuid

import requests

logger = logging.getLogger(__name__)

# Config from env
SUPERSET_URL = os.getenv("SUPERSET_URL", "https://bitool-hn2.zingplay.com")
SUPERSET_ACCESS_TOKEN = os.getenv("SUPERSET_ACCESS_TOKEN", "")
SUPERSET_DB_ID = int(os.getenv("SUPERSET_DB_ID", "5"))


def _make_session() -> requests.Session:
    """Create requests session with auth token."""
    s = requests.Session()
    if SUPERSET_ACCESS_TOKEN:
        s.headers.update({"Cookie": f"session={SUPERSET_ACCESS_TOKEN}"})
    return s


def _get_csrf_token(session: requests.Session) -> str:
    """Fetch CSRF token required for POST requests."""
    resp = session.get(
        f"{SUPERSET_URL}/api/v1/security/csrf_token/",
        timeout=10,
        verify=False,
    )
    resp.raise_for_status()
    return resp.json().get("result", "")


def query_superset(sql: str) -> list[dict]:
    """
    Execute a SQL query via Superset SQL Lab API.
    Returns rows as list of dicts, or empty list on error.
    """
    if not SUPERSET_ACCESS_TOKEN:
        logger.error("SUPERSET_ACCESS_TOKEN not configured in .env")
        return []

    session = _make_session()

    try:
        csrf_token = _get_csrf_token(session)
    except Exception as e:
        logger.error(f"Failed to get CSRF token: {e}")
        return []

    payload = {
        "database_id": SUPERSET_DB_ID,
        "sql": sql,
        "client_id": str(uuid.uuid4())[:10],
        "queryLimit": 10000,
        "runAsync": False,
    }

    try:
        resp = session.post(
            f"{SUPERSET_URL}/api/v1/sqllab/execute/",
            json=payload,
            headers={
                "X-CSRFToken": csrf_token,
                "Referer": SUPERSET_URL,
            },
            timeout=120,
            verify=False,
        )
        resp.raise_for_status()
        result = resp.json()

        columns = [col["name"] for col in result.get("columns", [])]
        rows = result.get("data", [])

        # Convert list-of-lists to list-of-dicts if needed
        if rows and isinstance(rows[0], list):
            return [dict(zip(columns, row)) for row in rows]

        return rows

    except requests.RequestException as e:
        logger.error(f"Superset query failed: {e}")
        if hasattr(e, "response") and e.response is not None:
            logger.debug(f"Response: {e.response.text[:500]}")
        return []


def format_results_markdown(results: list[dict], query_name: str = "", sql: str = "") -> str:
    """Format query results as readable markdown table."""
    if not results:
        return f"### {query_name}\n> Không có dữ liệu.\n"

    lines = []
    if query_name:
        lines.append(f"### {query_name}")
    if sql:
        lines.append(f"```sql\n{sql.strip()}\n```")

    # Table header
    headers = list(results[0].keys())
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

    # Table rows
    for row in results:
        vals = [str(row.get(h, "")) for h in headers]
        lines.append("| " + " | ".join(vals) + " |")

    lines.append("")
    return "\n".join(lines)
