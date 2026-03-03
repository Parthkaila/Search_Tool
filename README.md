# Google Maps Keyword Data Collector (with Filters + Excel Export)

This software lets you:
- Search Google Maps business data by **user keywords**.
- Collect details (name, address, phone, website, rating, coordinates, map URL, etc.).
- Apply filters such as:
  - Remove duplicate data
  - Remove rows without phone number
- Export the final dataset to an **Excel (.xlsx)** file.

## Important
This app works by opening **Google Maps directly in Chrome** and reading visible listing details.

**Local use**: Install Python and dependencies
**Website hosting**: See [DEPLOYMENT.md](DEPLOYMENT.md) for free hosting options

You need:
1. Google Chrome installed
2. Internet connection
3. Python dependencies installed

## Setup

```powershell
cd "d:\Python Word Dox Formating Software"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

If Chrome driver is downloaded slowly on first run, wait once. Next runs are faster.

## How to use
1. Enter one or multiple keywords (one per line or comma-separated).
2. Optional: set a location text (example: `Lahore, Pakistan`).
3. Click **Collect Data**.
4. Enable/disable filter options:
   - Remove duplicates
   - Remove rows without phone number
5. Click **Download Excel**.

## Notes
- Some places may not have phone numbers or websites in Google Maps details.
- Google Maps page layout can change over time; selectors may need updates if Google changes UI.
