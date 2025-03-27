from services.ecfr_scraper import fetch_ecfr_recent_agent_changes
from fastapi import APIRouter, Request
import json
import re
import time
from api.utils import format_response
import logging

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/api/agencies")
def list_agencies(request: Request):
    start = time.time()
    with open("out.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    result = [
        {
            "name": d.get("name", d.get("agency")),
            "sortable_name": d.get("sortable_name", ""),
            "short_name": d.get("short_name", ""),
            "slug": d.get("slug", "")
        }
        for d in data
    ]
    return format_response(result, start)

@router.get("/api/agencies/hierarchy")
def get_all_hierarchies(request: Request):
    start = time.time()
    with open("out.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    def recurse_children(children):
        structured = []
        for c in children:
            node = {
                "type": c.get("type"),
                "name": c.get("label")
            }
            if c.get("children"):
                if c["type"] == "chapter":
                    node["subchapters"] = recurse_children(c["children"])
                elif c["type"] == "subchapter":
                    node["parts"] = recurse_children(c["children"])
                elif c["type"] == "part":
                    node["sections"] = recurse_children(c["children"])
            structured.append(node)
        return structured

    def transform(agency):
        root = agency.get("structure", {})
        return {
            "agency": agency.get("name", agency.get("agency")),
            "sortable_name": agency.get("sortable_name", ""),
            "short_name": agency.get("short_name", ""),
            "slug": agency.get("slug", ""),
            "type": root.get("type", "chapter"),
            "name": root.get("label", "Unnamed Chapter"),
            "subchapters": recurse_children(root.get("children", []))
        }

    hierarchy = [transform(agency) for agency in data]
    return format_response(hierarchy, start)

@router.get("/api/agencies/history")
def get_agency_histories(request: Request):
    logger.info(f"Cocks I Slop")
    start = time.time()
    try:
        with open("out.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.debug(f"In /api/agencies/history:" )
        enriched = []
        i = 0;
        for item in data:
            if i < 10:
                i = i +1
                logger.info(f"Working on Agency: [{item.get('agency', 'N/A')}]")
                logger.info(f"Agency ok: [{item.get('agency', 'N/A')}]")
                text = item.get('agency', 'turd') 
                slug = re.sub(r'[^\w\s-]', '', text)  # Remove punctuation (if any) 
                slug = slug.lower().replace(' ', '-')
                logger.info(f"Agency slug: [{slug}]")
                change_data = fetch_ecfr_recent_agent_changes(slug)
                if "change_history" in change_data:
                    item["change_history"] = change_data["change_history"]
                enriched.append(item)
                logger.info(f"Enriched: {enriched}")

        return format_response(enriched, start)
    except Exception as e:
        return format_response({}, start, success=False, message=str(e), debug=True)