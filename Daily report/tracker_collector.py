"""
Tracker Collector: Scrapes daily metrics from tracker.zingplay.com/gsnreport/accactive
Data is server-rendered into Highcharts series — no separate API needed.
"""
import json
import logging
import re
import warnings
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")

from config import TRACKER_URL, TRACKER_SESSION, TIMEZONE

logger = logging.getLogger(__name__)

# Metrics to extract and their display names
SERIES_MAP = {
    "A1":        "dau",
    "A1_Android":"dau_android",
    "A1_iOS":    "dau_ios",
    "N1":        "new_installs",
    "Install_Android": "install_android",
    "Install_iOS":     "install_ios",
    "RevGross":  "revenue_gross",
    "RevNet":    "revenue_net",
    "P1":        "payers",
    "FPU":       "first_payers",
    "ARPU":      "arpu",
    "ARPPU":     "arppu",
    "PR":        "payment_rate",
    "RR1":       "rr1",
    "RR7":       "rr7",
    "RR30":      "rr30",
    "A7":        "a7",
    "A30":       "a30",
}


def _make_session() -> requests.Session:
    """Session với PHPSESSID cookie — dùng cookies jar để server tự set thêm cookies."""
    s = requests.Session()
    s.cookies.set("PHPSESSID", TRACKER_SESSION,
                  domain="tracker.zingplay.com", path="/")
    s.verify = False
    return s


def _get_page(session: requests.Session, app_name: str, country: str,
              from_date: str, to_date: str) -> str:
    """Fetch the accactive page with given filters via POST."""
    url = f"{TRACKER_URL}/gsnreport/accactive"

    # GET để nhận CSRF token và set cookies từ server
    r = session.get(url, timeout=15)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    token_input = soup.find("input", {"name": "_token"})
    if not token_input:
        raise ValueError("CSRF token not found on page")
    csrf = token_input["value"]

    # POST với filters — session đã có đủ cookies từ GET
    r2 = session.post(url, data={
        "_token":   csrf,
        "Country":  country,
        "AppName":  app_name,
        "FromDate": from_date,
        "ToDate":   to_date,
    }, headers={
        "Referer": url,
        "X-Requested-With": "XMLHttpRequest",
    }, timeout=30)
    r2.raise_for_status()
    return r2.text


def _parse_series(html: str) -> tuple[list[str], dict[str, list]]:
    """Extract categories (dates) and all series data from Highcharts HTML."""
    # Dates
    cats = re.findall(r"categories\s*:\s*(\[[^\]]+\])", html)
    dates = json.loads(cats[0]) if cats else []

    # Series: {"name":"...", "id":"...", "data":[...]}
    series_raw = re.findall(
        r'\{"name":"([^"]+)","id":"[^"]+","data":\[([^\]]+)\]',
        html
    )

    series = {}
    for name, data_str in series_raw:
        vals = []
        for v in data_str.split(","):
            v = v.strip()
            try:
                vals.append(float(v) if v != "null" else None)
            except ValueError:
                vals.append(None)
        series[name] = vals

    return dates, series


def _build_snapshot(dates: list[str], series: dict[str, list],
                    target_date_str: str) -> dict:
    """
    Extract values for a specific date (MM-DD format) from series.
    Returns dict of metric_name -> value.
    """
    # Find index of target date in categories (format MM-DD)
    target_short = target_date_str[5:]  # "2026-03-28" -> "03-28"

    if target_short in dates:
        idx = dates.index(target_short)
    else:
        idx = len(dates) - 1  # fallback: last available

    snapshot = {"date": dates[idx] if dates else target_short}
    for series_name, field_name in SERIES_MAP.items():
        vals = series.get(series_name, [])
        snapshot[field_name] = vals[idx] if idx < len(vals) else None

    return snapshot


def collect_tracker_metrics(report_date: date,
                            app_name: str = "cotyphu",
                            country: str = "") -> dict:
    """
    Fetch tracker metrics for report_date and comparison dates.
    Returns structured dict matching data_collector format.
    """
    if not TRACKER_SESSION:
        logger.error("TRACKER_SESSION not set!")
        return {}

    # Fetch enough history to cover D-8
    from_date = (report_date - timedelta(days=35)).strftime("%Y-%m-%d")
    to_date = report_date.strftime("%Y-%m-%d")

    session = _make_session()
    try:
        html = _get_page(session, app_name, country, from_date, to_date)
    except Exception as e:
        logger.error(f"Failed to fetch tracker page: {e}")
        return {}

    dates, series = _parse_series(html)
    logger.info(f"Tracker: got {len(series)} series, {len(dates)} dates "
                f"({dates[0] if dates else '?'} ... {dates[-1] if dates else '?'})")

    d1 = report_date
    d2 = report_date - timedelta(days=1)
    d8 = report_date - timedelta(days=7)

    # avg_7d: compute mean of D-7 to D-1 for each metric
    avg = {}
    for series_name, field_name in SERIES_MAP.items():
        vals_7d = []
        for offset in range(1, 8):
            d = report_date - timedelta(days=offset)
            short = d.strftime("%m-%d")
            if short in dates:
                idx = dates.index(short)
                v = series.get(series_name, [None] * (idx + 1))
                val = v[idx] if idx < len(v) else None
                if val is not None:
                    vals_7d.append(val)
        avg[field_name] = round(sum(vals_7d) / len(vals_7d), 2) if vals_7d else None

    return {
        "source": "tracker",
        "report_date": report_date.strftime("%Y-%m-%d"),
        "app_name": app_name,
        "D-1": _build_snapshot(dates, series, d1.strftime("%Y-%m-%d")),
        "D-2": _build_snapshot(dates, series, d2.strftime("%Y-%m-%d")),
        "D-8": _build_snapshot(dates, series, d8.strftime("%Y-%m-%d")),
        "avg_7d": avg,
    }


if __name__ == "__main__":
    import pytz
    from datetime import datetime
    import logging
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(name)s %(levelname)s %(message)s")

    from dotenv import load_dotenv
    load_dotenv()

    tz = pytz.timezone(TIMEZONE)
    report_date = datetime.now(tz).date() - timedelta(days=1)

    print(f"Fetching tracker metrics for {report_date}...")
    data = collect_tracker_metrics(report_date)
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
