import io
import re
import time
from urllib.parse import quote_plus
from datetime import datetime
from typing import Dict, List, Optional, Set

import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

MAPS_SEARCH_BASE = "https://www.google.com/maps/search/"


def parse_keywords(raw_text: str) -> List[str]:
    chunks = [part.strip() for line in raw_text.splitlines() for part in line.split(",")]
    return [item for item in chunks if item]


def build_driver(headless: bool = True) -> webdriver.Chrome:
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1600,1000")
    options.add_argument("--lang=en")
    options.add_argument("--disable-blink-features=AutomationControlled")

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


def find_place_urls(
    driver: webdriver.Chrome,
    query: str,
    max_results_per_keyword: int,
) -> List[str]:
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

    while len(collected) < max_results_per_keyword and stagnant_cycles < 7:
        anchors = driver.find_elements(By.CSS_SELECTOR, "a[href*='/maps/place/']")
        before = len(collected)
        for anchor in anchors:
            href = (anchor.get_attribute("href") or "").strip()
            if href and "/maps/place/" in href:
                collected.add(href)
                if len(collected) >= max_results_per_keyword:
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

    return list(collected)[:max_results_per_keyword]


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


def build_dataframe(rows: List[Dict]) -> pd.DataFrame:
    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    desired_order = [
        "keyword",
        "name",
        "place_id",
        "formatted_address",
        "formatted_phone_number",
        "international_phone_number",
        "website",
        "rating",
        "user_ratings_total",
        "business_status",
        "types",
        "latitude",
        "longitude",
        "google_maps_url",
    ]

    cols = [col for col in desired_order if col in df.columns] + [
        col for col in df.columns if col not in desired_order
    ]
    return df[cols]


def apply_filters(
    df: pd.DataFrame,
    remove_duplicates: bool,
    remove_without_phone: bool,
) -> pd.DataFrame:
    filtered = df.copy()

    if remove_duplicates and not filtered.empty:
        subset = ["place_id"] if "place_id" in filtered.columns else None
        filtered = filtered.drop_duplicates(subset=subset, keep="first")

    if remove_without_phone and "formatted_phone_number" in filtered.columns:
        phone_col = filtered["formatted_phone_number"].astype(str).str.strip()
        filtered = filtered[phone_col.notna() & (phone_col != "") & (phone_col != "nan")]

    return filtered.reset_index(drop=True)


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="places_data")
    output.seek(0)
    return output.read()


