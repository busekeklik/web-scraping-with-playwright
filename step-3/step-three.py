from playwright.sync_api import sync_playwright


def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1. Navigate to the target website
        # This is a sandbox website specifically designed for scraping practice.
        url = "http://books.toscrape.com/"
        print(f"Navigating to {url}...")
        page.goto(url)

        # 2. Identify the repeating elements (The Books)
        # Each book is contained inside an <article> tag with the class "product_pod".
        # We create a locator that matches ALL of them, not just one.
        books = page.locator(".product_pod")

        # 3. Count how many items we found
        count = books.count()
        print(f"Found {count} books on the page.\n")

        # 4. Iterate (Loop) through the list
        # Since 'books' points to multiple elements, we loop using the count.
        for i in range(count):
            # We grab the 'nth' (current) book in the loop
            current_book = books.nth(i)

            # --- SCOPED LOCATORS ---
            # Instead of searching the whole page, we search ONLY inside 'current_book'.

            # Extract Title: It's inside an <h3> tag, within an <a> tag, in the 'title' attribute.
            book_title = current_book.locator("h3 a").get_attribute("title")

            # Extract Price: It's inside a <p> tag with class "price_color".
            book_price = current_book.locator(".price_color").inner_text()

            # Print the clean data
            print(f"{i + 1}. {book_title} - {book_price}")

        print("\nScraping finished.")

        # Optional: Wait to see the result
        page.wait_for_timeout(3000)
        browser.close()


if __name__ == "__main__":
    run()