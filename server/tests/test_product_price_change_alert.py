import json
import os
from shore.settings import BASE_DIR
from unittest import mock

from django.test import TestCase

from alerts.models import ProductAlert
from alerts.utils import sanitize_product_data, save_ebay_product

test_dir = os.path.join(BASE_DIR, 'tests')


def mock_ebay_response():
    file_path = os.path.join(test_dir, 'ebay_response.json')
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data


class TestProductPriceChangeAlert(TestCase):
    def setUp(self):
        # Setup run before every test method.

        # Save data in test database
        # Sample product for no price changes
        self.ebay_response = mock_ebay_response()
        self.product_alert = ProductAlert.objects.create(search_phrase="mobile",
                                                         email="abc@gmail.com",
                                                         time_interval=2)

    @mock.patch('alerts.utils.get_ebay_product')
    def test_save_product_data(self, mock_get_ebay_product):
        mock_get_ebay_product.return_value = self.ebay_response
        products = save_ebay_product(self.product_alert.id)
        self.assertEqual(len(products), 20, 'Product got saved in db')
        self.assertEqual(products[0].alert_id, self.product_alert.id,
                         'Product got saved for created alert')

    def test_sanitize_product_data(self):
        response = sanitize_product_data(self.ebay_response[0])
        self.assertEqual(type(response), tuple,
                         "Response from sanitized data is product data"
                         " and price")
        self.assertEqual(response[0]['ebay_id'], self.ebay_response[0]
        ["itemId"][0], "Ebay item id is transformed as ebay_id in response"
                         )
        self.assertEqual(response[0]['image_url'], self.ebay_response[0]
        ["viewItemURL"][0], "Ebay image url")
        self.assertEqual(response[1], self.ebay_response[0]
        ["sellingStatus"][0]["currentPrice"][0]["__value__"],
                         "Ebay product price")



