import re
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)
logger.setLevel('INFO')

def fetch_ecfr_recent_agent_changes(agency):
    slug = agency
    base_url = "https://www.ecfr.gov"
    search_url = f"{base_url}/recent-changes?search[agency_slugs][]={slug}&search[date]=current"

    session = requests.Session()

    try:
        logger.info(f"Acquiring session cookies for agency slug: {slug}")
        session.get(base_url)
    except Exception as e:
        logger.error(f"Failed to acquire session cookies: {e}")
        return {"change_history": {"range": "Unavailable", "items": []}}

    try:
        logger.info(f"Fetching recent changes for agency slug: {slug}")
        logger.info("session: {session}")
        response = session.get(search_url, headers={
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        })
        response.raise_for_status()
        html_content = response.text
    except Exception as e:
        logger.error(f"Failed to fetch recent changes for {slug}: {e}")
        return {"change_history": {"range": "Unavailable", "items": []}}

    soup = BeautifulSoup(html_content, "html.parser")

    range_text = "Range not found"
    message_div = soup.find("div", class_="message")
    if message_div:
        raw_msg = message_div.get_text(strip=True)
        range_text = raw_msg.replace("Displaying ", "", 1).replace("changes", "Changes", 1)

    items = []
    current_date = None

    for tag in soup.find_all(["a", "li"]):
        if tag.name == "a":
            href = tag.get("href", "")
            if re.match(r"^/issues/\d{4}/\d{2}/\d{2}$", href):
                current_date = tag.get_text(strip=True)
                continue

        if tag.name == "li" and "recent-change-result" in tag.get("class", []) and current_date:
            a_tag = tag.find("a")
            if a_tag:
                raw_item_text = a_tag.get_text(strip=True)
                item_text = raw_item_text.replace("§", "").strip()
                item_href = a_tag.get("href", "")
                path = ""
                if item_href:
                    full_url = f"{base_url}{item_href}" if item_href.startswith("/") else item_href
                    path_parts = re.sub(
                        r"https://www\.ecfr\.gov/compare/\d{4}-\d{2}-\d{2}/to/\d{4}-\d{2}-\d{2}/",
                        "",
                        full_url
                    ).strip("/").split("/")
                    path = "->".join(path_parts + [item_text])
                items.append({
                    "date": current_date,
                    "item": item_text,
                    "path": path
                })

    logger.info(f"{len(items)} change items found for agency slug: {slug}")
    return {
        "change_history": {
            "range": range_text,
            "items": items
        }
    }