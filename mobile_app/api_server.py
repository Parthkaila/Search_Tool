from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import re
import time
from urllib.parse import quote_plus
from typing import Dict, Set

app = FastAPI(title="Google Maps Scraper API")

# Enable CORS for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAPS_SEARCH_BASE = "https://www.google.com/maps/search/"


class ScrapeRequest(BaseModel):
    keyword: str
    location: Optional[str] = ""
    max_results: int = 20


class ScrapeResponse(BaseModel):
    results: List[Dict]
    count: int


def build_driver(headless: bool = True) -> webdriver.Chrome:
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1600,1000")
    options.add_argument("--lang=en")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(45)
    return driver


def extract_lat_lng(url: str) -> Dict[str, str]:
    match = re.search(r"!3d(-?\d+(?:\.\d+)?)!4d(-?\d+(?:\.\d+)?)", url)
    if not match:
        return {"latitude": "", "longitude": ""}
    return {"latitude": match.group(1), "longitude": match.group(2)}


def safe_text(driver: webdriver.Chrome, css_selector: str) -> str:
    try:
        element = driver.find_element(By.CSS_SELECTOR, css_selector)
        return (element.text or "").strip()
    except Exception:
        return ""


def safe_href(driver: webdriver.Chrome, css_selector: str) -> str:
    try:
        element = driver.find_element(By.CSS_SELECTOR, css_selector)
        return (element.get_attribute("href") or "").strip()
    except Exception:
        return ""


def find_place_urls(driver: webdriver.Chrome, query: str, max_results: int) -> List[str]:
    search_url = f"{MAPS_SEARCH_BASE}{quote_plus(query)}"
    driver.get(search_url)

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/maps/place/']"))
        )
    except TimeoutException:
        return []

    collected: Set[str] = set()
    stagnant_cycles = 0

    while len(collected) < max_results and stagnant_cycles < 7:
        anchors = driver.find_elements(By.CSS_SELECTOR, "a[href*='/maps/place/']")
        before = len(collected)
        for anchor in anchors:
            href = (anchor.get_attribute("href") or "").strip()
            if href and "/maps/place/" in href:
                collected.add(href)
                if len(collected) >= max_results:
                    break

        if len(collected) == before:
            stagnant_cycles += 1
        else:
            stagnant_cycles = 0

        try:
            panel = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
            panel.send_keys(Keys.END)
        except Exception:
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(1.2)

    return list(collected)[:max_results]


def extract_place_details(driver: webdriver.Chrome, place_url: str) -> Dict:
    try:
        driver.get(place_url)
    except Exception:
        return {}

    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
        )
    except TimeoutException:
        return {}

    name = safe_text(driver, "h1")
    address = safe_text(driver, "button[data-item-id='address'] div.fontBodyMedium")
    phone = safe_text(driver, "button[data-item-id*='phone'] div.fontBodyMedium")
    website = safe_href(driver, "a[data-item-id='authority']")

    rating = safe_text(driver, "div.F7nice span[aria-hidden='true']")
    user_ratings_total = ""
    try:
        rating_button = driver.find_element(By.CSS_SELECTOR, "button[jsaction*='pane.rating.moreReviews']")
        aria_label = rating_button.get_attribute("aria-label") or ""
        match = re.search(r"([\d,]+)\s+reviews", aria_label)
        if match:
            user_ratings_total = match.group(1).replace(",", "")
    except Exception:
        user_ratings_total = ""

    lat_lng = extract_lat_lng(driver.current_url)
    place_id = ""
    place_id_match = re.search(r"0x[0-9a-fA-F]+:0x[0-9a-fA-F]+", driver.current_url)
    if place_id_match:
        place_id = place_id_match.group(0)

    return {
        "name": name,
        "place_id": place_id,
        "formatted_address": address,
        "formatted_phone_number": phone,
        "international_phone_number": "",
        "website": website,
        "rating": rating,
        "user_ratings_total": user_ratings_total,
        "business_status": "",
        "types": "",
        "latitude": lat_lng["latitude"],
        "longitude": lat_lng["longitude"],
        "google_maps_url": driver.current_url,
    }


@app.get("/")
async def root():
    return {"message": "Google Maps Scraper API", "status": "online"}


@app.post("/api/scrape", response_model=ScrapeResponse)
async def scrape_maps(request: ScrapeRequest):
    driver = None
    try:
        query = request.keyword
        if request.location:
            query = f"{request.keyword} in {request.location}"
        
        driver = build_driver(headless=True)
        
        place_urls = find_place_urls(driver, query, request.max_results)
        results = []
        
        for place_url in place_urls:
            detail = extract_place_details(driver, place_url)
            if detail:
                detail["keyword"] = request.keyword
                results.append(detail)
        
        return ScrapeResponse(results=results, count=len(results))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
