from playwright.sync_api import sync_playwright


def run():
    # Start Playwright using the context manager
    with sync_playwright() as p:
        # Launch Chromium browser.
        # headless=False means we can see the browser UI. Set it to True for background execution.
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)

        # Create a new browser page (tab)
        page = browser.new_page()

        # Define the target URL
        url = "https://www.wikipedia.org"

        # Navigate to the specified URL
        print(f"Navigating to {url}...")
        page.goto(url)

        # Get the page title to verify we are at the right place
        page_title = page.title()
        print(f"Page Title: {page_title}")

        # Example: Taking a screenshot of the landing page
        # This saves a screenshot in the current directory
        page.screenshot(path="step_one_screenshot.png")
        print("Screenshot saved as 'step_one_screenshot.png'.")

        # Wait for a few seconds to visually confirm everything before closing
        print("Waiting for 3 seconds...")
        page.wait_for_timeout(3000)

        # Close the browser instance
        browser.close()
        print("Browser closed.")


if __name__ == "__main__":
    run()