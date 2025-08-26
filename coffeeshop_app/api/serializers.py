from rest_framework import serializers
from coffeeshop_app.models import (Item, Farm, Barista, Review, FAQ,
                                   Gallery, Category, Size, Ingredient,
                                   ContactUs, About, MailCollector)

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'
        

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class SimpleItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'image', 'avg_rating', 'categories']  # Just basic info

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

class ListItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    sizes = SizeSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        exclude = ['related_items']

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None


class ItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    sizes = SizeSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    related_items = SimpleItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Item
        fields = '__all__'
        
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = '__all__'


class BaristaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Barista
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'
        
        
class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'
        
        
class MailCollectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailCollector
        fields = '__all__'