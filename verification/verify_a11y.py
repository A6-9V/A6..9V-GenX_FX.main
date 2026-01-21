
from playwright.sync_api import sync_playwright

def verify_system_test_results():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto("http://localhost:5173")

            # Wait for System Test Results to appear
            page.wait_for_selector("text=System Test Results")

            # Verify the hidden text is present in the DOM (but not visible)

            # Select the first success item
            success_item = page.locator("li:has-text('Success:')").first
            if success_item.count() > 0:
                print("✅ Found 'Success:' hidden text in DOM")
            else:
                print("❌ 'Success:' hidden text NOT found")

            # Select the first warning item
            warning_item = page.locator("li:has-text('Warning:')").first
            if warning_item.count() > 0:
                print("✅ Found 'Warning:' hidden text in DOM")
            else:
                print("❌ 'Warning:' hidden text NOT found")

            # Take a screenshot
            page.screenshot(path="verification/system_test_results.png")
            print("📸 Screenshot saved to verification/system_test_results.png")

        except Exception as e:
            print(f"❌ Verification failed: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_system_test_results()
