from django.db import models
from django.conf import settings

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    slug = models.SlugField()
    
    def __str__(self):
        return self.title
    
class Brand(models.Model):
    brand_name = models.CharField(max_length=200)
    slug = models.SlugField()
    
    def __str__(self):
        return self.brand_name
    
class Item(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to="product/")
    price = models.FloatField()
    discount_price = models.FloatField()
    
    def __str__(self):
        return self.title
    
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.qty} of {self.item.title}"

    def get_total_price(self):
        return self.qty * self.item.price

    def get_total_discount_price(self):
        return self.qty * self.item.discount_price

    def get_total_saving(self):
        return self.get_total_price() - self.get_total_discount_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        else:
            return self.get_total_price()
    
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact = models.IntegerField()
    pincode = models.IntegerField()
    locality = models.CharField(max_length=200)
    CITY_CHOICE = (("PRNA","PURNEA"),("PAT","PATNA"),("MHA","MUMBHAI"),("KHG","KHAGARIA"))
    city = models.CharField(max_length=10,choices=CITY_CHOICE)
    state = models.CharField(max_length=200)
    altrnative_no = models.IntegerField(null=True)
    
    def __str__(self):
        return self.name
    
class Coupon(models.Model):
    code = models.CharField(max_length=20)
    amount = models.IntegerField()
    
    def __str__(self):
        return self.code
    
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=200,null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE,null=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True)
    
    def __str__(self):
        return self.user.username

    def get_total_pay_amount(self):
        total=0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        
        if self.coupon:
            total -= self.coupon.amount
        return total
    
    def get_total_saving_amount(self):
        total=0
        for order_item in self.items.all():
            total += order_item.get_total_saving()
        return total
    
    def get_total_amount(self):
        total=0
        for order_item in self.items.all():
            total += order_item.get_total_price()
        return total
