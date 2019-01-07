from django.db import models


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateField(null=False)
    order_title = models.CharField(max_length=100)
    order_description = models.CharField(max_length=300)
    order_price = models.DecimalField(default=0.00, max_digits=5, decimal_places=2)
