import logging
from decimal import Decimal
from typing import List, Tuple, Dict

import requests
from django.core.mail import EmailMessage
from django.db.models import Max, ObjectDoesNotExist
from django.db.models.functions import Coalesce
from django.template.loader import get_template
from django.utils import timezone

from alerts.models import Product, Price, ProductAlert
from shore.settings import EBAY_APP_ID, EBAY_BASE_URL, EMAIL_HOST_USER

from server.shore.settings import PRODUCT_PRICE_CHANGE_DAYS

logger = logging.getLogger(__name__)


def sanitize_product_data(ebay_item: dict) -> Tuple[dict, float]:
    """
    Sanitize ebay item

    :param ebay_item: dict
    :return: tuple of product data and price
    """
    product_data = {
        'ebay_id': ebay_item['itemId'][0],
        'title': ebay_item["title"][0],
        'image_url': ebay_item["viewItemURL"][0],
        "location": ebay_item["location"][0]
    }
    price: float = ebay_item["sellingStatus"][0]["currentPrice"][
        0]["__value__"]

    return product_data, price


def get_ebay_product(search_phrase: str,
                     sorted_by: str = 'price', limit: int = 20) -> List[dict]:
    """
    Fetch product data from ebay for given search phrase
    :param search_phrase: product search phrase
    :param sorted_by: product sorted by lowest price
    :param limit: product limit
    :return: list of ebay product item
    """
    ebay_url = EBAY_BASE_URL.format(EBAY_APP_ID, search_phrase, sorted_by,
                                    limit)
    response = requests.get(ebay_url)
    response = response.json()

    product_data = []
    if response["findItemsByKeywordsResponse"][0]["ack"][0] == 'Success':
        product_data = response["findItemsByKeywordsResponse"][0][
            "searchResult"][0]["item"]
    else:
        logger.error("Error: {} in fetching product for :{}".format(
            response["errorMessage"], search_phrase))

    return product_data


def save_ebay_product(alert_id: int) -> List[Product]:
    """
    Save product data fetch by search phrase from ebay to db
    :param alert_id: product alert id
    :return: product queryset
    """
    alert = ProductAlert.objects.get(id=alert_id)
    ebay_items = get_ebay_product(alert.search_phrase)
    sanitized_data = [sanitize_product_data(item) for item in ebay_items]
    products = []
    for product_data, price in sanitized_data:
        product, _ = Product.objects.get_or_create(
            ebay_id=product_data['ebay_id'],
            alert=alert,
            defaults=product_data
        )

        try:
            # get last price
            last_price = product.price_set.latest('timestamp')
            print("last price: ", last_price)
        except ObjectDoesNotExist:
            print("Does not exist.")
            _ = Price.objects.create(price=price, product=product)
        else:
            print("exist")
            if last_price.price != Decimal(price).quantize(Decimal('.01')):
                print(" exist , diff, creating")
                # create price, if there is some change inn price
                _ = Price.objects.create(price=price, product=product)
            else:
                print("no diff")
        products.append(product)

    # sort by price, as it'll be mostly 20 products , this should be fine
    products = sorted(products, key=lambda p: float(p.price))

    return products


def send_alert_notification(subject: str, alert: ProductAlert,
                            products: List[Product],
                            template: str) -> int:
    """
    Send email to user for product alert.
    :param template: email template file path
    :param alert: Product alert instance
    :param subject: Email subject
    :param products: Product queryset
    :return: no of email sent
    """
    message = get_template(template).render({
        'products': products,
        'alert': alert
    })
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=EMAIL_HOST_USER,
        to=[alert.email],
    )
    mail.content_subtype = "html"
    return mail.send()


def get_product_price_change_report(alert: ProductAlert
                                    ) -> Dict[str, List[Product]]:
    now = timezone.now()
    from_date = now - timezone.timedelta(days=int(PRODUCT_PRICE_CHANGE_DAYS))
    report = {
        'decreased_2_per': [],
        'decreased': [],
        'no_change': []
    }
    products = Product.objects.filter(alert=alert)
    for product in products:
        last_max_price = product.price_set.filter(
            timestamp__date=from_date.date(),
        ).aggregate(
            max_price=Coalesce(Max('price'), Decimal('0.0'))
        )['max_price']
        current_price = product.price
        if current_price < last_max_price:
            decrease = last_max_price - current_price
            decrease_perc = (decrease / last_max_price) * Decimal('100.00')
            if decrease_perc >= 2:
                report['decreased_2_per'].append(product)
            else:
                report['decreased'].append(product)
        elif current_price == last_max_price:
            report['no_change'].append(product)
    return report


def serialize_reports(report: dict) -> dict:
    ser = {}
    for report, products in report.items():
        ser[report] = [p.dict() for p in products]
    ser['timestamp'] = timezone.now().isoformat()
    return ser
