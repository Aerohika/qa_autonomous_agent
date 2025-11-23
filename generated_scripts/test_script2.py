
import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class TestDiscountCode(unittest.TestCase):

    def setUp(self):
        # Create a dummy HTML file for testing
        self.html_file_path = "checkout.html"
        self.create_html_file()

        # Initialize Chrome WebDriver
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(f"file:///{os.path.abspath(self.html_file_path)}")

        # Common wait object
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the browser
        self.driver.quit()
        # Remove the dummy HTML file
        if os.path.exists(self.html_file_path):
            os.remove(self.html_file_path)

    def create_html_file(self):
        html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>E-Shop Checkout</title>
    <style>
        .error { color: red; }
        body { font-family: sans-serif; margin: 20px; }
        .item { margin-bottom: 10px; }
        button { padding: 8px 14px; cursor: pointer; }
        #total-price { font-size: 20px; font-weight: bold; margin-top: 10px; }
    </style>
</head>

<body>

<h1>E-Shop Checkout</h1>

<!-- ITEMS -->
<div id="items">
    <div class="item">
        <span class="item-name">Item A</span>
        <button class="add-to-cart-btn" data-item="A">Add to Cart</button>
    </div>
    <div class="item">
        <span class="item-name">Item B</span>
        <button class="add-to-cart-btn" data-item="B">Add to Cart</button>
    </div>
</div>

<!-- CART SUMMARY -->
<h2>Cart Summary</h2>
<div id="cart-summary">
    <label>Item A Qty:</label>
    <input id="itemA-qty" type="number" value="0" readonly><br>

    <label>Item B Qty:</label>
    <input id="itemB-qty" type="number" value="0" readonly><br>

    <div id="total-price">$0.00</div>
</div>

<!-- DISCOUNT -->
<h2>Discount Code</h2>
<input id="discount-code" type="text" placeholder="Enter discount code">
<button id="apply-discount">Apply</button>
<div id="discount-error" class="error"></div>

<!-- USER DETAILS -->
<h2>User Details</h2>
<form id="checkout-form">
    <input id="name" type="text" placeholder="Name">
    <div id="name-error" class="error"></div>

    <input id="email" type="email" placeholder="Email">
    <div id="email-error" class="error"></div>

    <textarea id="address" placeholder="Address"></textarea>
    <div id="address-error" class="error"></div>

    <h3>Shipping Method</h3>
    <label><input type="radio" name="shipping" value="standard" checked> Standard</label>
    <label><input type="radio" name="shipping" value="express"> Express</label>

    <h3>Payment Method</h3>
    <label><input type="radio" name="payment" value="card" checked> Credit Card</label>
    <label><input type="radio" name="payment" value="paypal"> PayPal</label>

    <button id="pay-now" type="button">Pay Now</button>
    <div id="form-error" class="error"></div>
    <div id="success-message"></div>
</form>


<!-- SCRIPT -->
<script>
    let cart = {
        "Item A": { price: 100, qty: 0 },
        "Item B": { price: 50, qty: 0 }
    };

    const discountCodes = {
        "SAVE15": 0.15
    };

    function calculateRawTotal() {
        return (cart["Item A"].price * cart["Item A"].qty) +
               (cart["Item B"].price * cart["Item B"].qty);
    }

    function updateCartSummary(applyDiscount = false) {
        let total = calculateRawTotal();
        const code = document.getElementById("discount-code").value;
        const errDiv = document.getElementById("discount-error");

        // Apply discount
        if (applyDiscount) {
            if (discountCodes[code]) {
                total = total * (1 - discountCodes[code]);
                errDiv.textContent = "";
            } else if (code.trim() !== "") {
                errDiv.textContent = "Invalid discount code";
            }
        }

        // Update UI
        document.getElementById("itemA-qty").value = cart["Item A"].qty;
        document.getElementById("itemB-qty").value = cart["Item B"].qty;
        document.getElementById("total-price").textContent = "$" + total.toFixed(2);
    }

    // Add to cart listeners
    document.querySelectorAll(".add-to-cart-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            let item = btn.getAttribute("data-item");
            cart["Item " + item].qty++;
            updateCartSummary(false);
        });
    });

    // Apply discount logic
    document.getElementById("apply-discount").addEventListener("click", () => {
        updateCartSummary(true);
    });

    // Initial update
    updateCartSummary();
</script>

</body>
</html>
        """
        with open(self.html_file_path, "w") as f:
            f.write(html_content)

    def test_tc_discount_002_invalid_discount_code(self):
        # ID: TC-DISCOUNT-002
        # Test Case: Invalid discount code

        # Preconditions:
        # The cart contains "Item A" (quantity: 1) and "Item B" (quantity: 2).
        # Based on the provided HTML/JS, Item A price is 100, Item B price is 50.
        # Thus, the initial raw total cart value will be $200.00 (1*100 + 2*50).
        # (Note: The test case description mentions $30.00, which conflicts with the given HTML's JS prices.)

        # Add Item A (quantity: 1)
        item_a_add_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.add-to-cart-btn[data-item='A']"))
        )
        item_a_add_btn.click()

        # Add Item B (quantity: 2)
        item_b_add_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.add-to-cart-btn[data-item='B']"))
        )
        item_b_add_btn.click() # First Item B
        item_b_add_btn.click() # Second Item B

        # Verify the initial raw total cart value is $200.00
        total_price_element = self.wait.until(
            EC.visibility_of_element_located((By.ID, "total-price"))
        )
        self.assertEqual(total_price_element.text, "$200.00",
                         "Precondition failed: Initial total price is not $200.00 after adding items.")

        # Verify the discount code input field is empty
        discount_code_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "discount-code"))
        )
        self.assertEqual(discount_code_input.get_attribute("value"), "",
                         "Precondition failed: Discount code input field is not empty.")

        # Verify the discount error message area is empty
        discount_error_div = self.wait.until(
            EC.presence_of_element_located((By.ID, "discount-error"))
        )
        self.assertEqual(discount_error_div.text.strip(), "",
                         "Precondition failed: Discount error message area is not empty.")

        # Steps:
        # 1. Enter "INVALID10" into the "discount-code" input field.
        discount_code_input.send_keys("INVALID10")
        
        # 2. Click the "Apply" button.
        apply_discount_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "apply-discount"))
        )
        apply_discount_button.click()

        # Expected Result:
        # The total-price displayed should remain "$200.00".
        # (Adjusted from "$30.00" as per the actual HTML/JS behavior)
        self.wait.until(EC.text_to_be_present_in_element((By.ID, "total-price"), "$200.00"))
        self.assertEqual(total_price_element.text, "$200.00",
                         "Expected Result failed: Total price did not remain $200.00.")

        # The discount-error div should display the text "Invalid discount code".
        self.wait.until(EC.text_to_be_present_in_element((By.ID, "discount-error"), "Invalid discount code"))
        self.assertEqual(discount_error_div.text.strip(), "Invalid discount code",
                         "Expected Result failed: Discount error message is not 'Invalid discount code'.")

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
