import time
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from helpers import retrieve_phone_code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    order_taxi_button = (By.XPATH, "//button[contains(., 'Pedir un taxi')]")
    tariff_card = (By.CLASS_NAME, 'tcard')

    phone_number_field_trigger = (By.CLASS_NAME, 'np-button')
    phone_field = (By.ID, 'phone')
    next_button = (By.XPATH, "//button[contains(., 'Siguiente')]")
    code_field = (By.ID, 'code')
    confirm_button = (By.XPATH, "//button[contains(., 'Confirmar')]")

    payment_method_trigger = (By.CLASS_NAME, 'pp-button')
    add_card_button = (By.CSS_SELECTOR, '.payment-picker.open .pp-selector .pp-row.disabled .pp-title')
    card_number_field = (By.ID, 'number')
    card_code_field = (By.CSS_SELECTOR, 'input.card-input#code')
    link_card_button = (By.CSS_SELECTOR, '.payment-picker .modal .section.active .pp-buttons > button')
    card_close_button = (By.CSS_SELECTOR, '.payment-picker .modal .section.active .close-button')
    linked_card_value = (By.CLASS_NAME, 'pp-value-text')

    message_field = (By.ID, 'comment')

    blanket_and_tissues_switch = (By.CLASS_NAME, 'switch')
    blanket_and_tissues_checkbox = (By.CLASS_NAME, 'switch-input')

    ice_cream_plus_button = (By.CLASS_NAME, 'counter-plus')
    ice_cream_counter_value = (By.CLASS_NAME, 'counter-value')

    submit_order_button = (By.CSS_SELECTOR, '.smart-button-wrapper button')
    taxi_search_modal = (By.CSS_SELECTOR, '.order-body')
    driver_arrival_info = (By.XPATH, "//div[contains(., 'El conductor llegará')]")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def set_from(self, from_address):
        from_input = self.wait.until(expected_conditions.presence_of_element_located(self.from_field))
        from_input.send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def click_order_taxi_button(self):
        self.wait.until(expected_conditions.element_to_be_clickable(self.order_taxi_button)).click()

    def select_comfort_tariff(self):
        tariffs = self.wait.until(
            expected_conditions.presence_of_all_elements_located(self.tariff_card))
        for tariff in tariffs:
            if 'Comfort' in tariff.text:
                tariff.click()
                return
        raise Exception("No se encontró la tarifa 'Comfort'")

    def is_comfort_tariff_selected(self):
        tariffs = self.driver.find_elements(*self.tariff_card)
        for tariff in tariffs:
            if 'Comfort' in tariff.text:
                return 'active' in tariff.get_attribute('class')
        return False

    def fill_phone_number(self, phone_number):
        self.wait.until(expected_conditions.element_to_be_clickable(self.phone_number_field_trigger)).click()
        phone_input = self.wait.until(expected_conditions.visibility_of_element_located(self.phone_field))
        phone_input.send_keys(phone_number)
        self.driver.find_element(*self.next_button).click()
        # da tiempo a que la petición del código de confirmación se complete y quede
        # registrada en los logs de rendimiento antes de leerla
        time.sleep(3)
        code = retrieve_phone_code(self.driver)
        code_input = self.wait.until(expected_conditions.visibility_of_element_located(self.code_field))
        code_input.send_keys(code)
        self.driver.find_element(*self.confirm_button).click()

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_field).get_property('value')

    def add_credit_card(self, card_number, card_code):
        self.wait.until(expected_conditions.element_to_be_clickable(self.payment_method_trigger)).click()
        self.wait.until(expected_conditions.element_to_be_clickable(self.add_card_button)).click()
        self.wait.until(expected_conditions.visibility_of_element_located(self.card_number_field)).send_keys(card_number)
        code_input = self.wait.until(expected_conditions.visibility_of_element_located(self.card_code_field))
        code_input.send_keys(card_code)
        # el botón 'link' permanece deshabilitado hasta que el campo CVV pierde el foco
        code_input.send_keys(Keys.TAB)
        self.wait.until(expected_conditions.element_to_be_clickable(self.link_card_button)).click()
        self.wait.until(expected_conditions.visibility_of_element_located(self.card_close_button)).click()

    def get_linked_card_value(self):
        return self.driver.find_element(*self.linked_card_value).text

    def write_message_for_driver(self, message):
        message_input = self.driver.find_element(*self.message_field)
        message_input.send_keys(message)

    def get_message_for_driver(self):
        return self.driver.find_element(*self.message_field).get_property('value')

    def order_blanket_and_tissues(self):
        self.wait.until(expected_conditions.element_to_be_clickable(self.blanket_and_tissues_switch)).click()

    def is_blanket_and_tissues_ordered(self):
        return self.driver.find_element(*self.blanket_and_tissues_checkbox).is_selected()

    def order_ice_creams(self, quantity=2):
        button = self.wait.until(expected_conditions.element_to_be_clickable(self.ice_cream_plus_button))
        for _ in range(quantity):
            button.click()

    def get_ice_cream_count(self):
        return int(self.driver.find_element(*self.ice_cream_counter_value).text)

    def submit_order(self):
        self.wait.until(expected_conditions.element_to_be_clickable(self.submit_order_button)).click()

    def is_taxi_search_modal_visible(self):
        return self.wait.until(expected_conditions.visibility_of_element_located(self.taxi_search_modal)).is_displayed()

    def wait_for_driver_info(self, timeout=90):
        return WebDriverWait(self.driver, timeout).until(
            expected_conditions.visibility_of_element_located(self.driver_arrival_info)).is_displayed()
