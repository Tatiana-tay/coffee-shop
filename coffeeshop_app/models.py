from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='items/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    total_rating = models.IntegerField(default=0)
    ingredients = models.JSONField(default=list)
    sizes = models.JSONField(default=list)
    categories = models.JSONField(default=list)
    related_items = models.ManyToManyField('self', blank=True)
    description = models.TextField(blank=True)
    origin_story = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    
class Farm(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='farms/')
    area = models.FloatField()
    height = models.FloatField()
    temperature = models.FloatField()
    region = models.CharField(max_length=255)
    map_url = models.URLField(max_length=500, blank=True)
    ground_info_img = models.ImageField(upload_to='farms/ground/')
    description = models.TextField(blank=True)
    info_arr = models.JSONField(default=list)  # Stores array of {text, image}

    def __str__(self):
        return self.name
    
    
    
class Barista(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='baristas/')
    age = models.PositiveIntegerField(validators=[MinValueValidator(15)])
    position = models.CharField(max_length=255)
    experience_years = models.PositiveIntegerField()
    nationality = models.JSONField(default=list) 
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    
class Review(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="reviews")
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    rate = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rate) + " | " + self.item.name + " | " + str(self.review_user)
    
    
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    def __str__(self):
        return self.answer
    

class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')
    def __str__(self):
        return str(self.image.name)
    
    

class MailCollector(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    ai_response = models.CharField(max_length=255)

    def __str__(self):
        return self.email

