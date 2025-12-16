from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import string

# Configuration
SHOP_URL = "https://localhost:8002/"
TIMEOUT = 10


# Generate random user data for registration
def generate_random_user():
    random_string = ''.join(random.choices(string.ascii_lowercase, k=8))
    return {
        'firstname': f'Test{random_string[:4]}',
        'lastname': f'User{random_string[4:]}',
        'email': f'test{random_string}@example.com',
        'password': f'TestPass123!{random_string[:4]}'
    }


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--start-maximized')

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(TIMEOUT)
    return driver


def wait_and_click(driver, by, value, timeout=TIMEOUT):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    element.click()
    return element


def wait_and_send_keys(driver, by, value, keys, timeout=TIMEOUT):
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )
    element.clear()
    element.send_keys(keys)
    return element


def add_products_to_cart(driver, num_products=10, num_categories=2):
    print(f"\n[1/10] Adding {num_products} products from {num_categories} categories...")

    products_added = 0
    categories_used = []

    try:
        categories = driver.find_elements(By.CSS_SELECTOR, "#top-menu > li > a")

        category_data = []
        for cat in categories:
            href = cat.get_attribute('href')
            text = cat.text
            if href and text:
                category_data.append({'url': href, 'name': text})

        if len(category_data) < num_categories:
            print(f"Warning: Found only {len(category_data)} categories")
            num_categories = len(category_data)

        # Select random categories
        selected_categories = random.sample(category_data, num_categories)
        products_per_category = num_products // num_categories

        for cat_data in selected_categories:
            category_name = cat_data['name']
            category_url = cat_data['url']
            print(f"  - Processing category: {category_name}")

            driver.get(category_url)
            time.sleep(2)

            products = driver.find_elements(By.CSS_SELECTOR, ".product-title a, h3.product-title a")
            product_links = [p.get_attribute('href') for p in products if p.get_attribute('href')]
            product_links = list(set(product_links))

            attempted = 0
            for product_url in product_links:
                if products_added >= num_products:
                    break
                if attempted >= products_per_category:
                    break

                try:
                    driver.get(product_url)
                    time.sleep(1.5)

                    quantity = random.randint(1, 3)
                    try:
                        qty_input = driver.find_element(By.CSS_SELECTOR, "#quantity_wanted")
                        qty_input.click()
                        qty_input.send_keys(Keys.CONTROL + "a")
                        qty_input.send_keys(Keys.BACKSPACE)
                        qty_input.send_keys(str(quantity))
                        time.sleep(1.5)
                    except:
                        print(f"    Could not set quantity, using default")

                    quantity_to_try = quantity
                    quantity_final = 0

                    while True:

                        if quantity_to_try <= 0:
                            print("    ! Nie udało się dodać produktu, minimalna ilość (0) osiągnięta.")
                            raise NoSuchElementException("Stock is zero, moving to next product.")

                        try:
                            add_to_cart = driver.find_element(By.CSS_SELECTOR,
                                                              ".add-to-cart, button[data-button-action='add-to-cart']")
                            qty_input = driver.find_element(By.CSS_SELECTOR, "#quantity_wanted")
                        except NoSuchElementException:
                            print("    ! Krytyczny element zniknął (może stock = 0). Pomiń.")
                            raise NoSuchElementException("Cannot find product elements.")

                        if add_to_cart.is_enabled():
                            quantity_final = quantity_to_try
                            print(f"    ✓ Przycisk jest aktywny dla ilości: {quantity_final}")
                            break

                        quantity_to_try -= 1
                        print(f"    Przycisk DISABLED. Zmniejszam ilość do: {quantity_to_try}")

                        try:
                            qty_input.click()
                            qty_input.send_keys(Keys.CONTROL + "a")
                            qty_input.send_keys(Keys.BACKSPACE)
                            qty_input.send_keys(str(quantity_to_try))
                            time.sleep(1.5)

                        except Exception as e:
                            print(f"    Wystąpił błąd wprowadzania ilości (Stale Element). Kontynuuję pętlę...")
                            pass

                    try:
                        final_add_to_cart = driver.find_element(By.CSS_SELECTOR,
                                                                ".add-to-cart, button[data-button-action='add-to-cart']")
                        driver.execute_script("arguments[0].click();", final_add_to_cart)
                        time.sleep(1.0)
                        MODAL_CONTAINER_SELECTOR = "#blockcart-modal .modal-content, .modal.fade.in, #_desktop_cart.modal"
                        CLOSE_BUTTON_SELECTOR = ".close, .modal-close, button.close"

                        try:
                            modal_container = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, MODAL_CONTAINER_SELECTOR))
                            )

                            close_modal_button = modal_container.find_element(By.CSS_SELECTOR, CLOSE_BUTTON_SELECTOR)

                            driver.execute_script("arguments[0].click();", close_modal_button)

                            time.sleep(1.0)  # Krótka pauza na zniknięcie modala

                            print("    Modal koszyka pomyślnie zamknięty.")

                        except TimeoutException:
                            print("    Warning: Kontener modala nie pojawił się w oczekiwanym czasie, kontynuuję.")
                        except Exception as e:
                            print(f"    Warning: Błąd przy zamykaniu modala. Kontynuuję. {str(e)[:50]}")

                    except Exception as e:
                        print(f"    Błąd przy klikaniu finalnego Add to Cart: {e}")
                        raise

                    products_added += 1
                    attempted += 1
                    print(f"    Added product {products_added}/{num_products} (qty: {quantity})")

                except Exception as e:
                    error_message = str(e)

                    if "Stock is zero, moving to next product" in error_message or "Cannot find product elements" in error_message:
                        print(f"    Failed to add product (Stock zero, skipping): {error_message[:100]}")
                    else:
                        print(f"    Failed to add product (General error): {error_message[:100]}")
                        attempted += 1
                        continue

            categories_used.append(category_name)

    except Exception as e:
        print(f"Error adding products: {e}")
        import traceback
        traceback.print_exc()

    print(f"    Successfully added {products_added} products from categories: {', '.join(categories_used)}")
    return products_added


