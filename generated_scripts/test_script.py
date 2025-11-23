import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === CONFIG ===
CHROMEDRIVER_PATH = r"C:\Users\91876\Desktop\qa-autonomous-agent\chromedriver-win64\chromedriver.exe"
# Use the local file URL for the checkout.html in your project
PAGE_URL = "file:///C:/Users/91876/Desktop/qa-autonomous-agent/assets/checkout.html"

def run_test_tc_discount_002():
    """
    TEST CASE: TC-DISCOUNT-002 - Invalid discount code visual checks.
    """
    print("Starting test TC-DISCOUNT-002: Invalid Discount Code...")

    # Chrome options (do NOT run headless for debugging)
    chrome_options = Options()
    # chrome_options.add_argument("--headless=new")  # enable later if needed
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    # Initialize the webdriver with explicit Service
    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(PAGE_URL)
        driver.maximize_window()
        print(f"Navigated to {PAGE_URL}")

        wait = WebDriverWait(driver, 10)

        # Add Item A
        print("Adding Item A to cart...")
        add_item_a_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.add-to-cart-btn[data-item='A']"))
        )
        # use JS click if normal click sometimes doesn't trigger the page JS:
        try:
            add_item_a_button.click()
        except Exception:
            driver.execute_script("arguments[0].click();", add_item_a_button)
        time.sleep(0.8)

        # Verify a non-zero total
        total_price_element = wait.until(
            EC.visibility_of_element_located((By.ID, "total-price"))
        )
        initial_total_text = total_price_element.text.strip()
        print("Initial total cart value:", initial_total_text)

        # convert to numeric safely
        try:
            initial_total_value = float(initial_total_text.replace('$','').strip())
        except Exception:
            initial_total_value = 0.0

        assert initial_total_value > 0.0, f"Precondition failed: Cart total is not > $0.00. Found: {initial_total_text}"
        print("Precondition met: Cart contains items with total value > $0.00.")

        # Discount field visible
        discount_code_input = wait.until(EC.visibility_of_element_located((By.ID, "discount-code")))
        assert discount_code_input.is_displayed() and discount_code_input.is_enabled()

        # Enter invalid code and apply
        invalid_discount_code = "INVALIDCODE"
        print("Entering invalid discount code:", invalid_discount_code)
        discount_code_input.clear()
        discount_code_input.send_keys(invalid_discount_code)

        apply_button = wait.until(EC.element_to_be_clickable((By.ID, "apply-discount")))
        try:
            apply_button.click()
        except Exception:
            driver.execute_script("arguments[0].click();", apply_button)
        time.sleep(1.0)

        # Expect discount error visible with text
        discount_error_element = wait.until(EC.visibility_of_element_located((By.ID, "discount-error")))
        actual_error_text = discount_error_element.text.strip()
        print("Discount error text:", repr(actual_error_text))
        assert "Invalid" in actual_error_text or "invalid" in actual_error_text.lower(), \
            f"Expected an invalid-code message but found: {actual_error_text}"

        # Check that total did not change
        current_total_text = total_price_element.text.strip()
        assert current_total_text == initial_total_text, \
            f"Total changed after invalid coupon. Before: {initial_total_text}, After: {current_total_text}"
        print("Total unchanged after invalid coupon:", current_total_text)

        print("\nTest TC-DISCOUNT-002 PASSED!")

    except Exception as e:
        print("\nTest TC-DISCOUNT-002 FAILED:", e)
        # save screenshot for debugging
        try:
            driver.save_screenshot("TC-DISCOUNT-002_failure.png")
            print("Saved screenshot: TC-DISCOUNT-002_failure.png")
        except Exception:
            pass
    finally:
        driver.quit()
        print("WebDriver closed.")

if __name__ == "__main__":
    run_test_tc_discount_002()
