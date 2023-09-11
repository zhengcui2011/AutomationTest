from playwright.sync_api import sync_playwright

# Configuration
VISIT_RESULT = 3  # Visit the third result
IMAGE_PATH = "image_path.jpg"
SCREENSHOT_PATH = "screenshot.png"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()

        # Open mage Search Page in Baidu
        page = context.new_page()
        page.goto("https://image.baidu.com/")

        # Upload the image for searching
        # this method in playwright is better than Selenium, which will avoid window dialog pop up, which selenium can
        # not handle, have to use the third party tool AutoIT
        file_input = page.locator('input[type="file"]')
        file_input.set_input_files(IMAGE_PATH)

        # Wait for search results to load
        page.wait_for_selector('xpath=.//div/img_container/img-hover/a')

        # Get a list of elements matching the selector
        results = page.query_selector_all('xpath=.//div/img_container/img-hover/a')

        if 0 <= VISIT_RESULT - 1 < len(results):
            result_to_visit = results[VISIT_RESULT - 1]
            result_to_visit.click()

            # Wait for the page to load
            page.wait_for_load_state('networkidle')

            # Take a screenshot of the last visited page
            page.screenshot(path=SCREENSHOT_PATH)

            # Perform validation: Check if the title of the page contains a relevant keyword
            expected_keyword = "The expected keyword"
            if expected_keyword in page.title():
                print(f"Validation: Page title contains '{expected_keyword}' - Validation PASSED")
            else:
                print(f"Validation: Page title does not contain '{expected_keyword}' - Validation FAILED")
        else:
            print(f"Invalid VISIT_RESULT: There are only {len(results)} results.")

        # Close the browser
        browser.close()

if __name__ == "__main__":
    main()
