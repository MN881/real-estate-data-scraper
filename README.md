# 🏡 Real Estate Data Scraper

An asynchronous Python web scraping pipeline built to extract, normalize, and export structured real estate property listings across multiple US states (Minnesota, Texas, and Washington).

## 🚀 Key Features
* **Bot-Evasion & Async Execution**: Uses `nodriver` (undetected Chrome automation) with randomized delays to bypass bot checks and scrape paginated search results reliably.
* **Embedded JSON Extraction**: Parses Next.js (`script#__NEXT_DATA__`) hydration payloads directly from the DOM using `BeautifulSoup` and `lxml`, avoiding fragile CSS selector scraping.
* **Automated Data Normalization**:
  * Standardizes lot sizes by converting `acres` into `sqft` (`1 acre = 43,560 sqft`).
  * Extracts nested geolocation coordinates (`Latitude`, `Longitude`), broker attributions, price reductions, and property image arrays.
* **Structured Output**: Exports clean, analysis-ready tabular data to `propsData.csv`.

## 🛠️ Tech Stack
* **Language**: Python 3.10+
* **Browser Automation**: `nodriver`, `asyncio`
* **Parsing**: `BeautifulSoup4`, `lxml`, `json`
* **Data Export**: Python `csv` module

## 📊 Data Schema (`propsData.csv`)

| Column | Description | Example |
| :--- | :--- | :--- |
| `Price` | Formatted listing price | `$485,000` |
| `Living Area(sqft)` | Interior square footage | `2586` |
| `Total Area(sqft)` | Standardized lot size in sq. ft. | `11020.68` |
| `Beds` / `Baths` | Bedroom and bathroom counts | `4` / `3` |
| `Address`, `City`, `State`, `Zip Code` | Full location details | `20795 Gemini Trl, Lakeville, MN 55044` |
| `Latitude` / `Longitude` | Exact geographic coordinates | `44.648506` / `-93.20928` |
| `Home Type` | Property classification | `SINGLE_FAMILY`, `TOWNHOUSE`, `CONDO`, `LOT` |
| `Days on Zillow` | Listing age | `2` |
| `PriceReduction` | Recent price drop & date | `$12,000 (Nov 19)` |
| `Broker` | Listing agency | `Epique Realty` |

## ⚙️ Setup & Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com
   cd real-estate-data-scraper
   ```

2. **Install dependencies**
   ```bash
   pip install nodriver  BeautifulSoup4
   ```

3. **Run the scraper**
   ```bash
   python real_estate_.py
   ```
   *The script will launch a browser session, iterate through the configured states and pagination limits, and output `propsData.csv`.*

## ⚠️ Disclaimer
This project is for educational and portfolio demonstration purposes only. Please respect website `robots.txt` policies and Terms of Service when running web scrapers.
