import csv
from playwright.sync_api import sync_playwright


def run():
    # Define the output filename
    csv_filename = "books.csv"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        url = "http://books.toscrape.com/"
        print(f"Navigating to {url}...")
        page.goto(url)

        # Locate all book articles
        books = page.locator(".product_pod")
        count = books.count()
        print(f"Found {count} books. Starting export to '{csv_filename}'...")

        # --- CSV FILE OPERATIONS ---
        # We open a file in 'write' mode (w).
        # newline='' is required by the csv module to prevent empty lines between rows on Windows.
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write the Header row (Column names)
            writer.writerow(["Title", "Price", "Availability"])

            # Loop through the books
            for i in range(count):
                current_book = books.nth(i)

                # 1. Title
                title = current_book.locator("h3 a").get_attribute("title")

                # 2. Price
                price = current_book.locator(".price_color").inner_text()

                # 3. Availability (Extra info: Is it in stock?)
                # It's inside a <p> tag with class 'instock availability'
                # We use .strip() to remove extra spaces/newlines from the text.
                availability = current_book.locator(".instock.availability").inner_text().strip()

                # Write the data row to the CSV file
                writer.writerow([title, price, availability])

                # Print to console just to show progress
                print(f"Saved: {title}")

        print(f"\nSuccess! Data saved to {csv_filename}")

        page.wait_for_timeout(2000)
        browser.close()


if __name__ == "__main__":
    run()