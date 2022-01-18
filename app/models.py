from django.db import models

# Create your models here.from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

# Create your models here.

STATE_CHOICES = (('Gujarat','Gujarat'),('Maharashtra','Maharashtra'),('Uttar Pradesh','Uttar Pradesh'))

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=50)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES = (('D','Drawing'),('P','Painting'))

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField(max_length=50)
    discounted_price = models.FloatField(max_length=50)
    description = models.TextField()
    artist = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    product_img = models.ImageField(upload_to='media')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

        

STATUS_CHOICES = (('Accepted','Accepted'),
                    ('Packed','Packed'),
                    ('On The Way','On The Way'),
                    ('Delivered','Delivered'),
                    ('Cancel','Cancel'))

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class ContactUs(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name 
