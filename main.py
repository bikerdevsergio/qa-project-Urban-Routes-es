import data
import pytest
from selenium import webdriver

from pages import UrbanRoutesPage


@pytest.fixture
def driver():
    # necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
    chrome_options = webdriver.ChromeOptions()
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    drv = webdriver.Chrome(options=chrome_options)
    drv.get(data.urban_routes_url)
    yield drv
    drv.quit()


def prepare_comfort_order(routes_page):
    """Precondición común: dirección establecida y tarifa Comfort seleccionada."""
    routes_page.set_route(data.address_from, data.address_to)
    routes_page.click_order_taxi_button()
    routes_page.select_comfort_tariff()


def prepare_phone_and_card(routes_page):
    """Precondición para las pruebas que necesitan poder enviar el pedido."""
    prepare_comfort_order(routes_page)
    routes_page.fill_phone_number(data.phone_number)
    routes_page.add_credit_card(data.card_number, data.card_code)


class TestUrbanRoutes:

    def test_set_route(self, driver):
        routes_page = UrbanRoutesPage(driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort_tariff(self, driver):
        routes_page = UrbanRoutesPage(driver)
        prepare_comfort_order(routes_page)
        assert routes_page.is_comfort_tariff_selected()

    def test_fill_phone_number(self, driver):
        routes_page = UrbanRoutesPage(driver)
        prepare_comfort_order(routes_page)
        routes_page.fill_phone_number(data.phone_number)
        assert routes_page.get_phone_number() == data.phone_number

    def test_fill_card(self, driver):
        routes_page = UrbanRoutesPage(driver)
        prepare_comfort_order(routes_page)
        routes_page.fill_phone_number(data.phone_number)
        routes_page.add_credit_card(data.card_number, data.card_code)
        assert routes_page.get_linked_card_value() != ''

    def test_comment_for_driver(self, driver):
        routes_page = UrbanRoutesPage(driver)
        prepare_comfort_order(routes_page)
        routes_page.write_message_for_driver(data.message_for_driver)
        assert routes_page.get_message_for_driver() == data.message_for_driver

    def test_order_blanket_and_tissues(self, driver):
        routes_page = UrbanRoutesPage(driver)
        prepare_comfort_order(routes_page)
        routes_page.order_blanket_and_tissues()
        assert routes_page.is_blanket_and_tissues_ordered()

    def test_order_two_ice_creams(self, driver):
        routes_page = UrbanRoutesPage(driver)
        prepare_comfort_order(routes_page)
        routes_page.order_ice_creams(2)
        assert routes_page.get_ice_cream_count() == 2

    def test_car_search_model(self, driver):
        routes_page = UrbanRoutesPage(driver)
        prepare_phone_and_card(routes_page)
        routes_page.submit_order()
        assert routes_page.is_taxi_search_modal_visible()

    def test_driver_info(self, driver):
        routes_page = UrbanRoutesPage(driver)
        prepare_phone_and_card(routes_page)
        routes_page.submit_order()
        assert routes_page.wait_for_driver_info()
