from django.db import models

from django.contrib.auth import get_user_model
from products.models import Product


User = get_user_model()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} of {self.item.name}'

    # total of each type of item
    def get_total(self):
        if self.item.on_sale:
            total = self.item.sale_price * self.quantity
        else:
            total =  self.item.price * self.quantity
        floattotal = float("{0:.2f}".format(total))
        return floattotal


class Order(models.Model):
    orderitems  = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order by- {self.user.username} id: {self.pk}'

    # order total
    def get_totals(self):
        total = 0
        for order_item in self.orderitems.all():
            total += order_item.get_total()

        return total
