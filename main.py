import asyncio
from playwright.async_api import async_playwright
import pandas as pd

async def scrape_jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Navigate to the job listings page
        base_url = "https://medrecruit.medworld.com/jobs/list?location=New+South+Wales&page="
        page_number = 1
        jobs = []
        
        while True:
            await page.goto(f"{base_url}{page_number}")
            await page.wait_for_timeout(2000)  # Wait for the page to load
            
            # Extract job listings on the current page
            job_listings = await page.query_selector_all('[data-testid="job-card"]')
            
            if not job_listings:
                print("No job listings found on this page.")
                break
            
            for job in job_listings:
                if len(jobs) >= 30:  # Stop if we have collected 30 jobs
                    break
                
                title = await job.query_selector('h2[data-testid="job-card-speciality"]')
                title_text = await title.inner_text() if title else 'N/A'
                
                department = await job.query_selector('p[data-testid="job-card-grade"]')
                department_text = await department.inner_text() if department else 'N/A'
                
                location = await job.query_selector('[data-testid="Location"]')
                location_text = await location.inner_text() if location else 'N/A'
                suburb, state = location_text.split(',') if ',' in location_text else (location_text, 'N/A')
                suburb = suburb.strip()
                state = state.strip()
                
                job_type = await job.query_selector('[data-testid="Work Type"]')
                job_type_text = await job_type.inner_text() if job_type else 'N/A'
                
                duration = await job.query_selector('[data-testid="Date"]')
                duration_text = await duration.inner_text() if duration else 'N/A'
                
                url = await job.query_selector('a.JobCard_title__jdBTC')
                url_link = await url.get_attribute('href') if url else 'N/A'
                
                jobs.append({
                    'Job Title': title_text,
                    'Department': department_text,
                    'Location': suburb,
                    'State': state,
                    'Job Type': job_type_text,
                    'Duration': duration_text,
                    'URL': 'https://medrecruit.medworld.com' + url_link
                })
            
            if len(jobs) >= 30:  # Stop if we have collected 30 jobs
                break
            
            # Check for the next page button
            next_page_button = await page.query_selector('button[aria-label="Go to next page"]')
            if next_page_button and not await next_page_button.is_disabled():
                page_number += 1
            else:
                break  # Exit the loop if there are no more pages
        
        await browser.close()
        
        # Create DataFrame
        df = pd.DataFrame(jobs)

        # Save to Excel
        df.to_excel('data/scrape_madrecuit.xlsx', index=False)

# Run the scraper
asyncio.run(scrape_jobs())