def search_and_add_product(driver):

    # Step 2: Search for a product and add random one from results (adding 1 item).

    print("\n[2/10] Searching for product and adding random one...")

    try:

        search_terms = ['piłka', 'torby', 'kosz', 'zestaw', 'siatkówka']
        search_term = random.choice(search_terms)

        search_input = driver.find_element(By.CSS_SELECTOR, "input[name='s'], .search-input, #search_query_top")
        search_input.clear()
        search_input.send_keys(search_term)
        search_input.send_keys(Keys.RETURN)
        time.sleep(2)

        products = driver.find_elements(By.CSS_SELECTOR, ".product-miniature a, .product-title a")
        product_links = [p.get_attribute('href') for p in products if p.get_attribute('href')]

        if not product_links:
            print("  ! No search results found")
            return

        search_candidates = product_links[:]
        random.shuffle(search_candidates)

        product_added_success = False

        for product_url in search_candidates:
            if product_added_success:
                break

            try:

                driver.get(product_url)
                time.sleep(1.5)

                add_to_cart = driver.find_element(By.CSS_SELECTOR,
                                                  ".add-to-cart, button[data-button-action='add-to-cart']")

                if add_to_cart.is_enabled():

                    driver.execute_script("arguments[0].click();", add_to_cart)
                    time.sleep(2)

                    MODAL_CONTAINER_SELECTOR = "#blockcart-modal .modal-content, .modal.fade.in, #_desktop_cart.modal"
                    CLOSE_BUTTON_SELECTOR = ".close, .modal-close, button.close"

                    try:
                        modal_container = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, MODAL_CONTAINER_SELECTOR))
                        )

                        close_modal_button = modal_container.find_element(By.CSS_SELECTOR, CLOSE_BUTTON_SELECTOR)

                        driver.execute_script("arguments[0].click();", close_modal_button)

                        time.sleep(1.0)

                        print("    Modal koszyka pomyślnie zamknięty.")

                    except TimeoutException:
                        print("    Warning: Kontener modala nie pojawił się w oczekiwanym czasie, kontynuuję.")
                    except Exception as e:
                        print(f"    Warning: Błąd przy zamykaniu modala. Kontynuuję. {str(e)[:50]}")

                    print(f" Added 1 item from search results for '{search_term}'")
                    product_added_success = True

                else:
                    print(f"    ! Product is not available (Stan 0). Trying another...")
                    continue

            except Exception as e:
                print(f"    ! Error adding a product: {str(e)[:100]}. Trying another...")
                continue

        if not product_added_success:
            print(f"  ! No available product found among the top candidates for '{search_term}'")

    except Exception as e:
        print(f"Error in search: {e}")


