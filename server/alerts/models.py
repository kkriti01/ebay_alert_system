from decimal import Decimal

from django.db import models


class ProductAlert(models.Model):
    """
    Store user's alert settings
    """
    INTERVAL_CHOICE = (
        (2, '2 minutes'),
        (10, '10 minutes'),
        (30, '30 minutes')
    )
    search_phrase = models.CharField(max_length=225, db_index=True)
    time_interval = models.IntegerField(choices=INTERVAL_CHOICE)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('email', 'search_phrase')

    def __str__(self):
        return self.search_phrase


class Update(models.Model):
    """
    Log of update sent to a user

    this is also being used to check next update
    """
    alert = models.ForeignKey(ProductAlert, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.alert.search_phrase}: {self.timestamp.ctime()}'


class Product(models.Model):
    """
    Stores product data. product price are stored in different Model (table)
    """
    alert = models.ForeignKey(ProductAlert, on_delete=models.CASCADE)
    ebay_id = models.CharField(max_length=100, db_index=True)
    title = models.CharField(max_length=225)
    location = models.TextField()
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('alert', 'ebay_id')

    def __str__(self):
        return self.title

    @property
    def price(self) -> Decimal:
        """
        :return: last checked price of the product
        """
        return self.price_set.latest('timestamp').price

    def dict(self):
        """
        Return json serializable dict
        :return:
        """
        return {
            'id': str(self.id),
            'ebay_id': self.ebay_id,
            'title': self.title,
            'price': self.price
        }


class Price(models.Model):
    """
    Store product price
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.title}: {self.price}'
























































