# MedRecruit Job Scraper

This project is a web scraper that extracts job listings from [MedRecruit](https://medrecruit.medworld.com/jobs/list) using Playwright.

## Features
- Scrapes job postings including:
  - Job Title
  - Department
  - Location (Suburb & State)
  - Job Type
  - Duration
  - Job URL
- Automatically paginates through job listings until 30 jobs are collected.
- Saves the extracted job data into an Excel file (`data/scrape_medrecruit.xlsx`).

## Requirements
- Python 3.7+
- Playwright
- Pandas

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/andrepradika/scrape-medrecruit.medworld.com.git
   cd scrape-medrecruit.medworld.com
   ```
2. Install dependencies:
   ```sh
   pip install playwright pandas
   ```
3. Install Playwright browsers:
   ```sh
   playwright install
   ```

## Usage
Run the script using:
```sh
python main.py
```

## Output
The script will generate an Excel file with job data:
- `data/scrape_medrecruit.xlsx`

## Notes
- Runs Playwright in **headless mode** for efficiency.
- Stops scraping once **30 job listings** are collected.
- Checks for pagination and continues to the next page if available.

## License
This project is licensed under the MIT License.

## Author
andrepradika