def remove_products_from_cart(driver, num_to_remove=3):
    # Step 3: Remove 3 products from cart

    print(f"\n[3/10] Removing {num_to_remove} products from cart...")

    try:
        driver.get(f"{SHOP_URL}/index.php?controller=cart")
        time.sleep(2)

        removed = 0
        for i in range(num_to_remove):
            try:
                remove_buttons = driver.find_elements(By.CSS_SELECTOR,
                                                      ".remove-from-cart, .cart-item-delete, a.remove-from-cart")

                if remove_buttons:
                    driver.execute_script("arguments[0].click();", remove_buttons[0])
                    time.sleep(1.5)
                    removed += 1
                    print(f"  - Removed product {removed}/{num_to_remove}")
                else:
                    print(f"  ! No more products to remove")
                    break
            except Exception as e:
                print(f"  ! Could not remove product: {e}")
                break

        print(f"Removed {removed} products from cart")

    except Exception as e:
        print(f"Error removing products: {e}")


def register_new_account(driver, user_data):
    # Step 4: Register new user account

    print("\n[4/10] Registering new account...")

    try:
        driver.get(f"{SHOP_URL}logowanie?create_account")
        time.sleep(2)

        wait_and_send_keys(driver, By.CSS_SELECTOR, "input[name='firstname']", user_data['firstname'])
        time.sleep(1.0)
        wait_and_send_keys(driver, By.CSS_SELECTOR, "input[name='lastname']", user_data['lastname'])
        time.sleep(1.0)
        wait_and_send_keys(driver, By.CSS_SELECTOR, "input[name='email']", user_data['email'])
        time.sleep(1.0)
        wait_and_send_keys(driver, By.CSS_SELECTOR, "input[name='password']", user_data['password'])
        time.sleep(1.0)

        try:
            terms_checkbox = driver.find_element(By.CSS_SELECTOR,
                                                 "input[name='psgdpr']")
            if not terms_checkbox.is_selected():
                terms_checkbox.click()
        except:
            pass

        try:
            customer_privacy = driver.find_element(By.CSS_SELECTOR, "input[name='customer_privacy']")
            if not customer_privacy.is_selected():
                customer_privacy.click()
        except:
            pass

        wait_and_click(driver, By.CSS_SELECTOR,
                       "button[data-action='save-customer'], .form-footer button[type='submit']")
        time.sleep(3)

        print(f"Registered user: {user_data['email']}")

    except Exception as e:
        print(f"Error during registration: {e}")
        pass


def proceed_to_checkout(driver):
    # Step 5: Proceed to checkout

    print("\n[5/10] Proceeding to checkout...")

    try:
        driver.get(f"{SHOP_URL}zamówienie")
        time.sleep(2)
        print("Navigated to checkout")
    except Exception as e:
        print(f"Error navigating to checkout: {e}")


def fill_address_and_continue(driver, user_data):
    # Fill address information

    try:
        address_field = driver.find_elements(By.CSS_SELECTOR, "input[name='address1']")

        if address_field:
            print("  - Filling address information...")
            wait_and_send_keys(driver, By.CSS_SELECTOR, "input[name='address1']", "Test Street 123")
            time.sleep(1.0)
            wait_and_send_keys(driver, By.CSS_SELECTOR, "input[name='postcode']", "80-489")
            time.sleep(1.0)
            wait_and_send_keys(driver, By.CSS_SELECTOR, "input[name='city']", "Warsaw")
            time.sleep(1.0)

            continue_btn = driver.find_element(By.CSS_SELECTOR, "button[name='confirm-addresses']")
            continue_btn.click()
            time.sleep(2)
    except:
        pass


def select_carrier(driver):
    # Step 6-7: Select one of two carriers

    print("\n[6/10] Selecting carrier...")

    try:
        carriers = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "input[name='delivery_option'], .delivery-option input"))
        )

        if len(carriers) >= 3:
            selected_carrier = random.choice(carriers[:3])
            driver.execute_script("arguments[0].click();", selected_carrier)
            time.sleep(2.0)
            print("Selected carrier")
        else:
            if carriers:
                carriers[0].click()
                time.sleep(2.0)
                print("Selected available carrier")

        try:
            continue_btn = driver.find_element(By.CSS_SELECTOR, "button[name='confirmDeliveryOption']")
            continue_btn.click()
            time.sleep(2)
        except:
            pass

    except Exception as e:
        print(f"Error selecting carrier: {e}")


