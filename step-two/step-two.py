from playwright.sync_api import sync_playwright


def run():
    with sync_playwright() as p:
        # Launch the browser in visible mode (headless=False)
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1. Navigate to Wikipedia
        print("Navigating to Wikipedia...")
        page.goto("https://www.wikipedia.org")

        # 2. LOCATORS & TYPING (Interaction)
        # We need to find the search box first.
        # Inspection shows it has an input tag with name="search".
        print("Typing 'Web scraping' into the search box...")

        # 'locator' is the method to find elements. 'fill' types text into it.
        page.locator('input[name="search"]').fill("Web scraping")

        # Optional: Wait a bit just to see the text being typed (for demo purposes)
        page.wait_for_timeout(1000)

        # 3. CLICKING (Interaction)
        # We find the search button. It usually has a type="submit" or specific class.
        print("Clicking the search button...")
        page.locator('button[type="submit"]').click()

        # 4. EXTRACTING DATA (Verification)
        # After clicking, we expect a new page. Let's grab the main article heading.
        # The main heading on Wikipedia articles usually has the ID 'firstHeading'.
        article_title = page.locator('#firstHeading').inner_text()

        print(f"Successfully reached the article: '{article_title}'")

        # Wait a bit before closing
        page.wait_for_timeout(2000)

        browser.close()
        print("Browser closed.")


if __name__ == "__main__":
    run()