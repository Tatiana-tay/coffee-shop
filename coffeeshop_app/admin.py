from django.contrib import admin
from coffeeshop_app.models import (Barista, FAQ, Farm, Gallery, Item , Review, 
                                   Category, Size, Ingredient,
                                   ContactUs, About)
# Register your models here.

admin.site.register(Barista)
admin.site.register(FAQ)
admin.site.register(Farm)
admin.site.register(Gallery)
admin.site.register(Item)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Ingredient)
admin.site.register(ContactUs)
admin.site.register(About)