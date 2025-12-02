import csv
from playwright.sync_api import sync_playwright


def run():
    csv_filename = "books_pagination.csv"

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        url = "http://books.toscrape.com/"
        print(f"Navigating to {url}...")
        page.goto(url)

        # Open CSV file once, keep it open during the loop
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Price", "Availability"])

            page_number = 1
            max_pages = 3  # LIMIT: Scrape only first 3 pages for testing. Set to None for all.

            # Start the main scraping loop
            while True:
                print(f"--- Scraping Page {page_number} ---")

                # 1. Scrape the books on current page
                books = page.locator(".product_pod")
                count = books.count()

                for i in range(count):
                    current_book = books.nth(i)
                    title = current_book.locator("h3 a").get_attribute("title")
                    price = current_book.locator(".price_color").inner_text()
                    availability = current_book.locator(".instock.availability").inner_text().strip()

                    writer.writerow([title, price, availability])

                print(f"Saved {count} books from page {page_number}.")

                # Check loop limit (Optional logic for testing)
                if max_pages and page_number >= max_pages:
                    print("Page limit reached. Stopping.")
                    break

                # 2. Pagination Logic: Check if 'Next' button exists
                # The 'Next' button selector is usually specific. Here it is 'li.next a'
                next_button = page.locator("li.next a")

                if next_button.count() > 0:
                    print("Clicking 'Next' button...")
                    next_button.click()

                    # Vital: Wait for the next page to load.
                    # We wait for the list of books to be visible again/refreshed.
                    page.wait_for_timeout(2000)  # Simple wait (better strategies exist)

                    page_number += 1
                else:
                    print("No 'Next' button found. End of pagination.")
                    break

        print(f"\nScraping finished. Check '{csv_filename}'.")
        browser.close()


if __name__ == "__main__":
    run()