def main() -> None:
    st.set_page_config(page_title="Maps Keyword Collector", layout="wide")
    st.title("Google Maps Keyword Data Collector")
    st.caption("Search directly on Google Maps, filter collected data, and export to Excel.")

    with st.sidebar:
        st.header("Search Settings")
        location_text = st.text_input("Location (optional)", placeholder="e.g., Karachi, Pakistan")
        max_results_per_keyword = st.number_input(
            "Max results per keyword",
            min_value=1,
            max_value=500,
            value=20,
            step=1,
            help="Set any number of places to collect for each keyword.",
        )
        open_live_browser = st.checkbox("Open Google Maps browser window (live)", value=True)
        show_preview = st.checkbox("Show live screenshot preview in app", value=True)

    raw_keywords = st.text_area(
        "Keywords",
        placeholder="restaurant\ndentist\ngym",
        height=140,
    )

    c1, c2 = st.columns([1, 2])
    with c1:
        run_collect = st.button("Collect Data", type="primary", use_container_width=True)

    if "raw_df" not in st.session_state:
        st.session_state.raw_df = pd.DataFrame()
    if "stop_requested" not in st.session_state:
        st.session_state.stop_requested = False
    if "is_collecting" not in st.session_state:
        st.session_state.is_collecting = False

    # Stop button (shown during collection)
    if st.session_state.is_collecting:
        with c2:
            if st.button("⏹️ Stop Collection", type="secondary", use_container_width=True):
                st.session_state.stop_requested = True
                st.rerun()

    if run_collect:
        st.session_state.stop_requested = False
        st.session_state.is_collecting = True
        
        keywords = parse_keywords(raw_keywords)
        if not keywords:
            st.error("Please enter at least one keyword.")
            st.session_state.is_collecting = False
            st.stop()

        progress = st.progress(0)
        status_box = st.empty()
        timer_box = st.empty()
        current_url_box = st.empty()
        preview_box = st.empty()
        log_box = st.empty()
        log_lines: List[str] = []
        started_at = time.time()
        user_stopped = False

        all_rows: List[Dict] = []
        total_steps = max(len(keywords), 1)
        driver: Optional[webdriver.Chrome] = None

        try:
            status_box.info("Starting Chrome automation...")
            driver = build_driver(headless=not open_live_browser)

            for index, keyword in enumerate(keywords, start=1):
                # Check if user requested stop
                if st.session_state.stop_requested:
                    user_stopped = True
                    log_lines.append("⏹️ Collection stopped by user")
                    log_box.text("\n".join(log_lines[-12:]))
                    break
                
                query = keyword if not location_text else f"{keyword} in {location_text}"
                status_box.info(f"Searching on Maps: {query}")
                timer_box.caption(f"Elapsed time: {int(time.time() - started_at)} sec")
                current_url_box.code(f"Current URL: {driver.current_url if driver.current_url else 'loading...'}")

                place_urls = find_place_urls(
                    driver=driver,
                    query=query,
                    max_results_per_keyword=max_results_per_keyword,
                )

                log_lines.append(f"Keyword '{keyword}': found {len(place_urls)} place links")
                log_box.text("\n".join(log_lines[-12:]))
                timer_box.caption(f"Elapsed time: {int(time.time() - started_at)} sec")
                current_url_box.code(f"Current URL: {driver.current_url if driver.current_url else 'loading...'}")
                if show_preview:
                    try:
                        preview_box.image(driver.get_screenshot_as_png(), caption="Live Maps preview", use_container_width=True)
                    except Exception:
                        pass

                for place_url in place_urls:
                    # Check if user requested stop
                    if st.session_state.stop_requested:
                        user_stopped = True
                        log_lines.append("⏹️ Collection stopped by user")
                        log_box.text("\n".join(log_lines[-12:]))
                        break
                    
                    status_box.info(f"Opening place: {place_url[:90]}...")
                    detail = extract_place_details(driver, place_url)
                    if not detail:
                        continue
                    detail["keyword"] = keyword
                    all_rows.append(detail)

                    timer_box.caption(f"Elapsed time: {int(time.time() - started_at)} sec")
                    current_url_box.code(f"Current URL: {driver.current_url if driver.current_url else 'loading...'}")
                    if show_preview:
                        try:
                            preview_box.image(driver.get_screenshot_as_png(), caption="Live Maps preview", use_container_width=True)
                        except Exception:
                            pass

                # Break outer loop if stopped in inner loop
                if user_stopped:
                    break
                    
                progress.progress(index / total_steps)
        except Exception as exc:
            st.error(f"Collection failed: {exc}")
        finally:
            if driver is not None:
                driver.quit()
            st.session_state.is_collecting = False

        timer_box.caption(f"Elapsed time: {int(time.time() - started_at)} sec")
        
        # Save collected data even if stopped
        st.session_state.raw_df = build_dataframe(all_rows)
        
        if user_stopped:
            status_box.warning(f"⏹️ Collection stopped by user. Showing {len(all_rows)} collected rows.")
        else:
            status_box.success("Data collection completed.")

    raw_df = st.session_state.raw_df

    st.subheader("Filter Options")
    f1, f2 = st.columns(2)
    with f1:
        remove_duplicates = st.checkbox("Remove duplicate data", value=True)
    with f2:
        remove_without_phone = st.checkbox("Remove rows without phone number", value=False)

    filtered_df = apply_filters(
        df=raw_df,
        remove_duplicates=remove_duplicates,
        remove_without_phone=remove_without_phone,
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("Rows collected", int(len(raw_df)))
    m2.metric("Rows after filters", int(len(filtered_df)))
    m3.metric("Keywords", int(len(parse_keywords(raw_keywords))))

    st.subheader("Collected Dataset")
    if filtered_df.empty:
        st.info("No data yet. Enter keywords and click Collect Data.")
    else:
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)
        excel_data = to_excel_bytes(filtered_df)
        filename = f"maps_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        st.download_button(
            "Download Excel",
            data=excel_data,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
