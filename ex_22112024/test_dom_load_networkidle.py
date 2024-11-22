from playwright.sync_api import sync_playwright, expect
import time

def test_domcont_load_networkidle():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False,slow_mo=200)
        page = browser.new_page()

        # Navigate to the page
        page.goto("https://app.vwo.com")

        # Wait for DOM to load
        page.wait_for_load_state("domcontentloaded")
        print("DOM fully loaded.")

        # Wait for all resources to load
        page.wait_for_load_state("load")
        print("Page and resources fully loaded.")

        page.wait_for_load_state("networkidle")
        print("Network is idle. Page is fully ready.")


        page.locator("input#login-username").fill("admin@gmail.com")
        page.locator("input#login-password").fill("admin123")
        page.locator("button#js-login-btn").click()
        expect(page).to_have_title("Login - VWO")


        try:
            page.locator("div#js-notification-box-msg").wait_for()
            error_message1 = page.locator("div#js-notification-box-msg").text_content()
            print(f"Error message: {error_message1}")
        except:
            pass
        error_message = page.locator("div#js-notification-box-msg")
        expect(error_message).to_have_text("Your email, password, IP address or location did not match")



        browser.close()