def select_payment_on_delivery(driver):
    # Step 7: Select payment on delivery (cash on delivery)

    print("\n[7/10] Selecting payment method: Cash on Delivery...")

    try:

        cod_payment = driver.find_element(By.CSS_SELECTOR, "input[data-module-name='ps_cashondelivery']")

        if cod_payment.is_selected():
            print("Cash on Delivery was already selected.")
            return

        driver.execute_script("arguments[0].click();", cod_payment)
        time.sleep(1)
        print(f"Selected Cash on Delivery ")

    except Exception as e:
        print(f"Error selecting payment: {e}")


def accept_terms_and_confirm_order(driver):
    # Step 8: Accept final terms and click 'Place Order' (Confirm Order).

    print("\n[8/10] Confirming order (Accepting terms and placing order)...")

    FINAL_TERMS_CHECKBOX_SELECTOR = "input[name*='conditions_to_approve'], #conditions-to-approve input"

    CONFIRM_BUTTON_SELECTOR = "button.btn-primary.center-block[type='submit']"

    try:
        print("  -> Searching for final terms checkbox...")

        terms_checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, FINAL_TERMS_CHECKBOX_SELECTOR))
        )

        if terms_checkbox.is_enabled() and not terms_checkbox.is_selected():
            driver.execute_script("arguments[0].click();", terms_checkbox)
            print("Final terms checkbox selected.")
        elif terms_checkbox.is_selected():
            print("Final terms checkbox was already selected.")

        time.sleep(1)

        confirm_btn = driver.find_element(By.CSS_SELECTOR, CONFIRM_BUTTON_SELECTOR)

        driver.execute_script("arguments[0].click();", confirm_btn)
        print("'ZŁÓŻ ZAMÓWIENIE' button clicked.")
        time.sleep(5)

    except Exception as e:
        print(f"  ! FATAL ERROR during order placement: {e}")


def check_order_status(driver):
    # Step 9: Check order status in order history

    print("\n[9/10] Checking order status...")

    try:
        # Go to order history
        driver.get(f"{SHOP_URL}historia-zamowien")
        time.sleep(2)

        # Find latest order
        orders = driver.find_elements(By.CSS_SELECTOR, ".order-item, tbody tr")

        if orders:
            status = driver.find_element(By.CSS_SELECTOR, ".order-status, .label")
            print(f"  ✓ Order status: {status.text}")
            return True
        else:
            print("  ! No orders found")
            return False

    except Exception as e:
        print(f"Error checking order status: {e}")
        return False


def download_invoice(driver):
    # Step 10: Download VAT invoice
    print("\n[10/10] Downloading VAT invoice...")

    try:
        invoice_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='invoice'], .pdf-invoice")
        if invoice_links:
            invoice_url = invoice_links[0].get_attribute('href')
            print(f"  ✓ Invoice download link found: {invoice_url}")
            invoice_links[0].click()
            time.sleep(2)
            print("  ✓ Invoice download initiated")
            return True
        else:
            print("  ! Invoice not yet available (order might need processing)")
            return False

    except Exception as e:
        print(f"Error downloading invoice: {e}")
        return False


def main():
    print("=" * 60)
    print("PrestaShop 1.7.8 Automated Test Script")
    print("=" * 60)

    driver = None
    start_time = time.time()

    try:
        # Initialize driver
        driver = init_driver()
        driver.get(SHOP_URL)
        time.sleep(2)

        # Generate user data
        user_data = generate_random_user()

        # Execute test steps
        add_products_to_cart(driver, num_products=10, num_categories=2)
        search_and_add_product(driver)
        remove_products_from_cart(driver, num_to_remove=3)
        register_new_account(driver, user_data)
        proceed_to_checkout(driver)
        fill_address_and_continue(driver, user_data)
        select_carrier(driver)
        select_payment_on_delivery(driver)
        accept_terms_and_confirm_order(driver)
        check_order_status(driver)
        download_invoice(driver)

        # Calculate execution time
        execution_time = time.time() - start_time

        print("\n" + "=" * 60)
        print(f" Test completed successfully in {execution_time:.2f} seconds")
        print("=" * 60)
    except Exception as e:
        print(f"\n Test failed with error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if driver:
            print("\nClosing browser in 5 seconds...")
            time.sleep(5)
            driver.quit()


if __name__ == "__main__":
    main()
