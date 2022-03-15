import uuid
from django.db import models
from django.contrib.auth.models import User
# 3/15/2022: Unfinished work = determining Product price, storing payment info


class Customer(models.Model):
    # We only have to add our extra variables here
    cust_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    delivery_info = models.OneToOneField('Delivery', null=True, on_delete=models.CASCADE)


class Delivery(models.Model):
    # Look at django Address Class, we may be able to get rid of this whole Class
    delivery_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                   help_text='Unique ID for this specific order-delivery information')
    user = models.ForeignKey('Delivery', on_delete=models.RESTRICT, null=False)
    street_address = models.CharField(max_length=250, null=False)
    street_address2 = models.CharField(max_length=250, null=True, blank=True, help_text='Apt number, building, etc.')
    # Note that for this project, our store will only be in Omaha, so these fields could be eliminated theoretically
    city = models.CharField(max_length=30, null=False)
    state = models.CharField(max_length=30, null=False)
    zipCode = models.CharField(max_length=5, null=False)


# NOT FINISHED
class Payment(models.Model):
    # Look at django Address Class, they have a whole form for payment information
    pay_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                              help_text='Unique ID for User Billing Info')


class Coupon(models.Model):
    coupon_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                 help_text='Unique ID for given Coupon and its discount')
    totalDiscount = models.DecimalField(blank=True, default=0.0)


class Product(models.Model):
    # Pizza is our only Product for the store and comes in two types: Whole Pizzas and Slices
    # PRODUCT_TYPES is a dictionary that shows both the type and its related base price
    # Base-price assumes only Cheese Topping
    # There is also only one type of crust if you were curious
    PRODUCT_TYPES = {
        'Slice': 3,
        'Whole Pie': 14
    }
    # PRODUCT_PIZZA_NAMES shows all possible flavors of Pizza as well as their number of toppings
    # Toppings determine price (i.e. more toppings = more expensive)
    PRODUCT_PIZZA_NAMES = {
        'Cheese': 0,
        'Pepperoni': 1,
        'Beef': 1,
        'Italian Sausage': 1,
        'Canadian Bacon': 1,
        'Chicken Alfredo': 2,
        'Supreme': 5,
        'Meat Lovers': 5,
        'Philly': 4,
        'BBQ Chicken': 3
    }
    # PRODUCT_SAUCES is a list of all possible sauces for a pizza
    # Sauce does NOT affect price
    PRODUCT_SAUCES = ['Classic Marinara', 'Garlic Parm', 'Buffalo', 'BBQ', 'None']
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for a Product')
    type = models.CharField(max_length=10, choices=PRODUCT_TYPES.keys(), blank=False, default='Whole Pie')
    name = models.CharField(max_length=20, choices=PRODUCT_PIZZA_NAMES.keys(), blank=False, default='Cheese')
    toppings = models.ManyToManyField('Toppings', blank=True)
    coupon = models.ManyToManyField('Coupon', blank=True)
    sauce = models.CharField(max_length=16, choices=PRODUCT_SAUCES, blank=False, default='Classic Marinara')
    price = models.DecimalField(blank=False, default=PRODUCT_TYPES['Slice'])

    def determine_price(self):
        pass


class Toppings(models.Model):
    # PRODUCT_TOPPINGS shows all possible toppings for a pizza
    # Each added topping adds 0.30 to slice or 0.65 to whole pizza
    # None indicates a pizza with only Cheese
    # If blank, then default goes to 'None'
    PRODUCT_TOPPINGS = ['Pepperoni', 'Beef', 'Italian Sausage', 'Canadian Bacon', 'Bacon', 'Chicken', 'Green Pepper',
                        'Jalapeno', 'Onion', 'Banana Pepper', 'Black Olive', 'None']
    name = models.CharField(max_length=15, choices=PRODUCT_TOPPINGS, null=False, blank=True, default='None')
